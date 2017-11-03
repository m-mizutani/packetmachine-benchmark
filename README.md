packetmachine-benchmark
==================

Benchmark for [PacketMachine](https://github.com/m-mizutani/packetmachine).

Competitors:

- libtins: https://github.com/mfontanini/libtins
- GoPacket: https://github.com/google/gopacket

NOTE: Absolutely, C++ program is faster than GO program in almost cases. But, as you know, processing speed is not the only reason to make a choice of a library for development. I would just like users choose appropriate packet decoding library by the result.

Prerequisite
------------

- Python >= 3.6
    - matplotlib
- Go >= 1.9.1

Setup
------------

Before setup, please set your `$GOPATH`.

```sh
$ git submodule update --init --recursive
$ cmake . && make
$ ./buildgo.sh
```

Run benchmark
-----------

```sh
$ ./benchmark.py
$ ./make_report.py
```

