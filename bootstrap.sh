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

if [ ! -e $DATA_DIR/lbnl.anon-ftp.Jan10-19.2003.tcpdump ]; then
    wget ftp://ita.ee.lbl.gov/new/lbnl.anon-ftp.Jan10-19.2003.tcpdump.gz -O $DATA_DIR/lbnl.anon-ftp.Jan10-19.2003.tcpdump.gz
		gunzip $DATA_DIR/lbnl.anon-ftp.Jan10-19.2003.tcpdump.gz
fi

rm -f test_data_path.txt 
echo $DATA_DIR/maccdc2012_00000.pcap               >> test_data_path.txt
echo $DATA_DIR/lbnl.anon-ftp.Jan10-19.2003.tcpdump >> test_data_path.txt
