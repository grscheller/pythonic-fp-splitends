# Copyright 2024-2025 Geoffrey R. Scheller
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

"""Mutable stack objects that can safely share data.

Python package implementing a singularly linked stack of nodes called a ``SplitEnd``.
While mutable, these data structures can safely share immutable data nodes between
themselves. These nodes, of type ``SENode``, always contain data. A root node is
a node whose previous node is itself. Root nodes mark the bottom of the stack.

Like one of many "split ends" from shafts of hair, a ``SplitEnd`` can be "snipped"
shorter or "extended" further from its "end" node at the top of the stack. Its "root"
node is at the bottom of the stack and can not be "snipped" or "cut" off.

A ``SplitEnd`` can be duplicated onto a compatible root node. By compatible, the
new root must contain data that compares as equal to the old root node.

TODO: A ``scalp`` is a container of root nodes all of whose contained data must be
hashable. The ``scalp.add(d)`` method will return the unique root node with data
that compares as equal to ``d``, or create a new root node if such a contained node
does not exist.
"""

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
