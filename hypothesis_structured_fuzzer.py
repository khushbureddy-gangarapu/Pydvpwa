import sys
import atheris
import ujson
from hypothesis import given, strategies as st

# We could define all these inline within the call to @given(),
# but it's a bit easier to read if we name them here instead.
JSON_ATOMS = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-(2 ** 63), max_value=2 ** 63 - 1),
    st.floats(allow_nan=False, allow_infinity=False),
    st.text(),
)
JSON_OBJECTS = st.recursive(
    base=JSON_ATOMS,
    extend=lambda inner: st.lists(inner) | st.dictionaries(st.text(), inner),
)
UJSON_ENCODE_KWARGS = {
    "ensure_ascii": st.booleans(),
    "encode_html_chars": st.booleans(),
    "escape_forward_slashes": st.booleans(),
    "sort_keys": st.booleans(),
    "indent": st.integers(0, 20),
}


@given(obj=JSON_OBJECTS, kwargs=st.fixed_dictionaries(UJSON_ENCODE_KWARGS))
@atheris.instrument_func
def test_ujson_roundtrip(obj, kwargs):
    """Check that all JSON objects round-trip regardless of other options."""
    assert obj == ujson.decode(ujson.encode(obj, **kwargs))


if __name__ == "__main__":
    # Running `pytest hypothesis_structured_fuzzer.py` will replay, deduplicate,
    # and minimize any failures discovered by earlier runs or by OSS-Fuzz, or
    # briefly search for new failures if none are known.
    # Or, when running via OSS-Fuzz, we'll execute it via the fuzzing hook:
    atheris.instrument_all()
    atheris.Setup(sys.argv, atheris.instrument_func(test_ujson_roundtrip.hypothesis.fuzz_one_input))
    atheris.Fuzz()
