#include<iostream>
#include<packetmachine.hpp>
#include "../ticker.hpp"

int main(int argc, char* argv[]) {
  auto m = pm::Machine();
  m.add_pcapfile(argv[1]);
  int ssn_count = 0;

  m.on("TCP.new_session", [&](const pm::Property& p) {
      ssn_count++;
    });
  
  {
    Ticker t;
    m.loop();
  }

  return 0;
}
