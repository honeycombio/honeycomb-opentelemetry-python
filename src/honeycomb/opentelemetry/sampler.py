from logging import getLogger
from typing import Optional

from opentelemetry.sdk.trace.sampling import (
    ALWAYS_OFF,
    ALWAYS_ON,
    TraceIdRatioBased,
    Sampler,
    SamplingResult
)

from opentelemetry.trace import Link, SpanKind
from opentelemetry.trace.span import TraceState
from opentelemetry.util.types import Attributes
from opentelemetry.context import Context

from honeycomb.opentelemetry.options import (
    DEFAULT_SAMPLE_RATE,
    HoneycombOptions
)

_logger = getLogger(__name__)


def configure_sampler(
    options: Optional[HoneycombOptions] = None,
):
    """Configures and returns an OpenTelemetry Sampler that is
    configured based on the sample_rate determined in HoneycombOptions.
    The configuration initializes a DeterministicSampler with
    an inner sampler of either AlwaysOn (1), AlwaysOff (0),
    or a TraceIdRatio as 1/N.

    These samplers do not take into account the parent span's
    sampling decision.

    Args:
        options (HoneycombOptions): the HoneycombOptions containing
        sample_rate used to configure the deterministic sampler.

    Returns:
        DeterministicSampler: the configured Sampler based on sample_rate
    """
    if options is None:
        return DeterministicSampler(DEFAULT_SAMPLE_RATE)

    return DeterministicSampler(options.sample_rate)


class DeterministicSampler(Sampler):
    """Implementation of :class:`Sampler` that uses an inner sampler
    of either AlwaysOn (1), AlwaysOff (0), or a TraceIdRatio as 1/N
    to determine a SamplingResult and SamplingDecision for a given span
    in a trace. We append a SampleRate attribute to the span with the
    given sample rate.

    Note: These samplers do not take into account the parent span's
    sampling decision.
    """

    def __init__(self, rate: int):
        self.rate = rate

        if self.rate <= 0:
            # Sampler that never samples spans, regardless of the
            # parent span's sampling decision
            self._sampler = ALWAYS_OFF

        elif self.rate == 1:
            # Sampler that always samples spans, regardless of the
            # parent span's sampling decision
            self._sampler = ALWAYS_ON

        else:
            # Sampler that samples probabilistically based on rate..
            ratio = 1.0 / self.rate
            self._sampler = TraceIdRatioBased(ratio)

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
        # using _sampler logic based on rate (OFF, ON, TraceIdRatio)
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
