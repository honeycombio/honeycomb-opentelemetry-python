"""
Add module doc string
"""
from honeycomb.opentelemetry.metrics import create_meter_provider
from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.trace import create_tracer_provider
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.metrics import set_meter_provider
from opentelemetry.trace import set_tracer_provider


def configure_opentelemetry(
    apikey: str = None,
    service_name: str = None,
    endpoint: str = None
):
    options = HoneycombOptions(apikey, service_name, endpoint)
    resource = create_resource(options)
    set_tracer_provider(
        create_tracer_provider(options, resource)
    )
    if options.enable_metrics:
        set_meter_provider(
            create_meter_provider(options, resource)
        )


class HoneycombDistro(BaseDistro):
    """
    The OpenTelemetry provided Distro configures a default set of
    configuration out of the box.
    """

    def _configure(self, **kwargs):
        configure_opentelemetry()
