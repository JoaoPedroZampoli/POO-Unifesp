class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        Linhas = len(image)
        Colunas = len(image[0])
        Cor = image[sr][sc]
        if Cor == color:
            return image
        def DFS(Linha, Coluna): #DepthFirstResearch
            if image[Linha][Coluna] == Cor:
                image[Linha][Coluna] = color
                if Linha >= 1:
                    DFS(Linha-1, Coluna)
                if Linha + 1 < Linhas:
                    DFS(Linha+1, Coluna)
                if Coluna >= 1:
                    DFS(Linha, Coluna-1)
                if Coluna + 1 < Colunas:
                    DFS(Linha, Coluna+1)
        DFS(sr, sc)
        return image

        