#include<iostream>
#include <tins/tins.h>
#include <tins/tcp_ip/stream_follower.h>


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
  Tins::FileSniffer(argv[1]).sniff_loop(callback);
  std::cout << http_count << std::endl;
  return 0;
}
