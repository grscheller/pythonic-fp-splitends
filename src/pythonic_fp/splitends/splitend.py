# Copyright 2023-2026 Geoffrey R. Scheller
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
Class SplitEnds
---------------

.. admonition:: LIFO stacks safely sharing immutable data.

    - each ``SplitEnd`` is a very simple stateful (mutable) LIFO stack
    - data can be either "extended" to or "snipped" off the "end"
    - "root" of a ``SplitEnd`` is embedded in a ``scalp``

      - the root data is immutable
      - it cannot be split off

    - different mutable split ends can safely share the same "tail"
    - each ``SplitEnd`` sees itself as a singularly linked list
    - bush-like datastructures can be formed using multiple ``SplitEnds``
    - the ``SplitEnd.split`` and ``len`` methods are O(1)
    - in a boolean context

      - falsy just a "root"
      - truthy otherwise

"""

from collections.abc import Callable, Iterator
from typing import cast, Final, overload
from pythonic_fp.gadgets.sentinels.flavored import Sentinel
from pythonic_fp.iterables.folding import reduce_left, fold_left
from pythonic_fp.queues.lifo import LIFOQueue
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
        .. admonition:: init

            :param root_data: Irremovable initial data at bottom of stack.
            :param ds: Removable data to be pushed onto splitend stack.

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
        """
        .. admonition:: iter

            Iterate from end to root.

            :yields: data from end to root

        """
        return iter(self._end)

    def __reversed__(self) -> Iterator[D]:
        """
        .. admonition:: reverse iter

            Iterate from end to root.

            :yields: data from end to root

        """
        return reversed(list(self))

    def __bool__(self) -> bool:
        """
        .. admonition:: bool

            :returns: ``True`` if ``SplitEnd`` is not just its root node.

        """
        return bool(self._end)

    def __len__(self) -> int:
        """
        .. admonition:: len

            :returns: The number of nodes on the ``Splitend``.

        """
        return self._count

    def __eq__(self, other: object, /) -> bool:
        """
        .. admonition:: equality comparison

            Efficiently compare two ``SplitEnds``.

            :returns: ``True`` only if ``other`` is also a ``Splitend``
                      whose corresponding data to ``self`` compares as
                      equal and both share the same root node.
                      Otherwise ``False``.

        """
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
                left = left.prev()
                right = right.prev()
        return True

    def __repr__(self) -> str:
        """
        .. admonition:: repr string

            Construct string to reproduce the ``SplitEnd``.
            TODO: Fix, does not include root node.

            :returns: String to reproduce the ``SplitEnd``.

        """
        return 'SplitEend(' + ', '.join(map(repr, reversed(self))) + ')'

    def __str__(self) -> str:
        """
        .. admonition:: user string

            Construct string meaningful to an end user.
            Does not give root node info.

            :returns: String to reproduce the ``SplitEnd``.

        """
        return '>< ' + ' -> '.join(map(str, self)) + ' ||'

    def snip(self) -> D:
        """
        .. admonition:: cut just tip

            :returns: Data from snipped tip,
                    just return root data if at root.

        """
        if self._count > 1:
            data, self._end, self._count = self._end.both() + (self._count - 1,)
        else:
            data = self._end.data()

        return data

    def cut(self, num: int | None = None) -> tuple[D, ...]:
        """
        .. admonition:: Cut data off end of SplitEnd

            Pop "cut" data off Split, just copy root data.

            :param num: Optional number of nodes to cut,
                        default is entire stack.
            :returns: Tuple of data cut off from end towards root.

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
        """
        .. admonition:: extend SplitEnd with data

            Add data onto the tip of the SplitEnd. Like adding
            a hair extension.

            :param ds: data to extend the splitend

        """
        for d in ds:
            node = SENode(d, self._end)
            self._end, self._count = node, self._count + 1

    def peak(self) -> D:
        """
        .. admonition:: peak at end

            Return the data at end (top) of the SplitEnd
            without consuming it.

            :returns: The data at the end (tip) of the SplitEnd.

        """
        return self._end.data()

    def root(self) -> SENode[D]:
        """
        .. admonition:: get root

            :returns: The root SENode node of the SplitEnd.

        """
        return self._root

    def reroot(self, root: SENode[D]) -> 'SplitEnd[D]':
        """
        .. admonition:: re-root SplitEnd

            Create a brand new SplitEnd with the same data but different root.

            :returns: New SplitEnd with the same data
                      and the new ``root``.
            :raises ValueError: If new and original root nodes
                                are not compatible.

            .. note::

                Two nodes are compatible root nodes if and only if

                - they are both actually root nodes

                - which implies that their previous nodes are themselves

                - their data compare as equal

                - comparing by identity is too strong

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

    def split(self, *ds: D) -> 'SplitEnd[D]':
        """
        .. admonition:: split

            Split the end and add more data.

            :returns: New instance, same data nodes plus
                      additional ones on end. Same root node.

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
        """
        .. admonition:: fold

            Reduce with a function, folding from tip to root.

            :param f: Folding function, first argument
                      is for the accumulator.
            :param init: Optional initial starting value for the fold.
            :returns: Reduced value folding from tip to root
                      in natural LIFO order.

        """
        if init is None:
            return self._end.fold(f)  # type: ignore
        return self._end.fold(f, init)

    @overload
    def rev_fold[T](self, f: Callable[[D, D], D]) -> D: ...
    @overload
    def rev_fold[T](self, f: Callable[[T, D], T], init: T) -> T: ...

    def rev_fold[T](self, f: Callable[[T, D], T], init: T | None = None) -> T:
        """
        .. admonition:: reverse fold

            Reduce with a function, fold from root to tip.

            :param f: Folding function, first argument
                      is for the accumulator.
            :param init: Optional initial starting value for the fold.
            :returns: Reduced value folding from root to tip.

        """
        if init is None:
            return cast(T, reduce_left(reversed(self), cast(Callable[[D, D], D], f)))
        return fold_left(reversed(self), f, init)
