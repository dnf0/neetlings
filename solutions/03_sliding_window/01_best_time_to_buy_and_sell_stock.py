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

HINTS = [
    "Use a sliding window or keep track of the minimum price seen so far.",
    "Initialize min_price to infinity and max_profit to 0.",
    "For each price, update min_price with the minimum of min_price and the current price.",
    "Calculate the potential profit if we sell today (price - min_price) and update max_profit with the max of max_profit and this potential profit.",
]


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        if not prices:
            return 0
        min_price = prices[0]
        max_profit = 0
        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price
        return max_profit


TEST_CASES = [
    {"input": ([7, 1, 5, 3, 6, 4],), "expected": 5, "name": "example1"},
    {"input": ([7, 6, 4, 3, 1],), "expected": 0, "name": "example2"},
    {"input": ([1, 2],), "expected": 1, "name": "example3"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.maxProfit(*case["input"]) == case["expected"]
