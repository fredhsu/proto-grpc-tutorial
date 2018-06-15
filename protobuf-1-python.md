# Google Protocol Buffers (protobuf) part 1 - Python 
Google Protocol buffers https://developers.google.com/protocol-buffers/ provide a langauge/platform agnostic way to serialize structured data.  Its simliar to XML or JSON, but faster, smaller, and with code generation.  One nice aspect is that I can define the structure of the data I want to work with, then generate code to work with it in multiple languages.  So I can work with the same data in Python and Go (or bunch of other languages) seamlessly.  

For this example let's say we wanted to serialize a simple routing table.  So we want to track the destination subnet, mask, next hop, metric, and interface as a route, then have multiple routes in a table.  If I were doing this in YAML a routing table might look something like this:

routingTable:
    - dest: 0.0.0.0
      mask: 0.0.0.0
      nh: 192.168.1.1
      metric: 1
      interface: eth0
    - dest: 192.168.1.0
      mask: 255.255.255.0
      nh: 192.168.1.1
      metric: 1
      interface: eth0
    - dest: 172.168.0.0
      mask: 255.255.0.0
      nh: 192.168.1.1
      metric: 10
      interface: eth0

Now let's define the same thing using protobuf:

First we start with declaring the version of protobuf we're using and the name of the package we're creating:

    syntax = "proto3";
    package tutorial;

Now we begin to define our data, by defining a `message`.  Let's start by defining a route:

  message Route {
    string dest = 1;
    string mask = 2;
    string nh = 3;
    int32 metric = 4;
    string interface = 5;
  }

In the above you'll see we give define each of the different fields of the Route, declare the type of data the field will contain, and give each field a unique integer identifier. 
Now we can roll these these routes into a routing table message:

    message RoutingTable {
        repeated Route routes = 1;
    }

Once I've defined a Route I can then use it as the data type of the `routes` field.  Since we can have many routes in a routing table I've indicated that with the `repeated` keyword.  Altogether it looks like this:

    syntax = "proto3";
    package routetable;

    // Define a route
    message Route {
        string dest = 1;
        string mask = 2;
        string nh = 3;
        int32 metric = 4;
        string interface = 5;
    }

    // Define a routing table
    message RoutingTable {
        repeated Route routes = 1;
    }

Now for the fun part, let's generate some code!  To do this we'll use the `protoc` command.  You will need to install the `protoc` binary following the instructions here: .  I'll start by creating some Python code:

`protoc --python_out=./ routetable.proto`

This will generate a Python file:

`routetable_pb2.py`

Personally I don't find the code generated to be the most readable, but let's put it to use.  I'll create a new python script that will import an use the code we just generated:

    import routetable_pb2

    route_table = routetable_pb2.RoutingTable()
    route = route_table.routes.add()

    route.dest = "0.0.0.0"
    route.mask = "0.0.0.0"
    route.nh = "10.1.1.1"
    route.metric = "1"
    route.interface = "eth0"

    print(route_table)

Now when we run th script we get this:

    $ python creatert.py
    Traceback (most recent call last):
    File "creatert.py", line 10, in <module>
        route.metric = "1"
    TypeError: '1' has type str, but expected one of: int, long

Woah!  Static typing in Python!  I'm not sure what magic makes this happen, but its super cool.  The interpreter just told me I used a string where I should've used an int.  Let's go fix it:

    route.metric=1

And then run it again

    $ python creatert.py
    routes {
    dest: "0.0.0.0"
    mask: "0.0.0.0"
    nh: "10.1.1.1"
    metric: 1
    interface: "eth0"
    }

Now I have my route table available as a Python object.  To make this useful I want to read and write it outside of my script.  For simplicity I'll write it out to a file:

    f = open("routetable.data", "wb")
    f.write(route_table.SerializeToString())
    f.close()

So now when I run the script I get a file named `routetable.data` in my directory.  In the next part we'll write some Go code that will read in this data.