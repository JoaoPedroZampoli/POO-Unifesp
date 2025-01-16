class Solution:
    def isValid(self, s: str) -> bool:
        Pilha = []

        for i in range (len(s)):
            if s[i] in "([{":
                Pilha.append(s[i])
            elif s[i] in ")]}":
                if not Pilha or (s[i] == ")" and Pilha[-1] != "(") or (s[i] == "}" and Pilha[-1] != "{") or (s[i] == "]" and Pilha[-1] != "["):
                    return False
                Pilha.pop()
            else:
                return False
        return not Pilha
                