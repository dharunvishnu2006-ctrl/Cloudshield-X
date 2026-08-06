class LRUNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """A cache with O(1) lookup and O(1) move-to-front, using a dict
    + doubly linked list."""

    def __init__(self, capacity: int = 500):
        self.capacity = capacity
        self.lookup: dict = {}
        self.head = LRUNode(None, None)
        self.tail = LRUNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.hits = 0
        self.misses = 0

    def _remove(self, node: LRUNode) -> None:
        """Unlink a node from wherever it currently sits."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_front(self, node: LRUNode) -> None:
        """Insert a node right after head - the 'most recently used' position."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """Look up a key. If found, move it to the front (most recently used)."""
        if key not in self.lookup:
            self.misses += 1
            return None

        self.hits += 1
        node = self.lookup[key]
        self._remove(node)
        self._insert_at_front(node)
        return node.value

    def put(self, key, value) -> None:
        """Add or update a key. Evict the oldest entry if over capacity."""
        if key in self.lookup:
            node = self.lookup[key]
            node.value = value
            self._remove(node)
            self._insert_at_front(node)
            return

        if len(self.lookup) >= self.capacity:
            oldest = self.tail.prev
            self._remove(oldest)
            del self.lookup[oldest.key]

        new_node = LRUNode(key, value)
        self.lookup[key] = new_node
        self._insert_at_front(new_node)
