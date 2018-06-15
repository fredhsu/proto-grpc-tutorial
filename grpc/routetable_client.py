import grpc
import routetable_pb2
import routetable_pb2_grpc
import random

def random_route_generator():
    a = random.randint(1, 254)
    b = random.randint(1, 254)
    c = random.randint(1, 254)
    dest = '{}.{}.{}.{}'.format(a,b,c,0)
    nh = '{}.{}.{}.{}'.format(b,a,c,1)

    yield routetable_pb2.Route(dest=dest, mask="255.255.255.0", nh=nh, metric=1, interface="eth0")

def static_route_generator():
    a = 192
    b = 168
    c = 100
    d = 0
    dest = '{}.{}.{}.{}'.format(a,b,c,0)
    nh = '{}.{}.{}.{}'.format(b,a,c,1)

    yield routetable_pb2.Route(dest=dest, mask="255.255.255.0", nh=nh, metric=1, interface="eth0")

def add_route(stub, route_iter):
    result = stub.AddRoutes(route_iter)
    if result.success == True:
        print("Added route")
    else:
        print("Route failed")


def main():
    print("test")
    channel = grpc.insecure_channel('localhost:50051')
    stub = routetable_pb2_grpc.RouterStub(channel)
    add_route(stub, static_route_generator())
    add_route(stub, random_route_generator())

    print("Now looking up the route")

    route = stub.GetRoute(routetable_pb2.Destination(network="192.168.100.0", mask="255.255.255.0"))
    print(route)
    


if __name__ == '__main__':
    main()
