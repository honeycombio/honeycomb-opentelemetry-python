"""This honey-flavored Distro configures OpenTelemetry for use with Honeycomb.

Typical usage example:

    using the opentelemetry-instrument command with
    requisite env variables set:

    $bash> opentelemetry-instrument python program.py

    or configured by code within your service:
    configure_opentelemetry(
        HoneycombOptions(
            debug=True,
            apikey=os.getenv("HONEYCOMB_API_KEY"),
            service_name="otel-python-example"
        )
    )
"""
from logging import getLogger
from typing import Optional
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.metrics import set_meter_provider
from opentelemetry.trace import set_tracer_provider
from honeycomb.opentelemetry.metrics import create_meter_provider
from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.trace import create_tracer_provider

_logger = getLogger(__name__)


def configure_opentelemetry(
    options: Optional[HoneycombOptions] = None,
):
    """
    Configures the OpenTelemetry SDK to send telemetry to Honeycomb.

    Args:
        options (HoneycombOptions, optional): the HoneycombOptions used to
        configure the the SDK. These options can be set either as parameters
        to this function or through environment variables

        Note: API key is a required option.
    """
    if options is None:
        options = HoneycombOptions()
    _logger.info("🐝 Configuring OpenTelemetry using Honeycomb distro 🐝")
    _logger.debug(vars(options))
    resource = create_resource(options)
    set_tracer_provider(
        create_tracer_provider(options, resource)
    )
    if options.metrics_dataset:
        set_meter_provider(
            create_meter_provider(options, resource)
        )


# pylint: disable=too-few-public-methods
class HoneycombDistro(BaseDistro):
    """
    An extension of the base python OpenTelemetry distro, which provides
    a mechanism to automatically configure some of the more common options
    for users. This class is auto-detected by the `opentelemetry-instrument`
    command.

    This class doesn't need to be touched directly when using the distro. If
    you'd like to explicitly set configuration in code, use the
    configure_opentelemetry() function above instead of the
    `opentelemetry-instrument` command.

    If you're wondering about the under-the-hood magic - we add the following
    declaration to package metadata in our pyproject.toml, like so:

    [tool.poetry.plugins."opentelemetry_distro"]
    distro = "honeycomb.opentelemetry.distro:HoneycombDistro"
    """

    def _configure(self, **kwargs):
        configure_opentelemetry()
