import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._bestLen = 0
        self._bestComp = []
        self.graph = nx.Graph()
        self.idMap = {}

    def buildGraph(self, min):
        self.graph.clear()
        airports = DAO.getAllAirports(min)
        self.graph.add_nodes_from(airports)
        for node in self.graph.nodes:
            self.idMap[node.ID] = node
        edges = DAO.getAllEdges(min, self.idMap)
        for edge in edges:
            if self.graph.has_edge(edge.airport2, edge.airport1):
                self.graph[edge.airport2][edge.airport1]['weight'] += edge.weight
            else:
                self.graph.add_edge(edge.airport1, edge.airport2, weight=edge.weight)
        return True

    def connessi(self, airport):
        lista = list(self.graph.neighbors(airport))
        result = []
        for nodo in lista:
            result.append((nodo, self.graph[airport][nodo]['weight']))
        result.sort(key=lambda x: x[1],
                         reverse=True)
        return result

    def getGraphDetails(self):
        return f"Grafo creato con {len(self.graph.nodes)} nodi e {len(self.graph.edges)} archi."

    def get_nodes(self):
        return self.graph.nodes

    def getPath(self, maxLen, a0, af):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        self._bestLen = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = [a0]
        self._ricorsionev2(parziale, maxLen, af)
        return self._bestComp

    def _ricorsionev2(self, parziale, maxLen, af):
        # verifico se soluzione è migliore di quella salvata in cache
        if len(parziale) <= maxLen and self._getScore(parziale) > self._bestLen:
            if parziale[-1] == af:
                # se lo è aggiorno i valori migliori
                self._bestComp = copy.deepcopy(parziale)
                self._bestLen = self._getScore(parziale)
        if len(parziale) > maxLen or (parziale[-1] == af and self._getScore(parziale) < self._bestLen):
            return
        # verifico se posso aggiungere un altro elemento
        for a in self.graph.neighbors(parziale[-1]):
            if a not in parziale:
                parziale.append(a)
                self._ricorsionev2(parziale, maxLen, af)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking

    def _getScore(self, nodes):
        score = 0
        for i in range(0, len(nodes)-1):
            score += self.graph[nodes[i]][nodes[i+1]]['weight']
        return score
