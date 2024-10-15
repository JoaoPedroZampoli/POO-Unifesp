def TwoSum(Nums, Target):
    TamVet = len(Nums)
    for i in range(TamVet):
        for j in range(i+1, TamVet):
            if Nums[i] + Nums[j] == Target:
                print([i, j])
                return

Nums = [2, 7, 11, 15]
Target = 9
TwoSum(Nums, Target)

Nums = [3, 2, 4]
Target = 6
TwoSum(Nums, Target)

Nums = [3, 3]
Target = 6
TwoSum(Nums, Target)