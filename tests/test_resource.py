import platform
from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.version import __version__


def test_default_resource():
    options = HoneycombOptions()
    resource = create_resource(options)
    assert resource._attributes["service.name"] == "unknown_service:python"
    assert "service.version" not in resource._attributes
    assert resource._attributes["honeycomb.distro.version"] == __version__
    assert resource._attributes["honeycomb.distro.runtime_version"] == platform.python_version(
    )


def test_can_set_service_name():
    options = HoneycombOptions(service_name="my-service")
    resource = create_resource(options)
    assert resource._attributes["service.name"] == "my-service"
    assert resource._attributes["honeycomb.distro.version"] == __version__
    assert resource._attributes["honeycomb.distro.runtime_version"] == platform.python_version(
    )


def test_can_set_service_version():
    options = HoneycombOptions(service_version="1.2.3")
    resource = create_resource(options)
    assert resource._attributes["service.version"] == "1.2.3"
