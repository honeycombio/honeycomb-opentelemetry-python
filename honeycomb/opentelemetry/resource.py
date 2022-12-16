import platform
from opentelemetry.sdk.resources import Resource
from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.version import __version__


def create_resource(options: HoneycombOptions):
    """
    Configures and returns a new OpenTelemetry Resource.

    Args:
        options (HoneycombOptions): the Honeycomb options to configure with
        resource (Resource): the resource to use with the new resource

    Returns:
        MeterProvider: the new Resource
    """
    attributes = {
        "service.name": options.service_name,
        "honeycomb.distro.version": __version__,
        "honeycomb.distro.runtime_version": platform.python_version()
    }
    if options.service_version:
        attributes["service.version"] = options.service_version
    return Resource.create(attributes)
