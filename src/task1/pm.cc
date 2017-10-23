#include <iostream>
#include <packetmachine.hpp>
#include "../ticker.hpp"

int main(int argc, char* argv[]) {
  pm::Config config;
  config.set_false("TCP.enable_session_mgmt");
  auto m = pm::Machine(config);
  m.add_pcapfile(argv[1]);
  int http_count = 0;

  m.on("TCP", [&](const pm::Property& p) {
      if (p.dst_port() == 80 || p.src_port() == 80) {
        http_count++;
      }
    });

  {
    Ticker t;
    m.loop();
  }

  return 0;
}
