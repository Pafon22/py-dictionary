from collections.abc import Hashable
from typing import Any


class Dictionary:
    _EMPTY = object()

    def __init__(self) -> None:
        self.capacity = 8
        self.keys = [self._EMPTY] * self.capacity
        self.values = [None] * self.capacity
        self.load_factor = int(2 / 3 * self.capacity)

    def resize_dictionary(self) -> None:
        self.capacity *= 2
        self.load_factor = int(2 / 3 * self.capacity)
        new_keys = [self._EMPTY] * self.capacity
        new_values = [None] * self.capacity

        for index, key in enumerate(self.keys):
            new_keys[index] = key
            new_values[index] = self.values[index]
        self.keys = new_keys
        self.values = new_values

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if isinstance(key, Hashable):
            if key in self.keys:
                index = self.keys.index(key)
                self.keys[index] = key
                self.values[index] = value
            else:
                if self.__len__() + 1 > self.load_factor:
                    self.resize_dictionary()

                for index, original_key in enumerate(self.keys):
                    if original_key is self._EMPTY:
                        self.keys[index] = key
                        self.values[index] = value
                        break
        else:
            raise TypeError("The key must be hashable.")

    def __getitem__(self, key: Hashable) -> list:
        if key in self.keys:
            return self.values[self.keys.index(key)]
        raise KeyError("The key doesn't exist.")

    def __len__(self) -> int:
        count = 0
        for key in self.keys:
            if key is not self._EMPTY:
                count += 1
        return count
