#!/bin/bash

go get github.com/google/gopacket
go get github.com/google/gopacket/pcap
go get github.com/google/gopacket/layers

go build -o bin/gopkt-task1 src/task1/gopkt.go
go build -o bin/gopkt-task3 src/task3/gopkt.go
