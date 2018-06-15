package main

import (
	"fmt"
	"io/ioutil"
	"log"

	rt "github.com/fredhsu/protobuftutorial/routetable"
	"github.com/golang/protobuf/proto"
)

func main() {
	// Read the existing route table data file
	in, err := ioutil.ReadFile("routetable.data")
	if err != nil {
		log.Fatalln("Error reading file:", err)
	}
	routeTable := &rt.RoutingTable{}
	if err := proto.Unmarshal(in, routeTable); err != nil {
		log.Fatalln("Failed to parse :", err)
	}
	fmt.Println(routeTable.GetRoutes())
	fmt.Println("Destination of the first route is: " + routeTable.GetRoutes()[0].GetDest())
}
