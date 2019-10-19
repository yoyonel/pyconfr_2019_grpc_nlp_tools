from contextlib import contextmanager
from typing import List

import pytest

from pyconfr_2019.grpc_nlp.tools.binary_search import binary_search_find_last_true


# https://docs.pytest.org/en/latest/example/parametrize.html#parametrizing-conditional-raising
@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize(
    "test_input, expected, expectation",
    [
        ([True, ] * i + [False, ] * j,
         max(min(i - 1, (i + j) - 2), 0),
         does_not_raise() if k > 1 else pytest.raises(ValueError,
                                                      match='range must not be empty!'))
        for k in range(1, 6)
        for i, j in zip(range(k), reversed(range(k)))
    ]
)
def test_binary_search_find_last_true(
        test_input: List[bool],
        expected: int,
        expectation
):
    with expectation:
        computed = binary_search_find_last_true(range(len(test_input)),
                                                lambda i: test_input[i])
        assert computed == expected
        # if one True in test_input list
        if any(test_input):
            assert test_input[computed]
            # if one False in test_input list
            if not all(test_input):
                assert not test_input[computed + 1]
