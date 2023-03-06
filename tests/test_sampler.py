from opentelemetry import context
from opentelemetry.trace import SpanKind
from opentelemetry.sdk.trace.sampling import (
    ALWAYS_OFF,
    ALWAYS_ON,
    TraceIdRatioBased,
    Decision
)

from honeycomb.opentelemetry.options import (
    HoneycombOptions,
    DEFAULT_SAMPLE_RATE
)
from honeycomb.opentelemetry.sampler import (
    configure_sampler,
    DeterministicSampler
)


def get_sampling_result(test_sampler):
    return test_sampler.should_sample(
        context.get_current(),  # parent_context
        112345678999,  # trace id
        "the_best_span",  # span name
        SpanKind.CLIENT,
        {"existing_attr": "is intact"},
        [],  # links
        {}  # trace state
    )


def test_sample_with_undefined_rate_defaults_to_ALWAYS_ON_and_recorded():
    undefined_rate_sampler = configure_sampler()
    # test the `DEFAULT_SAMPLE_RATE` is applied (i.e. 1)
    assert undefined_rate_sampler.rate == DEFAULT_SAMPLE_RATE
    # test the inner DeterministicSampler choice
    inner_sampler = undefined_rate_sampler._sampler
    assert inner_sampler == ALWAYS_ON
    assert isinstance(undefined_rate_sampler, DeterministicSampler)
    # test the SamplingResult is as expected
    sampling_result = get_sampling_result(undefined_rate_sampler)
    assert sampling_result.decision.is_sampled()
    assert sampling_result.attributes == {
        'existing_attr': 'is intact',
        'SampleRate': DEFAULT_SAMPLE_RATE
    }


def test_sampler_with_rate_of_one_is_ALWAYS_ON_and_recorded():
    sample_rate_one = HoneycombOptions(sample_rate=1)
    always_on_sampler = configure_sampler(sample_rate_one)
    # test the inner DeterministicSampler choice and rate
    inner_sampler = always_on_sampler._sampler
    assert inner_sampler == ALWAYS_ON
    assert isinstance(always_on_sampler, DeterministicSampler)
    assert always_on_sampler.rate == 1
    # test the SamplingResult is as expected
    sampling_result = get_sampling_result(always_on_sampler)
    assert sampling_result.decision.is_sampled()
    assert sampling_result.attributes == {
        'existing_attr': 'is intact',
        'SampleRate': 1
    }


def test_sampler_with_rate_of_zero_is_ALWAYS_OFF_and_DROP():
    sample_rate_zero = HoneycombOptions(sample_rate=0)
    always_off_sampler = configure_sampler(sample_rate_zero)
    # test the inner DeterministicSampler choice and rate
    inner_sampler = always_off_sampler._sampler
    assert inner_sampler == ALWAYS_OFF
    assert isinstance(always_off_sampler, DeterministicSampler)
    assert always_off_sampler.rate == 0
    # test the SamplingResult is as expected
    sampling_result = get_sampling_result(always_off_sampler)
    assert sampling_result.decision.is_sampled() is False
    assert sampling_result.decision == Decision.DROP
    assert sampling_result.attributes == {}


def test_sampler_with_rate_of_ten_configures_TraceIdRatioBased():
    sample_rate_ten = HoneycombOptions(sample_rate=10)
    trace_id_ratio_sampler = configure_sampler(sample_rate_ten)
    # test the inner DeterministicSampler choice and rate
    inner_sampler = trace_id_ratio_sampler._sampler
    assert isinstance(
        inner_sampler,
        TraceIdRatioBased
    )
    assert isinstance(
        trace_id_ratio_sampler,
        DeterministicSampler
    )
    assert trace_id_ratio_sampler.rate == 10
    assert "{0.1}" in inner_sampler.get_description()
    # test the SamplingResult is as expected
    sampling_result = get_sampling_result(trace_id_ratio_sampler)
    assert sampling_result.decision.is_sampled()
    assert sampling_result.attributes == {
        'existing_attr': 'is intact',
        'SampleRate': 10
    }
