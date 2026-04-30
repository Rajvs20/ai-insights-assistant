"""FastAPI application entry point."""

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.error_handlers import register_error_handlers
from app.api.middleware import CorrelationIdMiddleware
from app.config.settings import settings

logger = structlog.get_logger(__name__)


def _create_orchestrator():
    """Build and return an Orchestrator with model provider and tools."""
    from app.orchestrator.model_provider import OpenAIProvider
    from app.orchestrator.orchestrator import Orchestrator
    from app.tools.csv_tool import CSVQueryTool
    from app.tools.pdf_tool import PDFRetrievalTool
    from app.tools.sql_tool import SQLQueryTool

    provider = OpenAIProvider(
        api_key=settings.gemini_api_key or settings.openai_api_key,
        model_name=settings.model_name,
    )
    tools = [
        SQLQueryTool(),
        PDFRetrievalTool(),
        CSVQueryTool(),
    ]
    return Orchestrator(model_provider=provider, tools=tools)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown hooks."""
    logger.info("Starting AI Insights Assistant")

    # Run startup data loading (create tables, ingest seed data)
    from app.startup import run_startup

    run_startup()

    # Initialise the orchestrator and store on app.state
    orchestrator = _create_orchestrator()
    app.state.orchestrator = orchestrator
    logger.info("Orchestrator initialised with tools")

    yield
    logger.info("Shutting down AI Insights Assistant")


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

# --- Middleware (order matters: outermost first) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationIdMiddleware)

# --- Error handlers ---
register_error_handlers(app)

# --- Routers ---
from app.api.auth_routes import router as auth_router  # noqa: E402
from app.api.chat_routes import router as chat_router  # noqa: E402
from app.api.data_routes import router as data_router  # noqa: E402
from app.api.health_routes import router as health_router  # noqa: E402
from app.api.ingest_routes import router as ingest_router  # noqa: E402

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(ingest_router)
app.include_router(data_router)
