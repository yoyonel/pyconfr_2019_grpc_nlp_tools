import itertools
from typing import Any, Iterator

import grpc


def abort_if_empty(
        it_on_data: Iterator[Any],
        context,
        abort_details: str,
        abort_code: grpc.StatusCode = grpc.StatusCode.INVALID_ARGUMENT,
):
    """

    Args:
        it_on_data:
        context:
        abort_details:
        abort_code:

    Returns:

    """
    try:
        first_element = next(it_on_data)
    except StopIteration:
        # http://avi.im/grpc-errors/#python
        # https://grpc.github.io/grpc/python/grpc.html#grpc-exceptions
        # https://grpc.github.io/grpc/python/grpc.html#grpc.ServicerContext.abort
        # https://stackoverflow.com/a/48791071
        context.abort(abort_code, abort_details)
    else:
        # rebuild generator with the first tweet
        # https://docs.python.org/3/library/itertools.html#itertools.chain
        return itertools.chain([first_element], it_on_data)
