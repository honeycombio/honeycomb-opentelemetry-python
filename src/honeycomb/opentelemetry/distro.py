"""This honey-flavored Distro configures OpenTelemetry for use with Honeycomb.

TODO:  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
from logging import getLogger
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.metrics import set_meter_provider
from opentelemetry.trace import set_tracer_provider
from honeycomb.opentelemetry.metrics import create_meter_provider
from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.trace import create_tracer_provider

_logger = getLogger(__name__)


def configure_opentelemetry(
    options: HoneycombOptions = HoneycombOptions(),
):
    """
    Configures the OpenTelemetry SDK to send telemetry to Honeycomb.

    Args:
        options (HoneycombOptions, optional): the HoneycombOptions used to
        configure the the SDK. API key is a required option. These options 
        can be set either with this function or through environment variables
    """
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


# pylint: disable=too-few-public-methods
class HoneycombDistro(BaseDistro):
    """
    #TODO: explain this magic
    """

    def _configure(self, **kwargs):
        print("🐝 auto instrumented 🐝")
        configure_opentelemetry()
