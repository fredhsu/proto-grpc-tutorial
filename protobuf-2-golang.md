# Google Protocol Buffers (protobuf) part 2 - Go
In part 1 I used protobuf to serialize a Python object that represented a routing table and wrote it out to a file.  In this part I'll read in that same data file, but in Go instead of Python.  What I'm trying to highlight here is that we can use protocol buffers to read/write/manipulate data in different programming languages, but with a single definition of what that data looks like.

I'll be using the *same* `.proto` file that I used in part 1, but now I'm going to use the `protoc` tool to generate Go code instead.  

`protoc --go_out=./ routetable.proto`

If you compare it to the previous example, we simply switched from `--python_out` to `--go_out`.

After running the command I get this file in my directory:

`routetable.pb.go`

We can import and use the generated code to unmarshal the routing table we saved earlier.  To build the Go code properly, the code has to be setup in the proper project folder structure.  I've put it under a `protobuftutorial/routetable` folder in my github repo, which I can the import like this:

    import "github.com/fredhsu/protobuftutorial/routetable"

Now let's read the data file and unmarshal it into a Go struct for use:

    in, err := ioutil.ReadFile("routetable.data")
    if err != nil {
        log.Fatalln("Error reading file:", err)
    }
    routeTable := &rt.RoutingTable{}
    if err := proto.Unmarshal(in, routeTable); err != nil {
        log.Fatalln("Failed to parse :", err)
    }

Finally we can access the different data fields using the generated Getters:

    fmt.Println(routeTable.GetRoutes())
    fmt.Println("Destination of the first route is: " + routeTable.GetRoutes()[0].GetDest())

Putting it all together:

And running the code:

    $ go run main.go
    [dest:"0.0.0.0" mask:"0.0.0.0" nh:"10.1.1.1" metric:1 interface:"eth0" ]
    Destination of the first route is: 0.0.0.0

To recap, we started with a protocol buffer specification to define our data object in a language agnostic way.  Next, we used the `protoc` compiler to generate both Python and Go code.  Finally, we were able to use the generated code to manipulate and serialize the data into binary form in one langauge, and deserialize the data in another.  As you can see protocol buffers give a flexible and efficient way to share data.  In the next part we'll leverage this binary encoding to make RPC calls using gRPC.