#include <string>
#include <vector>
#include <algorithm>
using namespace std;

class DFA {
  // states
  enum {
    START = 0,
    SIGNED = 1,
    NUMBER = 2,
    END = 3
  };
  vector<vector<int>> table = {
    {START, SIGNED, NUMBER, END}, // for START 
    {END, END, NUMBER, END},      // for SIGNED
    {END, END, NUMBER, END},      // for NUMBER
    {END, END, END, END}          // for END
  };
  int getCol(char c) {
    if(c == ' ')
      return 0;
    else if(c == '+' || c == '-')
      return 1;
    else if('0' <= c && c <= '9')
      return 2;
    else
      return 3;
  }

  int state = START;
  int sign = 1;
  long long ans = 0;
public:
  void getNext(char c) {
    // get the next state
    state = table[state][getCol(c)];
    // action of state transition
    if(state == NUMBER) {
      ans = ans * 10 + c - '0';
      ans = sign == 1 ? min(ans, (long long)INT_MAX) : min(ans, -(long long)INT_MIN);
    } else if(state == SIGNED) {
      sign = c == '+' ? 1 : -1;
    }
  }
  // get the output of DFA
  int getOut() {
    return sign * ans;
  }
};

class Solution {
public:
  int myAtoi(string &s) {
    DFA dfa;
    for(auto &c : s)
      dfa.getNext(c);
    return dfa.getOut();
  }
};