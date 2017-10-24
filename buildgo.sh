#!/bin/bash

go get github.com/google/gopacket
go get github.com/google/gopacket/pcap
go get github.com/google/gopacket/layers

go build -o bin/gopkt-task1 src/task1/gopkt.go
