"""PDF Retrieval Tool – semantic search over ChromaDB pdf_chunks collection.

Returns the most relevant text chunks for a given natural-language query,
along with source document metadata for attribution.
"""

from __future__ import annotations

import os
import time

import chromadb
import structlog

from app.config.settings import settings
from app.tools.base import ToolResult

logger = structlog.get_logger(__name__)


class PDFRetrievalTool:
    """Tool that performs semantic search against indexed PDF chunks."""

    def __init__(self) -> None:
        self._chroma_client: chromadb.ClientAPI | None = None

    # -- ChromaDB helpers --------------------------------------------------

    def _get_chroma_client(self) -> chromadb.ClientAPI:
        if self._chroma_client is None:
            persist_dir = settings.chroma_persist_dir
            os.makedirs(persist_dir, exist_ok=True)
            self._chroma_client = chromadb.PersistentClient(path=persist_dir)
        return self._chroma_client

    def _get_pdf_collection(self) -> chromadb.Collection:
        client = self._get_chroma_client()
        return client.get_or_create_collection(name="pdf_chunks")

    # -- Tool protocol -----------------------------------------------------

    @property
    def name(self) -> str:
        return "pdf_retrieval"

    @property
    def description(self) -> str:
        return (
            "Search indexed PDF documents for passages relevant to a query. "
            "Returns the top-k most relevant text chunks with source metadata."
        )

    @property
    def parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search text to find relevant PDF passages.",
                },
                "top_k": {
                    "type": "integer",
                    "description": (
                        "Maximum number of chunks to return. "
                        f"Defaults to {settings.pdf_top_k}."
                    ),
                },
            },
            "required": ["query"],
        }

    async def execute(self, parameters: dict) -> ToolResult:
        """Perform semantic search and return relevant chunks."""
        query_text: str = parameters.get("query", "").strip()
        if not query_text:
            return ToolResult(
                data=None,
                error="No search query provided.",
                execution_duration_ms=0.0,
            )

        top_k: int = parameters.get("top_k", settings.pdf_top_k)
        if not isinstance(top_k, int) or top_k < 1:
            top_k = settings.pdf_top_k

        start = time.perf_counter()
        try:
            collection = self._get_pdf_collection()

            # If the collection is empty, return early
            if collection.count() == 0:
                elapsed_ms = (time.perf_counter() - start) * 1000
                return ToolResult(
                    data=[],
                    metadata={"chunk_count": 0},
                    execution_duration_ms=round(elapsed_ms, 2),
                    error="No PDF documents have been indexed yet.",
                )

            results = collection.query(
                query_texts=[query_text],
                n_results=top_k,
                include=["documents", "metadatas", "distances"],
            )

            # Unpack ChromaDB results (lists-of-lists for a single query)
            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]

            # Filter by relevance threshold.
            # ChromaDB returns L2 distances – smaller is more relevant.
            threshold = settings.pdf_relevance_threshold
            chunks: list[dict] = []
            for doc, meta, dist in zip(documents, metadatas, distances):
                if dist > threshold:
                    continue
                chunks.append(
                    {
                        "text": doc,
                        "filename": meta.get("filename", ""),
                        "chunk_index": meta.get("chunk_index", -1),
                        "distance": round(dist, 4),
                    }
                )

            elapsed_ms = (time.perf_counter() - start) * 1000

            if not chunks:
                logger.info(
                    "pdf_search_no_results",
                    query=query_text,
                    top_k=top_k,
                    duration_ms=round(elapsed_ms, 2),
                )
                return ToolResult(
                    data=[],
                    metadata={"chunk_count": 0},
                    execution_duration_ms=round(elapsed_ms, 2),
                    error="No relevant PDF passages found for the given query.",
                )

            logger.info(
                "pdf_search_executed",
                query=query_text,
                top_k=top_k,
                chunk_count=len(chunks),
                duration_ms=round(elapsed_ms, 2),
            )

            return ToolResult(
                data=chunks,
                metadata={"chunk_count": len(chunks)},
                execution_duration_ms=round(elapsed_ms, 2),
            )

        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.error(
                "pdf_search_failed",
                query=query_text,
                duration_ms=round(elapsed_ms, 2),
                error=str(exc),
            )
            return ToolResult(
                data=None,
                error="PDF search failed. Please try again.",
                execution_duration_ms=round(elapsed_ms, 2),
            )
