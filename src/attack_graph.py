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

    def dijkstra(self, start: str, end: str) -> tuple:
        """Find the cheapest-cost path from start to end."""
        import heapq

        distances = {start: 0.0}
        previous: dict = {}
        visited = set()
        heap = [(0.0, start)]

        while heap:
            current_dist, current = heapq.heappop(heap)

            if current in visited:
                continue
            visited.add(current)

            if current == end:
                break

            for neighbor, weight in self.neighbors(current):
                new_dist = current_dist + weight
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(heap, (new_dist, neighbor))

        if end not in distances:
            return [], float("inf")

        path = []
        node = end
        while node != start:
            path.append(node)
            node = previous[node]
        path.append(start)
        path.reverse()

        return path, distances[end]

    def bellman_ford(self, start: str) -> tuple:
        """Find cheapest distances from start, handling negative weights.
        Returns (distances, has_negative_cycle)."""
        all_hosts = list(self.adjacency.keys())
        distances = {host: float("inf") for host in all_hosts}
        distances[start] = 0.0

        for _ in range(len(all_hosts) - 1):
            for host in all_hosts:
                if distances[host] == float("inf"):
                    continue
                for neighbor, weight in self.neighbors(host):
                    new_dist = distances[host] + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist

        has_negative_cycle = False
        for host in all_hosts:
            if distances[host] == float("inf"):
                continue
            for neighbor, weight in self.neighbors(host):
                if distances[host] + weight < distances[neighbor]:
                    has_negative_cycle = True

        return distances, has_negative_cycle

    def floyd_warshall(self) -> dict:
        """Return all-pairs shortest distances between every host."""
        hosts = list(self.adjacency.keys())
        dist = {i: {j: float("inf") for j in hosts} for i in hosts}

        for host in hosts:
            dist[host][host] = 0.0

        for host in hosts:
            for neighbor, weight in self.neighbors(host):
                dist[host][neighbor] = weight

        for k in hosts:
            for i in hosts:
                for j in hosts:
                    through_k = dist[i][k] + dist[k][j]
                    if through_k < dist[i][j]:
                        dist[i][j] = through_k

        return dist


class UnionFind:
    """Disjoint Set Union - groups hosts into connected segments."""

    def __init__(self):
        self.parent: dict = {}

    def make_set(self, host: str) -> None:
        """Register a new host as its own segment, if not already known."""
        if host not in self.parent:
            self.parent[host] = host

    def find(self, host: str) -> str:
        """Find the root of host's segment, with path compression."""
        self.make_set(host)
        if self.parent[host] != host:
            self.parent[host] = self.find(self.parent[host])
        return self.parent[host]

    def union(self, a: str, b: str) -> None:
        """Merge the segments containing a and b."""
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a != root_b:
            self.parent[root_a] = root_b

    def connected(self, a: str, b: str) -> bool:
        """Return True if a and b are in the same segment."""
        return self.find(a) == self.find(b)
