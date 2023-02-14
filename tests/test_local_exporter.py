from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.trace.span import SpanContext
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from honeycomb.opentelemetry.local_exporter import LocalTraceLinkSpanExporter
from tests.utils import APIKEY, CLASSIC_APIKEY

TRACE_ID = 220134740205765644819457394801066567152
SPAN_ID = 7394801066567152


def _check_exporter_can_export_spans_successfully(exporter: SpanExporter):
    result = exporter.export([
        ReadableSpan(
            context=SpanContext(
                trace_id=TRACE_ID,
                span_id=SPAN_ID,
                is_remote=False
            ),
        )
    ])
    assert result == SpanExportResult.SUCCESS


def test_exporter_formats_correct_url_and_in_stdout(requests_mock, capsys):
    requests_mock.get("https://api.honeycomb.io/1/auth",
                      json={"environment": {"slug": "my-env"}, "team": {"slug": "my-team"}})
    exporter = LocalTraceLinkSpanExporter(
        service_name="my-service", apikey=APIKEY)
    url = exporter._build_url(TRACE_ID)
    assert url == "https://ui.honeycomb.io/my-team/environments/my-env/datasets/my-service/trace?trace_id=a59c68a6de76d5e642bdc9a7641ae5f0"
    _check_exporter_can_export_spans_successfully(exporter)
    # ensure the link is in stdout
    captured = capsys.readouterr()
    assert captured.out == 'Honeycomb link: https://ui.honeycomb.io/my-team/environments/my-env/datasets/my-service/trace?trace_id=a59c68a6de76d5e642bdc9a7641ae5f0\n'


def test_exporter_formats_correct_url_classic_and_in_stdout(requests_mock, capsys):
    requests_mock.get("https://api.honeycomb.io/1/auth",
                      json={"team": {"slug": "my-team"}})
    exporter = LocalTraceLinkSpanExporter(
        service_name="my-service", apikey=CLASSIC_APIKEY)
    url = exporter._build_url(TRACE_ID)
    assert url == "https://ui.honeycomb.io/my-team/datasets/my-service/trace?trace_id=a59c68a6de76d5e642bdc9a7641ae5f0"
    _check_exporter_can_export_spans_successfully(exporter)
    # ensure the link is in stdout
    captured = capsys.readouterr()
    assert captured.out == 'Honeycomb link: https://ui.honeycomb.io/my-team/datasets/my-service/trace?trace_id=a59c68a6de76d5e642bdc9a7641ae5f0\n'


def test_exporter_without_apikey_does_not_build_url():
    exporter = LocalTraceLinkSpanExporter(
        service_name="my-service", apikey=None)
    url = exporter._build_url(TRACE_ID)
    assert url is None
    _check_exporter_can_export_spans_successfully(exporter)
