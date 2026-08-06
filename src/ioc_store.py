class IOCStore:
    """A hash table you build yourself: buckets, hash function, chaining."""

    def __init__(self, num_buckets: int = 128):
        self.num_buckets = num_buckets
        self.buckets: list[list[str]] = [[] for _ in range(num_buckets)]

    def _hash(self, key: str) -> int:
        """Turn a string key into a bucket index."""
        total = sum(ord(ch) for ch in key)
        return total % self.num_buckets

    def add(self, key: str) -> None:
        """Add a key to the store, using chaining to handle collisions."""
        idx = self._hash(key)
        if key not in self.buckets[idx]:
            self.buckets[idx].append(key)

    def is_blocked(self, key: str) -> bool:
        """Check if a key exists in the store, O(1) average."""
        idx = self._hash(key)
        return key in self.buckets[idx]


def compare_feeds(feed_a: set, feed_b: set) -> dict:
    """Compare two threat feeds using set operations."""
    return {
        "agreed": feed_a & feed_b,
        "only_in_a": feed_a - feed_b,
        "only_in_b": feed_b - feed_a,
    }
