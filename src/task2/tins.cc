#include<iostream>
#include <tins/tins.h>
#include <tins/tcp_ip/stream_follower.h>

static size_t ssn_count(0);

void on_new_connection(Tins::TCPIP::Stream::Stream& stream) {
  ssn_count++;
}

int main(int argc, char* argv[]) {
  Tins::TCPIP::StreamFollower follower;
  follower.new_stream_callback(&on_new_connection);
  Tins::FileSniffer(argv[1]).sniff_loop([&](Tins::Packet& packet) {
      follower.process_packet(packet);
      return true;
    });
  std::cout << ssn_count << std::endl;
  return 0;
}
