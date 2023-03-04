# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import messages_pb2 as messages__pb2


class ServerStub(object):
  """The service definition of the main Server
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ReceiveMessageFromClient = channel.unary_unary(
        '/messages.Server/ReceiveMessageFromClient',
        request_serializer=messages__pb2.MessageToServer.SerializeToString,
        response_deserializer=messages__pb2.ServerLog.FromString,
        )


class ServerServicer(object):
  """The service definition of the main Server
  """

  def ReceiveMessageFromClient(self, request, context):
    """Receives a message from the client and sends some log back
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ServerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ReceiveMessageFromClient': grpc.unary_unary_rpc_method_handler(
          servicer.ReceiveMessageFromClient,
          request_deserializer=messages__pb2.MessageToServer.FromString,
          response_serializer=messages__pb2.ServerLog.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'messages.Server', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
