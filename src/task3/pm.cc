#include<iostream>
#include<packetmachine.hpp>
#include "../ticker.hpp"

int main(int argc, char* argv[]) {
  int google_count = 0;

  pm::Config config;
  config.set_false("TCP.enable_session_mgmt");

  auto m = pm::Machine(config);
  m.add_pcapfile(argv[1]);

  auto q_key = m.lookup_param_key("DNS.question");
  m.on("DNS", [&](const pm::Property& p) {
      const auto& vals = p.value(q_key);
      if (vals.is_array()) {
        for (size_t idx = 0; idx < vals.size(); idx++) {
          const auto& v = vals.get(idx);
          auto s = v.find("name").repr();

          if (s.find(".google.") != std::string::npos) {
            google_count++;
          }
        }
      }
    });
  
  {
    Ticker t;
    m.loop();
  }

  return 0;
}
