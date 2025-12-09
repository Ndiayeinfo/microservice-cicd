from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


def setup_tracing(service_name: str):
    """
    Initialise le tracing OpenTelemetry pour un microservice FastAPI
    et retourne un tracer utilisable dans le code métier.
    """

    # 1. Déclarer le provider avec le nom du service
    provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: service_name})
    )
    trace.set_tracer_provider(provider)

    # 2. Exporter vers Jaeger (OTLP HTTP endpoint)
    exporter = OTLPSpanExporter(
        endpoint="http://jaeger:4318/v1/traces",
    )

    # 3. Ajouter au processeur
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    # 4. Retourner un tracer opérationnel
    return trace.get_tracer(service_name)
