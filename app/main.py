from collections.abc import Hashable
from typing import Any


class Node:
    def __init__(self, key: Hashable, hash_id: int, value: Any) -> None:
        self.key = key
        self.hash_id = hash_id
        self.value = value
        self.length = 0

    def __eq__(self, other: Hashable) -> bool:
        return self.key == other


class Dictionary:
    _EMPTY = object()

    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = int(2 / 3 * self.capacity)
        self.hash_table = [[self._EMPTY] for _ in range(self.capacity)]

    def calculate_hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def resize_dictionary(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.load_factor = int(2 / 3 * self.capacity)
        self.hash_table = [[self._EMPTY] for _ in range(self.capacity)]

        self.length = 0
        for node_list in old_hash_table:
            for node in node_list:
                if node is not self._EMPTY:
                    self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        try:
            hash(key)
        except TypeError:
            raise TypeError("The key must be hashable.")

        index = self.calculate_hash(key)
        current_node = Node(key, index, value)

        for position, node in enumerate(self.hash_table[index]):
            if node is not self._EMPTY and node.key == key:
                self.hash_table[index][position] = current_node
                return
        else:
            if self.length + 1 > self.load_factor:
                self.resize_dictionary()
                index = self.calculate_hash(key)
                current_node = Node(key, index, value)

            for position, node in enumerate(self.hash_table[index]):
                if node is self._EMPTY:
                    self.hash_table[index][position] = current_node
                    break
            else:
                self.hash_table[index].append(current_node)
            self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self.calculate_hash(key)
        for node in self.hash_table[index]:
            if node is not self._EMPTY and node.key == key:
                return node.value
        raise KeyError("The key doesn't exist.")

    def __len__(self) -> int:
        return self.length
