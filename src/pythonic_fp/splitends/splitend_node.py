# Copyright 2023-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
SENode
======

**Used to make inwardly directed bush-like graphs.**

- designed so multiple splitends can safely share the same data
- nodes always contain data
- data node ``SENode[D]`` make up end-to-root singularly linked lists
- two nodes compare as equal if
    - both their previous Nodes are the same
    - their data compare as equal
- a root node whose previous node is itself
    - root nodes mark ends of lists
- more than one node can point to the same proceeding node
    - forming bush like graphs

"""

from collections.abc import Callable, Iterator
from typing import cast, Final, overload, Self
from pythonic_fp.sentinels.flavored import Sentinel

__all__ = ['SENode']

type _secret = tuple[str, str, str, str]
type _Sentinel = Sentinel[_secret]
_sentinel: Final[_Sentinel] = Sentinel(('split', 'end', 'node', 'private'))


class SENode[D]:
    __slots__ = '_data', '_prev'

    def __init__(self, data: D, prev: Self | _Sentinel = _sentinel) -> None:
        """
        :param data: Nodes always contain data of type ``D``.
        :param prev: Link to previous node. Points to ``self`` if a root node.
        """
        self._data = data
        if prev is not _sentinel:
            self._prev = cast(Self, prev)
        else:
            self._prev = self

    def __bool__(self) -> bool:
        return self._prev is not self

    def __iter__(self) -> Iterator[D]:
        node = self
        while node:
            yield node._data
            node = node._prev
        yield node._data

    def __eq__(self, other: object) -> bool:
        """
        Two ``SENodes`` nodes are equal if their previous nodes are the
        same object and their data compare as equal.
        """
        if not isinstance(other, type(self)):
            return False

        if self._prev is not other._prev:
            return False
        if self._data == other._data:
            return True
        return False

    def peak_data(self) -> D:
        """Peak at data.

        :returns: The data stored in the ``SENode``.
        """
        return self._data

    def peak_prev(self) -> Self:
        """Peak at previous node.

        :returns: The previous node stored in the ``SENode``.
        """
        if self:
            return self._prev
        return self

    def peak2(self) -> tuple[D, Self]:
        """Peak at data and previous node, if a root then data and self.

        :returns: tuple of type tuple[D, SENode[D]]
        """
        if self:
            return self._data, self._prev
        return self._data, self

    def push(self, data: D) -> Self:
        """Create a new ``SENode[D]``.

        :param data: Data for new node to contain.
        :returns: New ``SENode`` whose previous node is the current node.
        """
        return cast(Self, SENode(data, self))

    @overload
    def fold(self, f: Callable[[D, D], D]) -> D: ...
    @overload
    def fold[T](self, f: Callable[[T, D], T], init: T) -> T: ...

    def fold[T](self, f: Callable[[T, D], T], init: T | _Sentinel = _sentinel) -> T:
        """Fold data across linked nodes with a function..

        :param f: Folding function, first argument is for accumulated value.`
        :param init: Optional initial starting value for the fold.
        :returns: Reduced value folded from end to root in natural LIFO order.
        """
        if init is not _sentinel:
            acc = cast(T, init)
            node = self
        else:
            acc = cast(T, self._data)  # in this case T = D
            node = self._prev

        while node:
            acc = f(acc, node._data)
            node = node._prev
        acc = f(acc, node._data)
        return acc
