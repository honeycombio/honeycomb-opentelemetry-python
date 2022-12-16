"""
Add module doc string
"""
from honeycomb.opentelemetry.metrics import create_meter_provider
from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.trace import create_tracer_provider
from logging import getLogger
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.metrics import set_meter_provider
from opentelemetry.trace import set_tracer_provider

_logger = getLogger(__name__)


def configure_opentelemetry(
    options: HoneycombOptions = HoneycombOptions(),
):
    _logger.debug("🐝 Configuring OpenTelemetry using Honeycomb distro 🐝")
    _logger.debug(vars(options))
    resource = create_resource(options)
    set_tracer_provider(
        create_tracer_provider(options, resource)
    )
    if options.metrics_dataset:
        set_meter_provider(
            create_meter_provider(options, resource)
        )


class HoneycombDistro(BaseDistro):
    """
    This honey-flavored Distro configures OpenTelemetry for use with Honeycomb.
    """

    def _configure(self, **kwargs):
        print("🐝 auto instrumented 🐝")
        configure_opentelemetry()
