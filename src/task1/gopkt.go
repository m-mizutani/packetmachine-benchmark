package main

// Use tcpdump to create a test file
// tcpdump -w test.pcap
// or use the example above for writing pcap files

import (
	"fmt"
	"github.com/google/gopacket"
	"github.com/google/gopacket/pcap"
	"github.com/google/gopacket/layers"
	"log"
	"os"
	"time"
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
	httpCount := 0
	
	// Loop through packets in file
	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())

	startTs := time.Now()
	for packet := range packetSource.Packets() {
		tcpLayer := packet.Layer(layers.LayerTypeTCP)
		if tcpLayer != nil {
			tcp, _ := tcpLayer.(*layers.TCP)
			if tcp.SrcPort == 80 || tcp.DstPort == 80 {
				httpCount++
			}
		}
	}
	endTs := time.Now()
	fmt.Println(endTs.Sub(startTs).Nanoseconds() / 1000)
}
