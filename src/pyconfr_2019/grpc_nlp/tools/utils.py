from collections.abc import MutableMapping, MutableSequence, MutableSet

import dictdiffer
from _pytest.python_api import ApproxScalar

DICT_TYPES = (MutableMapping,)
LIST_TYPES = (MutableSequence,)
SET_TYPES = (MutableSet,)


def make_hashable(o):
    """
    https://stackoverflow.com/a/42151923
    """
    if isinstance(o, LIST_TYPES):
        return list((make_hashable(e) for e in o))

    if isinstance(o, DICT_TYPES):
        return '{dict}' + str(
            sorted((k, make_hashable(v)) for k, v in o.items())
        )

    if isinstance(o, SET_TYPES):
        return set(sorted(make_hashable(e) for e in o))

    return o


def sorted_nested_container(d):
    if isinstance(d, DICT_TYPES):
        return {
            k: sorted_nested_container(v)
            for k, v in iter(d.items())
        }

    if isinstance(d, LIST_TYPES):
        return sorted(map(sorted_nested_container, d), key=make_hashable)

    return d


def compare_containers(computed, expected, sort_insensitive=True):
    if sort_insensitive:
        computed = sorted_nested_container(computed)
        expected = sorted_nested_container(expected)
    return list(
        dictdiffer.diff(computed, expected,
                        tolerance=ApproxScalar.DEFAULT_RELATIVE_TOLERANCE))
