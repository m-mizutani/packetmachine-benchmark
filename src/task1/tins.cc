#include <iostream>
#include <tins/tins.h>
#include <tins/tcp_ip/stream_follower.h>
#include "../ticker.hpp"

static size_t http_count(0);

bool callback(const Tins::PDU &pdu) {
  // Find the TCP layer
  const Tins::TCP &tcp = pdu.rfind_pdu<Tins::TCP>();
  if (tcp.dport() == 80 || tcp.sport() == 80) {
    http_count++;
  }
  return true;
}


int main(int argc, char* argv[]) {
  auto sniffer = Tins::FileSniffer(argv[1]);
  
  {
    Ticker t;
    sniffer.sniff_loop(callback);
  }

  return 0;
}
