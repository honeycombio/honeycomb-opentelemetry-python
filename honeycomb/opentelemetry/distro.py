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
    options: HoneycombOptions = HoneycombOptions(),
):
    resource = create_resource(options)
    set_tracer_provider(
        create_tracer_provider(options, resource)
    )
    set_meter_provider(
        create_meter_provider(options, resource)
    )


class HoneycombDistro(BaseDistro):
    """
    This honey-flavored Distro configures OpenTelemetry for use with Honeycomb.
    """

    def _configure(self, **kwargs):
        print('🐝 auto instrumented 🐝')
        configure_opentelemetry()
