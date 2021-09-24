import collections
import bisect


class TimeMap:
    # https://leetcode.com/problems/time-based-key-value-store/discuss/247130/Python-concise-6-liner
    # two dict solution
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.times = collections.defaultdict(list)
        self.values = collections.defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times[key].append(timestamp)
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        i = bisect.bisect(self.times[key], timestamp)
        return self.values[key][i - 1] if i else ''

class TimeMap2:
    # one dict with list in it
    # cost little bit more than the two dict one?
    def __init__(self):
        self.d = {}
            
    def set(self, key, value, timestamp):
        self.d.setdefault(key, []).append([timestamp, value])
            
    def get(self, key, timestamp):
        v = self.d.get(key, [])
        # chr(ord('z')+1) = '{' the first character after all letters and digits
        i = bisect.bisect_right(v, [timestamp, chr(ord('z')+1)])
        return v[i-1][1] if i else ''

# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)