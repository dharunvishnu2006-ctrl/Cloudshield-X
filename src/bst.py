class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    """A plain binary search tree - no self-balancing."""

    def __init__(self):
        self.root = None

    def insert(self, value) -> None:
        if self.root is None:
            self.root = BSTNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node: BSTNode, value) -> None:
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = BSTNode(value)
            else:
                self._insert_recursive(node.right, value)

    def height(self) -> int:
        """Return the height of the tree - how many levels deep."""
        return self._height_recursive(self.root)

    def _height_recursive(self, node) -> int:
        if node is None:
            return 0
        return 1 + max(
            self._height_recursive(node.left), self._height_recursive(node.right)
        )
