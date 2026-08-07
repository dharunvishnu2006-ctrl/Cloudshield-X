from collections import deque


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

    def bfs(self, start: str, max_hops: int = 3) -> dict:
        """Return every host reachable within max_hops, with their hop count."""
        visited = {start: 0}
        queue = deque([start])

        while queue:
            current = queue.popleft()
            current_hops = visited[current]

            if current_hops >= max_hops:
                continue

            for neighbor, _ in self.neighbors(current):
                if neighbor not in visited:
                    visited[neighbor] = current_hops + 1
                    queue.append(neighbor)

        return visited

    def dfs(self, start: str, target: str) -> list:
        """Find one path from start to target using depth-first search."""
        visited = set()
        path: list = []

        def _dfs_helper(current: str) -> bool:
            visited.add(current)
            path.append(current)

            if current == target:
                return True

            for neighbor, _ in self.neighbors(current):
                if neighbor not in visited:
                    if _dfs_helper(neighbor):
                        return True

            path.pop()
            return False

        found = _dfs_helper(start)
        return path if found else []
