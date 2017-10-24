package main

// Use tcpdump to create a test file
// tcpdump -w test.pcap
// or use the example above for writing pcap files

import (
	"fmt"
	"github.com/google/gopacket"
	"github.com/google/gopacket/pcap"
	"log"
	"os"
)

var (
	handle   *pcap.Handle
	err      error
)

func main() {
	// Open file instead of device
	handle, err = pcap.OpenOffline(os.Args[1])
	if err != nil { log.Fatal(err) }
	defer handle.Close()
	http_count := 0
	
	// Loop through packets in file
	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())
	for packet := range packetSource.Packets() {
		http_count++
		fmt.Println(packet)
	}
}
