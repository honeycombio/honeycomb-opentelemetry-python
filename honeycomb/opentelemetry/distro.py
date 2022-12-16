"""
Add module doc string
"""
from logging import getLogger
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.metrics import set_meter_provider
from opentelemetry.trace import set_tracer_provider
from honeycomb.opentelemetry.metrics import create_meter_provider
from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.trace import create_tracer_provider
from honeycomb.opentelemetry.sampler import configure_sampler

_logger = getLogger(__name__)


def configure_opentelemetry(
    options: HoneycombOptions = HoneycombOptions(),
):
    """
    Configures the OpenTelemetry SDK to send telemetry to Honeycomb.

    Args:
        options (HoneycombOptions, optional): the HoneycombOptions used to
        configure the the SDK
    """
    _logger.debug("🐝 Configuring OpenTelemetry using Honeycomb distro 🐝")
    _logger.debug(vars(options))
    resource = create_resource(options)
    set_tracer_provider(
        create_tracer_provider(options, resource)
    )
    set_meter_provider(
        create_meter_provider(options, resource)
    )

    configure_sampler(options)


# pylint: disable=too-few-public-methods
class HoneycombDistro(BaseDistro):
    """
    This honey-flavored Distro configures OpenTelemetry for use with Honeycomb.
    """

    def _configure(self):
        print("🐝 auto instrumented 🐝")
        configure_opentelemetry()
