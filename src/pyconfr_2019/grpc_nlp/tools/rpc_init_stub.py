"""

"""
import logging

from grpc import insecure_channel

from pyconfr_2019.grpc_nlp.tools.check_connectivity import check_connectivity

logger = logging.getLogger(__name__)


def rpc_init_stub(
        addr,
        port,
        service_stub,
        wait_for_connection=True,
        service_name="",
):
    """

    :param addr:
    :type addr: str
    :param port:
    :type port: int
    :param service_stub:
    :param wait_for_connection:
    :type wait_for_connection: bool
    :param service_name:
    :type service_name: str
    :return:
    """
    target = "{}:{}".format(addr, port)

    channel = insecure_channel(target)

    if wait_for_connection:
        logger.info("Connection to: [{}]/{} - WAITING ...".format(target, service_name))
        check_connectivity(channel)

    logger.info("Connection to: [{}]/{} - ESTABLISHED".format(target, service_name))
    return service_stub(channel)
