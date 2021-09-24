import heapq
from typing import List
class Solution:
    def minRefuelStops(self, target: int, startFuel: int, stations: List[List[int]]) -> int:
        tank = startFuel
        # A heap storingg the gas in the station that has passed
        # The value in it will be negative because the heappop will pop smallest value first
        # And we want the maximum value at the same time
        pq = []  
        # treat the target as the last gas station
        stations.append((target, float('inf')))

        # ans: refuel times
        # prev: distance between start point to previous station
        ans = prev = 0
        # location: miles away from start point to this station
        # capacity: gas in this station
        for location, capacity in stations:
            # gas remain in the tank minus the distance between two station
            tank -= location - prev
            while len(pq) and (tank < 0):  # must refuel in past
                tank += -heapq.heappop(pq)
                ans += 1
            if tank < 0: return -1
            heapq.heappush(pq, -capacity)
            prev = location

        return ans