class AttackGraph:
    """A graph of hosts and their connections, using an adjacency list."""

    def __init__(self):
        self.adjacency: dict = {}

    def add_edge(self, src: str, dst: str, weight: float = 1.0) -> None:
        """Add a directed connection from src to dst, with an optional weight."""
        if src not in self.adjacency:
            self.adjacency[src] = []
        if dst not in self.adjacency:
            self.adjacency[dst] = []
        self.adjacency[src].append((dst, weight))

    def neighbors(self, host: str) -> list:
        """Return all hosts directly reachable from this host."""
        return self.adjacency.get(host, [])
