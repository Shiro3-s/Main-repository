# observability/tracing.py - VERSIÓN SIMPLE
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import os
import logging

logger = logging.getLogger(__name__)

def setup_tracing(app):
    """Setup básico sin exportadores externos"""
    if os.getenv("ENABLE_TRACING", "false").lower() != "true":
        return
    
    try:
        trace.set_tracer_provider(TracerProvider())
        FastAPIInstrumentor.instrument_app(app)
        logger.info("OpenTelemetry configurado exitosamente")
    except Exception as e:
        logger.error(f"Error configurando OpenTelemetry: {e}")
        pass  # No fallar la aplicación