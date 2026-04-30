"""AI Orchestrator – manages the tool-calling loop between the AI model and backend tools.

The :class:`Orchestrator` receives a user question, builds a system prompt
describing the entertainment analytics assistant role and available schema,
sends the question to the model, and iteratively invokes tools until the
model produces a final text answer.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from typing import Any

import structlog

from app.config.settings import settings
from app.models.responses import (
    ChatResponse,
    ChartPayload,
    Insight,
    SourceAttribution,
    ToolTraceEntry,
)
from app.orchestrator.model_provider import ModelProvider, ModelResponse
from app.services.analytics import AnalyticsGenerator
from app.tools.base import Tool, ToolResult

logger = structlog.get_logger(__name__)

# Maximum iterations of the tool-calling loop to prevent infinite loops.
_MAX_ITERATIONS = 5


def _build_system_prompt(tool_names: list[str]) -> str:
    """Build the system prompt describing the assistant role and schema."""

    csv_dir = os.path.join(settings.data_dir, "csv")
    csv_files: list[str] = []
    if os.path.isdir(csv_dir):
        csv_files = sorted(f for f in os.listdir(csv_dir) if f.endswith(".csv"))

    csv_section = ""
    if csv_files:
        csv_list = "\n".join(f"  - {f}" for f in csv_files)
        csv_section = f"""
Available CSV files for direct querying (via csv_query tool):
{csv_list}
"""

    return f"""\
You are an AI-powered entertainment analytics assistant for an internal \
analytics platform. Your role is to help leadership and analysts answer \
business questions by querying structured data, retrieving information from \
PDF reports, and analysing CSV files.

You have access to the following tools: {', '.join(tool_names)}.

DATABASE SCHEMA (SQLite):
The database contains the following tables and columns:

  movies: id, title, genre, release_date, duration_minutes, rating, budget, revenue, director, studio
  viewers: id, viewer_id, name, age, gender, region, subscription_tier, signup_date
  watch_activity: id, viewer_id, movie_id, watch_date, watch_duration_minutes, completed, device
  reviews: id, viewer_id, movie_id, rating, review_text, review_date
  marketing_spend: id, movie_id, campaign_name, channel, spend_amount, start_date, end_date, impressions, clicks, conversions
  regional_performance: id, movie_id, region, views, revenue, avg_rating, period_start, period_end
{csv_section}
GUIDELINES:
- Use the sql_query tool for structured data questions about movies, viewers, \
watch activity, reviews, marketing spend, and regional performance.
- Use the pdf_retrieval tool for questions about internal reports, policies, \
roadmaps, and executive summaries.
- Use the csv_query tool for direct CSV file analysis when appropriate.
- Always provide source attribution in your answers.
- When presenting numerical data, be precise and include units where applicable.
- If the data is insufficient to answer a question, say so clearly.
- Never fabricate data. Only use information returned by the tools.
- Do NOT include raw SQL queries, file paths, or connection strings in your answers.
"""


def _summarise_tool_result(result: ToolResult, max_length: int = 200) -> str:
    """Create a short summary of a tool result for the trace."""
    if result.error:
        return f"Error: {result.error}"
    if result.data is None:
        return "No data returned."
    data_str = json.dumps(result.data, default=str)
    if len(data_str) > max_length:
        return data_str[:max_length] + "…"
    return data_str


def _source_from_tool(tool_name: str, parameters: dict, result: ToolResult) -> SourceAttribution | None:
    """Derive a SourceAttribution from a tool invocation."""
    if result.error and result.data is None:
        return None

    if tool_name == "sql_query":
        return SourceAttribution(
            source_type="sql",
            source_name="SQL Database",
            detail=f"Query: {str(parameters.get('query', ''))[:120]}",
        )
    elif tool_name == "pdf_retrieval":
        filenames: set[str] = set()
        if isinstance(result.data, list):
            for chunk in result.data:
                if isinstance(chunk, dict) and chunk.get("filename"):
                    filenames.add(chunk["filename"])
        detail = ", ".join(sorted(filenames)) if filenames else "PDF search"
        return SourceAttribution(
            source_type="pdf",
            source_name="PDF Documents",
            detail=detail,
        )
    elif tool_name == "csv_query":
        filename = parameters.get("filename", "unknown")
        return SourceAttribution(
            source_type="csv",
            source_name="CSV File",
            detail=filename,
        )
    return None


class Orchestrator:
    """Manages the AI model ↔ tool interaction loop.

    Parameters
    ----------
    model_provider:
        An object satisfying the :class:`ModelProvider` protocol.
    tools:
        List of tool instances to register with the orchestrator.
    """

    def __init__(self, model_provider: ModelProvider, tools: list[Tool]) -> None:
        self._model_provider = model_provider
        self._tools: dict[str, Tool] = {t.name: t for t in tools}
        self._analytics = AnalyticsGenerator()
        # In-memory conversation history keyed by session_id.
        self._sessions: dict[str, list[dict[str, Any]]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def process_question(
        self,
        question: str,
        filters: dict | None = None,
        session_id: str | None = None,
    ) -> ChatResponse:
        """Process a user question through the tool-calling loop.

        1. Build system prompt with schema and tool definitions.
        2. Send user question to the model.
        3. If the model returns tool_calls, invoke each tool and feed
           results back.
        4. Repeat until the model returns a final text answer or the
           iteration limit is reached.
        """
        correlation_id = str(uuid.uuid4())
        if session_id is None:
            session_id = str(uuid.uuid4())

        logger.info(
            "orchestrator_process_start",
            question=question[:200],
            session_id=session_id,
            correlation_id=correlation_id,
        )

        # Build tool definitions in OpenAI format
        from app.orchestrator.model_provider import OpenAIProvider

        openai_tools = [
            OpenAIProvider.tool_to_openai_format(t) for t in self._tools.values()
        ]

        # Retrieve or initialise conversation history
        messages = self._sessions.get(session_id, [])
        if not messages:
            messages.append(
                {
                    "role": "system",
                    "content": _build_system_prompt(list(self._tools.keys())),
                }
            )

        # Append user message (include filters if provided)
        user_content = question
        if filters:
            user_content += f"\n\n[Active filters: {json.dumps(filters, default=str)}]"
        messages.append({"role": "user", "content": user_content})

        # Tracking
        tool_trace: list[ToolTraceEntry] = []
        sources: list[SourceAttribution] = []
        all_tool_results: list[ToolResult] = []

        # --- Tool-calling loop ---
        for iteration in range(_MAX_ITERATIONS):
            try:
                response: ModelResponse = await self._model_provider.chat_completion(
                    messages=messages,
                    tools=openai_tools if openai_tools else None,
                )
            except Exception as exc:
                logger.error(
                    "model_call_failed",
                    error=str(exc)[:300],
                    correlation_id=correlation_id,
                )
                answer_text = (
                    "I'm having trouble connecting to the AI model right now. "
                    "This is usually temporary — please try again in a moment."
                )
                break

            # If the model returned a final text answer (no tool calls)
            if not response.tool_calls:
                answer_text = response.content or ""
                break

            # Process each tool call
            assistant_msg: dict[str, Any] = {
                "role": "assistant",
                "content": response.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function_name,
                            "arguments": json.dumps(tc.arguments),
                        },
                    }
                    for tc in response.tool_calls
                ],
            }
            messages.append(assistant_msg)

            for tc in response.tool_calls:
                tool = self._tools.get(tc.function_name)
                if tool is None:
                    # Unknown tool – send error back to model
                    tool_response_content = json.dumps(
                        {"error": f"Unknown tool: {tc.function_name}"}
                    )
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": tool_response_content,
                        }
                    )
                    tool_trace.append(
                        ToolTraceEntry(
                            tool_name=tc.function_name,
                            input_parameters=tc.arguments,
                            output_summary=f"Error: Unknown tool '{tc.function_name}'",
                            execution_duration_ms=0.0,
                        )
                    )
                    continue

                start = time.perf_counter()
                result = await tool.execute(tc.arguments)
                elapsed_ms = (time.perf_counter() - start) * 1000

                all_tool_results.append(result)

                # Build tool response for the model
                tool_response_data: dict[str, Any] = {}
                if result.error:
                    tool_response_data["error"] = result.error
                if result.data is not None:
                    tool_response_data["data"] = result.data
                if result.metadata:
                    tool_response_data["metadata"] = result.metadata

                tool_response_content = json.dumps(tool_response_data, default=str)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": tool_response_content,
                    }
                )

                # Record trace
                tool_trace.append(
                    ToolTraceEntry(
                        tool_name=tc.function_name,
                        input_parameters=tc.arguments,
                        output_summary=_summarise_tool_result(result),
                        execution_duration_ms=round(elapsed_ms, 2),
                    )
                )

                # Record source attribution
                source = _source_from_tool(tc.function_name, tc.arguments, result)
                if source is not None:
                    sources.append(source)

                logger.info(
                    "tool_invoked",
                    tool=tc.function_name,
                    duration_ms=round(elapsed_ms, 2),
                    has_error=result.error is not None,
                    correlation_id=correlation_id,
                )
        else:
            # Reached max iterations without a final answer
            answer_text = (
                "I was unable to fully answer your question within the "
                "allowed number of steps. Please try rephrasing or "
                "simplifying your question."
            )

        # Check if all tools returned errors / empty
        if tool_trace and all(
            tr.output_summary.startswith("Error") or tr.output_summary == "No data returned."
            for tr in tool_trace
        ):
            answer_text = (
                "I wasn't able to find relevant data for your question. "
                "Please try refining your question or adjusting your filters."
            )

        # Persist conversation history
        if answer_text:
            messages.append({"role": "assistant", "content": answer_text})
        self._sessions[session_id] = messages

        # Analytics: extract chart data and insights
        chart_data: ChartPayload | None = None
        insights: list[Insight] | None = None
        if all_tool_results:
            chart_data = self._analytics.extract_chart_data(all_tool_results, question)
            insights_list = self._analytics.generate_insights(all_tool_results)
            insights = insights_list if insights_list else None

        logger.info(
            "orchestrator_process_complete",
            session_id=session_id,
            correlation_id=correlation_id,
            tool_count=len(tool_trace),
            has_chart=chart_data is not None,
            insight_count=len(insights) if insights else 0,
        )

        return ChatResponse(
            answer=answer_text,
            sources=sources,
            chart_data=chart_data,
            insights=insights,
            tool_trace=tool_trace,
            session_id=session_id,
            correlation_id=correlation_id,
        )
