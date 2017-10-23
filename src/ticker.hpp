#include <chrono>
#include <iostream>

class Ticker {
 private:
  std::chrono::system_clock::time_point start_, end_;
 public:
  Ticker() {
    this->start_ = std::chrono::system_clock::now();
  }
  ~Ticker() {
    this->end_ = std::chrono::system_clock::now();
    std::cout << std::chrono::duration_cast<std::chrono::microseconds>(this->end_ - this->start_).count() << std::endl;
  }
};
