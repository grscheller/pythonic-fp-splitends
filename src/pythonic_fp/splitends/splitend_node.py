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

"""Node class used to make inwardly directed bush-like graphs."""

from collections.abc import Callable, Iterator
from typing import cast
from pythonic_fp.fptools.maybe import MayBe
from pythonic_fp.sentinels.flavored import Sentinel

__all__ = ['SENode']

type _Sentinel = Sentinel[tuple[str, str, str, str]]
_sentinel: _Sentinel = Sentinel(('split', 'end', 'node', 'private'))


class SENode[D]:
    """Used by class SplitEnd as a hidden implementation detail.

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

    __slots__ = '_data', '_prev'

    def __init__(self, data: D, prev: 'SENode[D] | _Sentinel' = _sentinel) -> None:
        """
        :param data: Nodes always contain data of type ``D``.
        :param prev: optional link to a previous node
        """
        self._data = data
        if prev is not _sentinel:
            self._prev = MayBe(prev)
        else:
            self._prev = MayBe()

    def __iter__(self) -> Iterator[D]:
        node = self
        while node:
            yield node._data
            node = cast(SENode[D], node._prev.get())
        yield node._data

    def __bool__(self) -> bool:
        return self._prev != MayBe()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self._prev != other._prev:
            return False
        if self._data == other._data:
            return True
        return False

    def peak_data(self) -> D:
        """Peak at data.

        :returns: The data stored in the ``SENode``.
        """
        return self._data

    def peak_prev(self) -> 'SENode[D]':
        """Peak at previous node.

        :returns: Reference to previous node stored in the ``SENode``.
        """
        if self:
            return self._prev.get()
        return self

    def peak2(self) -> 'tuple[D, SENode[D]]':
        """Peak at data and previous node, if a root then data and self.

        :returns: tuple of type tuple[D, SENode[D]]
        """
        if self._prev:
            return self._data, self._prev.get()
        return self._data, self

    def push(self, data: D) -> 'SENode[D]':
        """Create a new ``SENode``.

        :param data: Data for new node to contain.
        :returns: New ``SENode`` whose previous node is the current node.
        """
        return SENode(data, self)

    def fold[T](self, f: Callable[[T, D], T], init: T | None = None) -> T:
        """Fold data across linked nodes with a function..

        :param f: Folding function, first argument is for accumulated value.`
        :param init: Optional initial starting value for the fold.
        :returns: Reduced value folding from end to root in natural LIFO order.
        """
        if init is None:
            acc: T = cast(T, self._data)
            node = self._prev.get()
        else:
            acc = init
            node = self

        while node:
            acc = f(acc, node._data)
            node = node._prev.get()
        acc = f(acc, node._data)
        return acc
