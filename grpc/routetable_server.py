import grpc

import routetable_pb2
import routetable_pb2_grpc
import time
from concurrent import futures

#import route_guide_resources
class RouterServicer(routetable_pb2_grpc.RouterServicer):
    """Provides methods that implement functionality of routing server."""

    def __init__(self):
        self.db = []

    def GetRoute(self, request, context):
        print("Current route table")
        print(self.db)
        for r in self.db:
            if r.dest == request.network:
                return r
        return routetable_pb2.Route(nh="0.0.0.0")

    def AddRoutes(self, request_iterator, context):
        print("Adding route to database")
        for r in request_iterator:
            print("Adding {}".format(r))
            self.db.append(r)
        return routetable_pb2.Result(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    routetable_pb2_grpc.add_RouterServicer_to_server(
        RouterServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(1000000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()