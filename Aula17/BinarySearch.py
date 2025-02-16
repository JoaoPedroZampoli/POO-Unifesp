class Solution:
    def search(self, nums: List[int], target: int) -> int:
        Esq = 0
        Dir = len(nums) - 1

        while Esq <= Dir:
            Meio = (Esq + Dir) // 2
            if nums[Meio] == target:
                return Meio
            elif nums[Meio] < target:
                Esq = Meio + 1
            else:
                Dir = Meio - 1
        else:
            return -1