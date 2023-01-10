from logging import getLogger

from opentelemetry.sdk.trace.sampling import (
    DEFAULT_OFF,
    DEFAULT_ON,
    ParentBasedTraceIdRatio,
    Sampler,
    SamplingResult
)
# DEFAULT_OFF,
# ParentBasedTraceIdRatio
# not Decision // call and inner sampler instead

from opentelemetry.trace import Link, SpanKind
from opentelemetry.trace.span import TraceState
from opentelemetry.util.types import Attributes
from opentelemetry.context import Context

from honeycomb.opentelemetry.options import HoneycombOptions

_logger = getLogger(__name__)


def configure_sampler(
    options: HoneycombOptions = HoneycombOptions(),
):
    return DeterministicSampler(options.sample_rate)


class DeterministicSampler(Sampler):
    """
    Custom samplers can be created by subclassing Sampler and implementing
    Sampler.should_sample as well as Sampler.get_description.
    """

    def __init__(self, rate: int):
        self.rate = rate

        # Can't use match/case statement until minimum Python 3.10
        if self.rate == 0:
            # Sampler that respects its parent span's sampling decision,
            # but otherwise never samples.
            self._sampler = DEFAULT_OFF
            print("[DeterministicSampler] default off")

        elif self.rate == 1:
            # Sampler that respects its parent span's sampling decision,
            # but otherwise always samples.
            self._sampler = DEFAULT_ON
            print("[DeterministicSampler] default on")

        elif self.rate > 1:
            # Sampler that respects its parent span's sampling decision,
            # but otherwise samples probabalistically based on `rate`.
            ratio = 1.0 / self.rate
            self._sampler = ParentBasedTraceIdRatio(ratio)
            print(f"[DeterministicSampler] traceId ratio: {ratio}")

    def _configure(self):
        configure_sampler()

    # pylint: disable=too-many-arguments
    def should_sample(
        self,
        parent_context: Context,
        trace_id: int,
        name: str,
        kind: SpanKind = None,
        attributes: Attributes = None,
        links: Link = None,
        trace_state: "TraceState" = None
    ) -> "SamplingResult":
        # append our SampleRate field to attributes
        sample_rate = {'SampleRate': self.rate}
        if attributes is None:
            attributes = sample_rate
        else:
            attributes.update(sample_rate)

        return self._sampler.should_sample(
            parent_context,
            trace_id,
            name,
            kind,
            attributes,
            links,
            trace_state
        )

    def get_description(self) -> str:
        return "HNYDeterministicSampler"
