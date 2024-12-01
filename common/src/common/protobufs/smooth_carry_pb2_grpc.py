# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import smooth_carry_pb2 as smooth__carry__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in smooth_carry_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class SmoothCarryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_smooth_carry = channel.unary_unary(
                '/raw_data.SmoothCarry/get_smooth_carry',
                request_serializer=smooth__carry__pb2.SmoothCarryRequest.SerializeToString,
                response_deserializer=smooth__carry__pb2.SmoothCarryResponse.FromString,
                _registered_method=True)


class SmoothCarryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_smooth_carry(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SmoothCarryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_smooth_carry': grpc.unary_unary_rpc_method_handler(
                    servicer.get_smooth_carry,
                    request_deserializer=smooth__carry__pb2.SmoothCarryRequest.FromString,
                    response_serializer=smooth__carry__pb2.SmoothCarryResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'raw_data.SmoothCarry', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('raw_data.SmoothCarry', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class SmoothCarry(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_smooth_carry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/raw_data.SmoothCarry/get_smooth_carry',
            smooth__carry__pb2.SmoothCarryRequest.SerializeToString,
            smooth__carry__pb2.SmoothCarryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)