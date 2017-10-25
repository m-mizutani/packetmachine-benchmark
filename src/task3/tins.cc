#include <iostream>
#include <tins/tins.h>
#include <tins/tcp_ip/stream_follower.h>
#include "../ticker.hpp"

static size_t google_count(0);

bool callback(const Tins::PDU &pdu) {
  Tins::DNS dns = pdu.rfind_pdu<Tins::RawPDU>().to<Tins::DNS>();

  // Retrieve the queries and print the domain name:
  for (const auto& query : dns.queries()) {
    if (query.dname().find(".google.") != std::string::npos) {
      google_count++;
    }
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
