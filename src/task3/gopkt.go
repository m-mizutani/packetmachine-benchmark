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
	"strings"
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
	google_count := 0
	
	// Loop through packets in file
	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())

	startTs := time.Now()
	for packet := range packetSource.Packets() {
		dnsLayer := packet.Layer(layers.LayerTypeDNS)
		if dnsLayer != nil {
			dns, _ := dnsLayer.(*layers.DNS)

			for _, dnsQuestion := range dns.Questions {
				name := string(dnsQuestion.Name)
				if strings.Index(name, ".google.") >= 0 {
					google_count += 1
				}
			}
		}
	}
	endTs := time.Now()
	fmt.Println(endTs.Sub(startTs).Nanoseconds() / 1000)
}
