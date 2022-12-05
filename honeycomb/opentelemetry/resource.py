from honeycomb.opentelemetry.options import HoneycombOptions
from opentelemetry.sdk.resources import Resource
from honeycomb.opentelemetry.version import __version__


def create_resource(options: HoneycombOptions):
    return Resource.create({
        "service.name": options.service_name,
        "honeycomb.distro.version": __version__,
        "honeycomb.distro.runtime_version": platform.python_version()
    })
