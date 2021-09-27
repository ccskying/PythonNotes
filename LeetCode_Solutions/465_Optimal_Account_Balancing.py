'''
You are given an array of transactions transactions where transactions[i] = [fromi, toi, amounti] indicates that the person with ID = fromi gave amounti $ to the person with ID = toi.

Return the minimum number of transactions required to settle the debt.

 

Example 1:

Input: transactions = [[0,1,10],[2,0,5]]
Output: 2
Explanation:
Person #0 gave person #1 $10.
Person #2 gave person #0 $5.
Two transactions are needed. One way to settle the debt is person #1 pays person #0 and #2 $5 each.
Example 2:

Input: transactions = [[0,1,10],[1,0,1],[1,2,5],[2,0,5]]
Output: 1
Explanation:
Person #0 gave person #1 $10.
Person #1 gave person #0 $1.
Person #1 gave person #2 $5.
Person #2 gave person #0 $5.
Therefore, person #1 only need to give person #0 $4, and all debt is settled.
 

Constraints:

1 <= transactions.length <= 8
transactions[i].length == 3
0 <= fromi, toi <= 20
fromi != toi
1 <= amounti <= 100
'''


import collections
from typing import List

class Solution:
    def minTransfers(self, transactions: List[List[int]]) -> int:
        # greedy approche, only keep the person debt is not 0
        counter = collections.Counter()
        for f, t, m in transactions:
            counter[f] -= m
            counter[t] += m
        balances = list(counter.values())
        
        # function used for further calculation
        def dfs(b):
            if not b:   # base case
                return 0

            if not b[0]:   #skip ppl whose balance==0 
                return dfs(b[1:])

            minTrans = float('inf')
            for i in range(1, len(b)):
                if b[i] == -b[0]:   # greedy shortcut 
                    return 1 + dfs(b[1:i] + [0] + b[i+1:])

                elif b[i] * b[0] < 0: 
                    minTrans = min(minTrans, dfs(b[1:i] + [b[i]+b[0]] + b[i+1:])) 

            return minTrans + 1  

        return dfs(balances)