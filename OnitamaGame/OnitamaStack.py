"""
This is the stack class that will come handy in the OnitamaGame file.
"""
from typing import Any


class OnitamaStack:
    """
    A class that implements the stack ADT. Used in the undo function of the
    OnitamaGame.

    Private Attribute:

    _items: the list that contains the board and the styles.
    """
    _items: list

    def __init__(self) -> None:
        """
        Initializes the OnitamaStack.
        """
        self._items = []

    def empty(self) -> bool:
        """
        Checks whether if the stack is empty or not.
        """
        return self._items == []

    def push(self, n: Any) -> None:
        """
        Pushes the item into the stack.
        """
        self._items.append(n)

    def pop(self) -> Any:
        """
        Pops the the item at the top of the stack.
        """
        if not self.empty():
            return self._items.pop()
