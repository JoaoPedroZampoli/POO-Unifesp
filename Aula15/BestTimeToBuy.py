class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        gain = 0
        buy = prices[0]
        for i in range(1, len(prices)):
            if prices[i] < buy:
                buy = prices[i]
            elif prices[i] - buy > gain:
                gain = prices[i] - buy
        return gain
        #print(prices)
        