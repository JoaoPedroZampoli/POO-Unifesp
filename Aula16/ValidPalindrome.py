class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = "".join(c.lower() for c in s if c.isalnum())
        print(s)

        esq = 0
        dir = len(s) - 1

        while esq < dir:
            if s[esq] != s[dir]:
                return False
            esq += 1
            dir -= 1
        return True