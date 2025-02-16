class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        OrdenaS = sorted(s)
        OrdenaT = sorted(t)
        return OrdenaS == OrdenaT