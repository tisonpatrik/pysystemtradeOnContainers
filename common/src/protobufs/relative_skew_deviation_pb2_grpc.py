# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import relative_skew_deviation_pb2 as relative__skew__deviation__pb2

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
        + f' but the generated code in relative_skew_deviation_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class RelativeSkewDeviationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_relative_skew_deviation = channel.unary_unary(
                '/raw_data.RelativeSkewDeviation/get_relative_skew_deviation',
                request_serializer=relative__skew__deviation__pb2.RelativeSkewDeviationRequest.SerializeToString,
                response_deserializer=relative__skew__deviation__pb2.RelativeSkewDeviationResponse.FromString,
                _registered_method=True)


class RelativeSkewDeviationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_relative_skew_deviation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RelativeSkewDeviationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_relative_skew_deviation': grpc.unary_unary_rpc_method_handler(
                    servicer.get_relative_skew_deviation,
                    request_deserializer=relative__skew__deviation__pb2.RelativeSkewDeviationRequest.FromString,
                    response_serializer=relative__skew__deviation__pb2.RelativeSkewDeviationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'raw_data.RelativeSkewDeviation', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('raw_data.RelativeSkewDeviation', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class RelativeSkewDeviation(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_relative_skew_deviation(request,
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
            '/raw_data.RelativeSkewDeviation/get_relative_skew_deviation',
            relative__skew__deviation__pb2.RelativeSkewDeviationRequest.SerializeToString,
            relative__skew__deviation__pb2.RelativeSkewDeviationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
