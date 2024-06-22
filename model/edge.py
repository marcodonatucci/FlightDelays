from dataclasses import dataclass
from model.airport import Airport


@dataclass
class Edge:
    airport1: Airport
    airport2: Airport
    weight: int


