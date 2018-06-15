#!/usr/bin/python

import routetable_pb2

route_table = routetable_pb2.RoutingTable()
route = route_table.routes.add()

route.dest = "0.0.0.0"
route.mask = "0.0.0.0"
route.nh = "10.1.1.1"
route.metric = 1
route.interface = "eth0"

print(route_table)

f = open("routetable.data", "wb")
f.write(route_table.SerializeToString())
f.close()
