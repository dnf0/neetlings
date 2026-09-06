"""Best Time to Buy and Sell Stock.

You are given an array prices where prices[i] is the price of a given stock on the ith day.
You want to maximize your profit by choosing a single day to buy one stock and choosing a
different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Examples:
    1. Input: prices = [7,1,5,3,6,4]
       Output: 5
       Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
    2. Input: prices = [7,6,4,3,1]
       Output: 0
       Explanation: In this case, no transactions are done and the max profit = 0.

Constraints:
    - 1 <= prices.length <= 10^5
    - 0 <= prices[i] <= 10^4

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""

class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {"input": ([7, 1, 5, 3, 6, 4],), "expected": 5, "name": "example1"},
    {"input": ([7, 6, 4, 3, 1],), "expected": 0, "name": "example2"},
    {"input": ([1, 2],), "expected": 1, "name": "example3"},
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.maxProfit(*case["input"]) == case["expected"]
