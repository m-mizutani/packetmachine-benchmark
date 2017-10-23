#include<iostream>
#include <tins/tins.h>
#include <tins/tcp_ip/stream_follower.h>
#include "ticker.hpp"

static size_t ssn_count(0);

void on_new_connection(Tins::TCPIP::Stream::Stream& stream) {
  ssn_count++;
}

int main(int argc, char* argv[]) {
  Tins::TCPIP::StreamFollower follower;
  follower.new_stream_callback(&on_new_connection);
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
