from opentelemetry import context
from opentelemetry.trace import SpanKind
from opentelemetry.sdk.trace.sampling import (
    DEFAULT_OFF,
    DEFAULT_ON,
    ParentBasedTraceIdRatio,
    Decision
)

from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.sampler import (
    configure_sampler,
    DeterministicSampler
)


def get_sampling_result(test_sampler):
    return test_sampler.should_sample(
        context.get_current(),  # parent_context
        "d4cda95b652f4a1592b449d5929fda1b",  # trace id
        "the_best_span",  # span name
        SpanKind.CLIENT,
        {"thingy": "attribute"},
        [],  # links
        {}  # trace state
    )


def test_undefined_defaults_to_DEFAULT_ON():
    deterministic_sampler = configure_sampler()
    assert isinstance(deterministic_sampler, DeterministicSampler)
    assert deterministic_sampler.rate == 1
    assert deterministic_sampler._sampler == DEFAULT_ON

    result = get_sampling_result(deterministic_sampler)
    assert result.decision == Decision.RECORD_AND_SAMPLE


def test_sampler_with_rate_of_1_defaults_to_DEFAULT_ON():
    deterministic_sampler = configure_sampler(HoneycombOptions(sample_rate=1))
    assert isinstance(deterministic_sampler, DeterministicSampler)
    assert deterministic_sampler.rate == 1
    assert deterministic_sampler._sampler == DEFAULT_ON

    # TODO: get result decision, assert RECORD_AND_SAMPLED
    # assert sample rate attribute


def test_sampler_with_rate_of_0_defaults_to_DEFAULT_OFF():
    options = HoneycombOptions(sample_rate=0)
    deterministic_sampler = configure_sampler(options)
    assert isinstance(deterministic_sampler, DeterministicSampler)
    assert deterministic_sampler.rate == 0
    assert deterministic_sampler._sampler == DEFAULT_OFF

    # TODO: test result decisions


def test_sampler_with_rate_of_10_configures_ParentBasedTraceIdRatio():
    deterministic_sampler = configure_sampler(HoneycombOptions(sample_rate=10))
    assert isinstance(deterministic_sampler, DeterministicSampler)
    assert deterministic_sampler.rate == 10
    assert isinstance(
        deterministic_sampler._sampler,
        ParentBasedTraceIdRatio
    )

    # TODO: test result decisions
    # assert sample rate attribute

# TODO: add a test that our custom sample rate has been added
# AND other attributes are intact?
