#include<iostream>
#include <tins/tcp_ip/stream.h>
#include <tins/tcp_ip/stream_follower.h>
#include <tins/tins.h>
#include "ticker.hpp"


int main(int argc, char* argv[]) {
  size_t ssn_count(0);
  Tins::TCPIP::StreamFollower follower;
  follower.new_stream_callback([&](Tins::TCPIP::Stream& stream) {
      ssn_count++;
    });
  auto sniffer = Tins::FileSniffer(argv[1]);

  {
    Ticker t;
    sniffer.sniff_loop([&](Tins::Packet& packet) {
        follower.process_packet(packet);
        return true;
      });
  }

  return 0;
}
