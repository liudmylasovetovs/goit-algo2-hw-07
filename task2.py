from functools import lru_cache
from timeit import timeit
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, node):
        while node.parent:
            if node.parent.parent is None:  
                if node == node.parent.left:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left and node.parent == node.parent.parent.left:  
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.right:  
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_left(self, node):
        right = node.right
        if right:
            node.right = right.left
            if right.left:
                right.left.parent = node
            right.parent = node.parent
        if not node.parent:
            self.root = right
        elif node == node.parent.left:
            node.parent.left = right
        else:
            node.parent.right = right
        if right:
            right.left = node
            node.parent = right

    def _rotate_right(self, node):
        left = node.left
        if left:
            node.left = left.right
            if left.right:
                left.right.parent = node
            left.parent = node.parent
        if not node.parent:
            self.root = left
        elif node == node.parent.left:
            node.parent.left = left
        else:
            node.parent.right = left
        if left:
            left.right = node
            node.parent = left

    def insert(self, key, value):
        if not self.root:
            self.root = Node(key, value)
            return
        node = self.root
        while True:
            if key < node.key:
                if node.left:
                    node = node.left
                else:
                    node.left = Node(key, value)
                    node.left.parent = node
                    self._splay(node.left)
                    return
            elif key > node.key:
                if node.right:
                    node = node.right
                else:
                    node.right = Node(key, value)
                    node.right.parent = node
                    self._splay(node.right)
                    return
            else:
                return  

    def search(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return node.value
        return None

def fibonacci_splay(n, tree):
    cached = tree.search(n)
    if cached is not None:
        return cached
    if n <= 1:
        return n
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result

def measure_time():
    tree = SplayTree()
    ns = list(range(0, 951, 50))
    lru_times = []
    splay_times = []
    for n in ns:
        lru_time = timeit(lambda: fibonacci_lru(n), number=10) / 10
        splay_time = timeit(lambda: fibonacci_splay(n, tree), number=10) / 10
        lru_times.append(lru_time)
        splay_times.append(splay_time)
    return ns, lru_times, splay_times

def print_table(ns, lru_times, splay_times):
    table = Table(title="Порівняння часу виконання для LRU Cache та Splay Tree")
    table.add_column("n", justify="right")
    table.add_column("LRU Cache Time (s)", justify="right")
    table.add_column("Splay Tree Time (s)", justify="right")
    for n, lru_time, splay_time in zip(ns, lru_times, splay_times):
        table.add_row(str(n), f"{lru_time:.8f}", f"{splay_time:.8f}")
    console = Console()
    console.print(table)

def show_plot(ns, lru_times, splay_times):
    plt.figure(figsize=(10, 5))
    plt.plot(ns, lru_times, marker='o', label="LRU Cache")
    plt.plot(ns, splay_times, marker='s', label="Splay Tree")
    plt.xlabel("Число Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    ns, lru_times, splay_times = measure_time()
    print_table(ns, lru_times, splay_times)
    show_plot(ns, lru_times, splay_times)