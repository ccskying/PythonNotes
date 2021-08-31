import collections
import  heapq
'''
For every turn, find the node with less delay and loop all the node current position can reach
The status of current node will be set as true in seen[]
The reachable node will have a delay value in dist[]
In every turn, the value in seen[] of the current node will be set as True
the value in dist[] of the reachable node from current node will be given at the end of the loop

if seen[i] = true, this position has been calculated, ignore
if dist[i] = 'inf', this position is unreachable for now
if all reachable node has been calculated, no new node will have dist value with false in seen[]
'''
class Solution(object):
    def networkDelayTime(self, times, N, K):
        # convert list to gargh
        # for each node u, v is the node it can reach with time w
        graph = collections.defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        # N node plus a zero point that won't be used here
        # create list to store distance [use range() in python3]
        dist = {node: float('inf') for node in xrange(1, N+1)}
        # tag the nodes that has been calculated
        seen = [False] * (N+1)
        # tag the starting node
        dist[K] = 0

        while True:
            cand_node = -1
            cand_dist = float('inf')
            # find the reachable node with miminum delay.
            for i in xrange(1, N+1):
                if not seen[i] and dist[i] < cand_dist:
                    cand_dist = dist[i]
                    cand_node = i
            # if all reachable node has been calculated, break
            if cand_node < 0: break
            # current node calculated
            seen[cand_node] = True
            # set delay time for reachable nodes from this position
            for nei, d in graph[cand_node]:
                dist[nei] = min(dist[nei], dist[cand_node] + d)
        # calculate the maximum delay of this network graph
        ans = max(dist.values())
        # if ans is 'inf', it means some node is unreachable, return -1
        return ans if ans < float('inf') else -1

    # Heap Implementation
    def networkDelayTime_H(self, times, N, K):
        graph = collections.defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        pq = [(0, K)]
        dist = {}
        while pq:
            d, node = heapq.heappop(pq)
            if node in dist: continue
            dist[node] = d
            for nei, d2 in graph[node]:
                if nei not in dist:
                    heapq.heappush(pq, (d+d2, nei))

        return max(dist.values()) if len(dist) == N else -1