# Copyright 2023-2024 Geoffrey R. Scheller
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

from pythonic_fp.splitends.splitend_node import SENode

class Test_Node:
    def test_bool(self) -> None:
        n1 = SENode(1)
        n2 = SENode(2, n1)

        assert not n1
        assert n2

    def test_linking(self) -> None:
        n1 = SENode(1)
        n2 = SENode(2, n1)
        n3 = SENode(3, n2)

        # originally done before there were methods
        assert n3._data == 3
        assert n3._prev._data == 2
        assert n2._prev is n1
        assert n1._prev is n1
        assert n2._data == n3._prev._data== 2
        assert n1._data == n2._prev._data == n3._prev._prev._data == 1
        assert n3._prev == n2
        assert n3._prev._prev is n1
        assert n3._prev._prev._prev is n1
        assert n3._prev._prev == n1
        assert n3._prev._prev._prev == n1

        assert n3.data() == 3
        assert n3.prev()._data == 2
        assert n2._prev is n1
        assert n1._prev is n1
        assert n2.data() == n3._prev.data()== 2
        assert n1.data() == n2.prev().data() == n3.prev().prev().data() == 1
        assert n3.prev() == n2
        assert n3.prev().prev() is n1
        assert n3.prev().prev().prev() is n1
        assert n3.prev().prev() == n1
        assert n3.prev().prev().prev() == n1

    def test_iter(self) -> None:
        n1 = SENode(1)
        n2 = SENode(2, n1)
        n3 = SENode(3, n2)
        n4 = SENode(4, n3)
        n5 = SENode(5, n4)

        value = 5
        for ii in n5:
            assert ii == value
            value -= 1

    def test_eq(self) -> None:
        a1 = SENode(1)
        a2 = SENode(2, a1)
        a3 = SENode(3, a2)
        a4 = SENode(4, a3)
        a5 = SENode(5, a4)

        b1 = SENode(1)
        b2 = SENode(2, b1)
        b3 = SENode(3, b2)
        b4 = SENode(4, b3)

        c2 = SENode(2, b1)
        c3 = SENode(3, b1)

        d2 = SENode(2, a1)
        d3 = SENode(3, d2)
        d4 = SENode(42, d3)
        d5 = SENode(5, d4)

        e5 = SENode(5, a4)
        e6 = SENode(6, e5)
        f5 = SENode(5, a4)
        f6 = SENode(6, f5)
        g5 = SENode(5, a4)
        g6 = SENode(6, g5)

        h6 = SENode(6, g5)
        h7 = SENode(7, g5)

        assert a1 == a1
        assert a1 != a2
        assert a1 != b1
        assert a5 != b4
        assert a4 != b4
        assert b2 == c2
        assert b2 != c3
        assert d2 != b2
        assert d2 == a2
        assert d3 != a3
        assert d3 != b3
        assert d4 != b4
        assert d5 != a5
        assert e5 == f5 == g5
        assert e6 != f6
        assert e6 != g6
        assert f6 != g6
        assert g6 == h6
        assert g6 != h7
        assert h6 != h7
        assert d5.prev() == d4
        assert d4.prev() == d3
        assert d5.prev().prev() == d3
        assert a2.prev() == a1
        assert a1.prev() == a1
        assert a1.prev() is a1
        assert a1.prev() is a1
        assert b3.prev() != a2
        assert b3.prev() is not a2
        assert b3.prev() is b2

    def test_fold(self) -> None:
        a1 = SENode(1)
        a2 = SENode(2, a1)
        a3 = SENode(3, a2)
        a4 = SENode(4, a3)
        a5 = SENode(5, a4)

        assert a4.fold(lambda x,y: x+y) == 10
        assert a4.fold(lambda x,y: x+y, 32) == 42
        assert a5.fold(lambda x,y: x+y) == 15

        b1 = SENode(1)
        b2 = SENode(2, b1)
        b3 = SENode(5, b2)
        b4 = SENode(2, b3)

        assert b4.fold(lambda x,y: x*y) == 20
        assert b4.fold(lambda x,y: x*y, 2.1) == 42.0
