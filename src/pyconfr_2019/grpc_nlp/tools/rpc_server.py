import logging
import os
import signal
import time
from concurrent import futures
from typing import Callable, Optional

try:
    import grpc
except ImportError:
    raise ModuleNotFoundError("grpc is needed in order to "
                              "launch RPC server (`pip install .[grpc]`)")

logger = logging.getLogger(__name__)

SIGNALS = [signal.SIGINT, signal.SIGTERM]
_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def _signal_handler(sig, stack):
    """ Empty signal handler used to override python default one """
    pass


def serve(
        server_name: str,
        caller_add_service_servicer_to_server: Callable[[grpc.Server], None],
        grpc_host_and_port: str,
        number_of_concurrent_client: int = 500,
        block: bool = True
) -> Optional[grpc.Server]:
    """
    Start a new instance of `` service.

    If the server can't be started, a ConnectionError exception is raised

    :param server_name:
    :type server_name: str

    :param caller_add_service_servicer_to_server:
    :type caller_add_service_servicer_to_server:

    :param number_of_concurrent_client:
    :type number_of_concurrent_client: int

    :param block: If True, block until interrupted.
                  If False, start the server and return directly
    :type block: bool

    :param grpc_host_and_port: Listening address of the server.
    :type grpc_host_and_port: str

    :return: If ``block`` is True, return nothing.
             If ``block`` is False, return the server instance
    :rtype: None | grpc.server
    """

    # Register signal handler, only if blocking
    if block:
        for sig in SIGNALS:
            signal.signal(sig, _signal_handler)

    # We set this number high to allow basically anyone to connect with us
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=number_of_concurrent_client),
        maximum_concurrent_rpcs=number_of_concurrent_client
    )

    # add service(s) to server
    caller_add_service_servicer_to_server(server)

    port = server.add_insecure_port(grpc_host_and_port)
    if port == 0:
        logger.error(f"Failed to start gRPC server on {grpc_host_and_port}")
        raise ConnectionError()

    logger.info(f"Starting {server_name} server on {grpc_host_and_port}...")
    server.start()
    logger.info("Ready and waiting for connections.")

    if not block:
        return server

    if os.name == 'posix':
        # Wait for a signal before exiting
        # ps: not working/existing on Windows ...
        # TODO: look at
        #  - https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_server_with_reflection.py
        #  - https://github.com/grpc/grpc/pull/19299/files
        sig = signal.sigwait(SIGNALS)
        logger.info('Signal {} received, shutting down...'.format(sig))
        #
        server.stop(5).wait()
    elif os.name == 'nt':
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(5).wait()
