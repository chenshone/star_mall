# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import inventory_pb2 as inventory__pb2


class InventoryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SetInv = channel.unary_unary(
            "/Inventory/SetInv",
            request_serializer=inventory__pb2.GoodsInvInfo.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.InvDetail = channel.unary_unary(
            "/Inventory/InvDetail",
            request_serializer=inventory__pb2.GoodsInvInfo.SerializeToString,
            response_deserializer=inventory__pb2.GoodsInvInfo.FromString,
        )
        self.Sell = channel.unary_unary(
            "/Inventory/Sell",
            request_serializer=inventory__pb2.SellInfo.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.Reback = channel.unary_unary(
            "/Inventory/Reback",
            request_serializer=inventory__pb2.SellInfo.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )


class InventoryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SetInv(self, request, context):
        """设置库存"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def InvDetail(self, request, context):
        """获取库存信息"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Sell(self, request, context):
        """扣减库存"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Reback(self, request, context):
        """库存归还"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_InventoryServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "SetInv": grpc.unary_unary_rpc_method_handler(
            servicer.SetInv,
            request_deserializer=inventory__pb2.GoodsInvInfo.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "InvDetail": grpc.unary_unary_rpc_method_handler(
            servicer.InvDetail,
            request_deserializer=inventory__pb2.GoodsInvInfo.FromString,
            response_serializer=inventory__pb2.GoodsInvInfo.SerializeToString,
        ),
        "Sell": grpc.unary_unary_rpc_method_handler(
            servicer.Sell,
            request_deserializer=inventory__pb2.SellInfo.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "Reback": grpc.unary_unary_rpc_method_handler(
            servicer.Reback,
            request_deserializer=inventory__pb2.SellInfo.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "Inventory", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Inventory(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SetInv(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/Inventory/SetInv",
            inventory__pb2.GoodsInvInfo.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def InvDetail(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/Inventory/InvDetail",
            inventory__pb2.GoodsInvInfo.SerializeToString,
            inventory__pb2.GoodsInvInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Sell(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/Inventory/Sell",
            inventory__pb2.SellInfo.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Reback(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/Inventory/Reback",
            inventory__pb2.SellInfo.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
