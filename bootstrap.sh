#!/bin/bash

if [ -z $1 ]; then
    DATA_DIR="data"
else
    DATA_DIR=$1
fi

mkdir -p $DATA_DIR

if [ ! -e $DATA_DIR/maccdc2012_00000.pcap ]; then
    curl https://download.netresec.com/pcap/maccdc-2012/maccdc2012_00000.pcap.gz \
	 -o $DATA_DIR/maccdc2012_00000.pcap.gz
    gunzip $DATA_DIR/maccdc2012_00000.pcap.gz
fi

echo $DATA_DIR/maccdc2012_00000.pcap > test_data_path.txt

