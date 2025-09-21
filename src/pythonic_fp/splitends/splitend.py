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
SplitEnds
=========

**LIFO stacks safely sharing immutable data.**

- each ``SplitEnd`` is a very simple stateful (mutable) LIFO stack
- data can be either "extended" to or "snipped" off the "end" 
- the "root" of a ``SplitEnd``
  - it is fixed and cannot be removed from the ``SplitEnd``
- different mutable split ends can safely share the same "tail"
- each ``SplitEnd`` sees itself as a singularly linked list
- bush-like datastructures can be formed using multiple ``SplitEnds``
- the ``SplitEnd.split`` and ``len`` methods are O(1)
- in boolean context returns true if the ``SplitEnd`` is not just its "root"

"""

from collections.abc import Callable, Iterator
from pythonic_fp.iterables.folding import reduce_left, fold_left
from typing import cast, Final, overload
from pythonic_fp.queues.lifo import LIFOQueue
from pythonic_fp.sentinels.flavored import Sentinel
from .splitend_node import SENode

__all__ = ['SplitEnd']

type _SecretType = tuple[str, str, str]
_secret_value: Final[_SecretType] = 'split', 'end', '_private'
type _Sentinel = Sentinel[_SecretType]
_sentinel: Final[_Sentinel] = Sentinel(_secret_value)


class SplitEnd[D]:
    __slots__ = '_end', '_root', '_count'

    def __init__(self, *ds: D, root: SENode[D] | _Sentinel = _sentinel) -> None:
        """
        :param root_data: Irremovable initial data at bottom of stack.
        :param data: Removable data to be pushed onto splitend stack.
        """
        if root is _sentinel:
            if ds:
                root_node: SENode[D] = SENode(ds[0])
                ds = ds[1:]
            else:
                msg = 'SplitEnd: No data provided for root node'
                raise ValueError(msg)
        else:
            if root:
                root_node = cast(SENode[D], root)
            else:
                msg = 'SplitEnd: Provided node is not a root node'
                raise ValueError(msg)

        end, count = root_node, 1
        for d in ds:
            node = SENode(d, end)
            end, count = node, count + 1

        self._end, self._root, self._count = end, root_node, count

    def __iter__(self) -> Iterator[D]:
        return iter(self._end)

    def __reversed__(self) -> Iterator[D]:
        return reversed(list(self))

    def __bool__(self) -> bool:
        """
        :returns: ``True`` is ``SplitEnd`` is not just its root node.
        """
        return bool(self._end)

    def __len__(self) -> int:
        return self._count

    def __repr__(self) -> str:
        return 'SplitEend(' + ', '.join(map(repr, reversed(self))) + ')'

    def __str__(self) -> str:
        return '>< ' + ' -> '.join(map(str, self)) + ' ||'

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False
        if self._root != other._root:
            return False

        left = self._end
        right = other._end
        for _ in range(self._count):
            if left is right:
                return True
            if left.data() != right.data():
                return False
            if left:
                left = left._prev
                right = right._prev
        return True

    def cut(self, num: int | None = None) -> tuple[D, ...]:
        """Cut data off end of ``SplitEnd``.

        :param num: Optional number of nodes to cut, default is entire stack.
        :returns: Tuple of data cut off from end.
        """
        if num is None or num > self._count:
            num = self._count

        data: tuple[D, ...] = ()
        node = self._end
        count = self._count
        n = num
        while n > 0:
            d, node = node.both()
            data = data + (d,)
            n -= 1

        if self._count - num > 1:
            self._end, self._count = node, count - num
        else:
            self._end, self._count = node, 1

        return data

    def extend(self, *ds: D) -> None:
        """Add data onto the tip of the SplitEnd. Like adding a hair
        extension.

        :param ds: data to extend the splitend
        """
        for d in ds:
            node = SENode(d, self._end)
            self._end, self._count = node, self._count + 1

    def peak(self) -> D:
        """Return the data at end (top) of SplitEnd without consuming it.

        :returns: The data at the end of the SplitEnd.
        """
        return self._end.data()

    def root(self) -> SENode[D]:
        """
        :returns: The root SENode node of the SplitEnd.
        """
        return self._root

    def reroot(self, root: SENode[D]) -> 'SplitEnd[D]':
        """Create a brand new SplitEnd with the same data but different root.

        .. note::

            Two nodes are compatible root nodes if and only if

            - they are both actually root nodes
              - that is their previous nodes are themselves
            - their data compare as equal
              - comparing by identity is too strong for some use cases

        :returns: New SplitEnd with the same data and the new ``root``.
        :raises ValueError: If new and original root nodes are not compatible.
        """
        if not root:
            msg = 'New root node is not a root node.'
            raise ValueError(msg)
        if root.data() != self._root.data():
            msg = 'New root node not compatible with current root node.'
            raise ValueError(msg)

        lifo = LIFOQueue[D]()
        for data in self:
            lifo.push(data)
        lifo.pop()

        return SplitEnd(*lifo, root = root)

    def snip(self) -> D:
        """Snip data off tip of SplitEnd. Just return data if tip is root.

        :returns: Data snipped off tip, just return root data if at root.
        """
        if self._count > 1:
            data, self._end, self._count = self._end.both() + (self._count - 1,)
        else:
            data = self._end.data()

        return data

    def split(self, *ds: D) -> 'SplitEnd[D]':
        """Split the end and add more data.

        :returns: New instance, same data nodes plus additional ones on end.
        """
        se: SplitEnd[D] = SplitEnd(self._root.data())
        se._count, se._end, se._root = self._count, self._end, self._root
        se.extend(*ds)
        return se

    @overload
    def fold[T](self, f: Callable[[D, D], D]) -> D: ...
    @overload
    def fold[T](self, f: Callable[[T, D], T], init: T) -> T: ...

    def fold[T](self, f: Callable[[T, D], T], init: T | None = None) -> T:
        """Reduce with a function, folding from tip to root.

        :param f: Folding function, first argument is for the accumulator.
        :param init: Optional initial starting value for the fold.
        :returns: Reduced value folding from tip to root in natural LIFO order.
        """
        if init is None:
            return self._end.fold(f)  # type: ignore
        return self._end.fold(f, init)

    @overload
    def rev_fold[T](self, f: Callable[[D, D], D]) -> D: ...
    @overload
    def rev_fold[T](self, f: Callable[[T, D], T], init: T) -> T: ...

    def rev_fold[T](self, f: Callable[[T, D], T], init: T | None = None) -> T:
        """Reduce with a function, fold from root to tip.

        :param f: Folding function, first argument is for the accumulator.
        :param init: Optional initial starting value for the fold.
        :returns: Reduced value folding from root to tip.
        """
        if init is None:
            return cast(T, reduce_left(reversed(self), cast(Callable[[D, D], D], f)))
        return fold_left(reversed(self), f, init)
