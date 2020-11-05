//force - mine, similar to leetcode solution 2 - sliding windows, [l,r)
class Solution {
public:
    int lengthOfLongestSubstring(std::string &s) {
    	if(s.size() < 2)
    		return s.size();
		int ans = 0,l = 0,r = 0;
		for(r = 1;r < s.size();++r) {
			//judge: ∃ i ∈ [l,r), s[i] == s[r]
			int i;
			for(i = l;i < r;++i)
				if(s[i] == s[r])
					break;
			if(i == r)
				continue;
			ans = std::max(ans,r - l);
			l = i + 1;//not ++l
		}
    	return max(ans,r-l);
    }
};

//using map to speed up finding
#include <map>
class Solution {
public:
    int lengthOfLongestSubstring(std::string &s) {
    	if(s.size() < 2)
    		return s.size();
    	std::map<char,int> val2pos;
		int ans = 0,l = 0,r = 0;//[l,r]
		for(;r < s.size(); ++r) {
			auto iter = val2pos.find(s[r]);
			if(iter != val2pos.end())
				l = std::max(iter->second + 1, l);//the reason why we use max is that we don't earse the element before the duplicated element
			ans = std::max(ans, r - l + 1);
			val2pos[s[r]] = r;
		}
    	return ans;
    }
};


//using vector to replace map
#include <map>
class Solution {
public:
    int lengthOfLongestSubstring(std::string &s) {
    	if(s.size() < 2)
    		return s.size();
    	std::vector<int> val2pos(128,-1);
		int ans = 0,l = 0,r = 0;//[l,r]
		for(;r < s.size(); ++r) {
			l = std::max(val2pos[s[r]] + 1, l);//the reason why we use max is that we don't earse the element before the duplicated element
			ans = std::max(ans, r - l + 1);
			val2pos[s[r]] = r;
		}
    	return ans;
    }
};

//improve above
#include <map>
class Solution {
public:
    int lengthOfLongestSubstring(std::string &s) {
    	if(s.size() < 2)
    		return s.size();
    	std::vector<int> val2pos(128,0);//not real position
		int ans = 0,l = 0,r = 0;//[l,r]
		for(;r < s.size(); ++r) {
			l = std::max(val2pos[s[r]], l);//the reason why we use max is that we don't earse the element before the duplicated element
			ans = std::max(ans, r - l + 1);
			val2pos[s[r]] = r + 1;
		}
    	return ans;
    }
};