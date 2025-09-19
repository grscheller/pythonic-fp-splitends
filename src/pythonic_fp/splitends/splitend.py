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

"""LIFO stacks safely sharing immutable data between themselves."""

from collections.abc import Callable, Iterator
from pythonic_fp.iterables.folding import maybe_fold_left
from .splitend_node import SENode

__all__ = ['SplitEnd']


class SplitEnd[D]:
    """Like one of many "split ends" from a shaft of hair,
    a ``splitend`` can be "snipped" shorter or "extended"
    further from its "tip". Its root is irremovable and
    cannot be "snipped" off. While mutable, different
    splitends can safely share data with each other.
    """

    __slots__ = '_count', '_tip', '_root'

    def __init__(self, root_data: D, *data: D) -> None:
        """
        :param root_data: Irremovable initial data at bottom of stack.
        :param data: Removable data to be pushed onto splitend stack.
        """
        node: SENode[D] = SENode(root_data)
        self._root = node
        self._tip, self._count = node, 1
        for d in data:
            node = SENode(d, self._tip)
            self._tip, self._count = node, self._count + 1

    def __iter__(self) -> Iterator[D]:
        return iter(self._tip)

    def __reversed__(self) -> Iterator[D]:
        return reversed(list(self))

    def __bool__(self) -> bool:
        # Returns true until all data is exhausted
        return bool(self._tip)

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

        left = self._tip
        right = other._tip
        for _ in range(self._count):
            if left is right:
                return True
            if left.peak_data() != right.peak_data():
                return False
            if left:
                left = left._prev.get()
                right = right._prev.get()
        return True

    def extend(self, *ds: D) -> None:
        """Add data onto the tip of the SplitEnd. Like adding a hair
        extension.

        :param ds: data to extend the splitend
        """
        for d in ds:
            node = SENode(d, self._tip)
            self._tip, self._count = node, self._count + 1

    def peak(self) -> D:
        """Return the data at end of SplitEnd without consuming it.

        :returns: The data at the tip of the SplitEnd.
        """
        return self._tip.peak_data()

    def snip(self) -> D:
        """Snip data off tip of SplitEnd. Just return data if tip is root.

        :returns: Data snipped off tip, just return root data if at root.
        """
        if self._count > 1:
            data, self._tip, self._count = self._tip.peak2() + (self._count - 1,)
        else:
            data = self._tip.peak_data()

        return data

    def cut(self, num: int | None = None) -> tuple[D, ...]:
        """Cut data off end of ``SplitEnd``.

        :param num: Optional number of nodes to cut, default is entire stack.
        :returns: Tuple of data cut off from end.
        """
        if num is None or num > self._count:
            num = self._count

        data: tuple[D, ...] = ()
        node = self._tip
        count = self._count
        n = num
        while n > 0:
            d, node = node.peak2()
            data = data + (d,)
            n -= 1

        if self._count - num > 1:
            self._tip, self._count = node, count - num
        else:
            self._tip, self._count = node, 1

        return data

    def split(self, *ds: D) -> 'SplitEnd[D]':
        """Split the end and add more data.

        :returns: New instance, same data nodes plus additional ones on end.
        """
        se: SplitEnd[D] = SplitEnd(self._root.peak_data())
        se._count, se._tip, se._root = self._count, self._tip, self._root
        se.extend(*ds)
        return se

    def fold[T](self, f: Callable[[T, D], T], init: T | None = None) -> T:
        """Reduce with a function, folding from tip to root.

        :param f: Folding function, first argument is for the accumulator.
        :param init: Optional initial starting value for the fold.
        :returns: Reduced value folding from tip to root in natural LIFO order.
        """
        return self._tip.fold(f, init)

    def rev_fold[T](self, f: Callable[[T, D], T], init: T | None = None) -> T:
        """Reduce with a function, fold from root to tip.

        :param f: Folding function, first argument is for the accumulator.
        :param init: Optional initial starting value for the fold.
        :returns: Reduced value folding from root to tip.
        """
        if init is None:
            return maybe_fold_left(reversed(self), f).get()
        return maybe_fold_left(reversed(self), f, init).get()
