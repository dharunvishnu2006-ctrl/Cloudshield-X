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


class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """A self-balancing BST using rotations to stay close to O(log n)."""

    def __init__(self):
        self.root = None

    def _height(self, node) -> int:
        return node.height if node else 0

    def _balance_factor(self, node) -> int:
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_left(self, z):
        """Fix a right-heavy imbalance by rotating left."""
        y = z.right
        t2 = y.left

        y.left = z
        z.right = t2

        self._update_height(z)
        self._update_height(y)
        return y

    def _rotate_right(self, y):
        """Fix a left-heavy imbalance by rotating right."""
        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        self._update_height(y)
        self._update_height(x)
        return x

    def insert(self, value) -> None:
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if node is None:
            return AVLNode(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        else:
            node.right = self._insert_recursive(node.right, value)

        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)

        if balance < -1 and value >= node.right.value:
            return self._rotate_left(node)

        if balance > 1 and value >= node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def height(self) -> int:
        return self._height(self.root)
