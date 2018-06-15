# Part 3 - gRPC in Python
Now that we have a foundation in protocol buffers, we're ready to tackle gRPC.  gRPC allows clients to call methods on a remote server as if it were running on the same machine.  With gRPC you define a service using protcol buffers, then once you've defined the service, you can generate the code for the client and server.  After implmenting the service on the server side, the client can make calls to the methods.  Since it uses protocol buffers, the clients and servers can be written in multiple languages and are interoperable.  For this example we'll create the server in Python, and clients in Python and Go.

Let's begin by defining our service:
```
  service Router {

  }
```
Now we define the methods for that service using protocol buffers.  There are a four different types of methods depending on what type of request and response you want.  For this example we'll use two of them, simple RPC and response-streaming RPC.  The simple RPC will just be a method call and returns a value.  Response-streaming has the client send a message, then the server will respond with a sequence of messages.  The client will consume these responses until there are no more messages.  This is signified by using the `stream` keyword in front of the return value.
```
  service Router {
    // GetNextHop(Subnet) is a simple RPC that will return the route to a given destination 
    rpc GetRoute(Destination) returns (Route) {}

    // ListRoutes() is a response-streaming RPC to list the routes in the routing table
    rpc ListRoutes() returns (stream Route) {}
  }
```

Now we define the message types that are used in the requests and responses, this should look familiar after working with protocol buffers, in fact I'll use the same `Route` message that we used earlier:

```
  message Route {
    string dest = 1;
    string mask = 2;
    string nh = 3;
    int32 metric = 4;
    string interface = 5;
  }
```

```
  message Destination {
    string network = 1;
    string mask = 2;
  }
```

Now let's take this and create our gRPC service.  We'll another code generator to create both the client and server code for this RPC.  First we install the gRPC tools for Python:

```bash
  $ pip install grpcio-tools
```

Then we can generate our code:

```python
  $ python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. routetable.proto
```

You should now see two additional files:
```
routetable_pb2.py
routetable_pb2_grpc.py
```

Take a look inside the `routetable_pb2_grpc.py` file, and you'll see the following method defined:
```python
def GetRoute(self, request, context):
    """GetNextHop(Subnet) is a simple RPC that will return the route to a given destination 
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
```

You can see it created the `GetRoute` method based on the protobuf definition given, and for now just raises a `Not Implemented` error.  It is our job to create the server logic.  To do that I'll create a new file to implement the class methods for our service called `routetable_server.py`.  

First I import the *grpc* library, the generated code, and a few standard libraries we'll use later.

```python
import grpc

import routetable_pb2
import routetable_pb2_grpc
import time
from concurrent import futures
```

Next I am going to create a new class that inherits from the *grpc* one, and create an `init` function to setup our inital route table which is just an empty list:
```python
class RouterServicer(routetable_pb2_grpc.RouterServicer):
    """Provides methods that implement functionality of routing server."""

    def __init__(self):
        self.db = []
```

Now I will implement the two methods for our RPC:

```python
    def GetRoute(self, request, context):
        for r in self.db:
            if r.dest == request.destination:
                return r
        return routetable_pb2.Route(nh="0.0.0.0")

    def AddRoutes(self, request_iterator, context):
        for r in request_iterator:
            self.db.append(r)
        return routetable_pb2.Result(success=True)
```

For the `GetRoute` method we go through our route table and see if there is a match.  If so, we return that, otherwise we set the next hop to be `0.0.0.0` and return it.
For `AddRoutes` we go through all the routes that were sent, and append them to our route database.  We then return a `success=True` result.

Finally I create a function to create the RPC server and run it:

```python
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
```

Ok now that we've got the server, we need to create a client to exercise the server.  