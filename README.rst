=======================
Pythonic FP - SplitEnds
=======================

Singularly linked data structures allowing data to be safely shared
between multiple instances.

This project is part of the
`PyPI pythonic-fp Namespace Projects <https://github.com/grscheller/pythonic-fp/blob/main/README.rst>`_.

Detailed API documentation
`documentation <https://grscheller.github.io/pythonic-fp/maintained/splitends>`_
on *GH-Pages*.

Features:
---------

Stateful singularly linked data structures allowing data to be safely shared
between multiple instances by making shared data immutable and inaccessible to
client code. Also the infrastructure supporting the entire head of hair.

**Warning:** The PyPI ``pythonic_fp.splitends`` project is Alpha level software
and subject to change. It will probably remain Alpha for quite a while.

Singularly link stack with shareable data nodes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- *module* ``pythonic_fp.splitends.splitend``
- *class* ``SplitEnd``: Singularly link stack with shareable data nodes

  - This class provides the primary client code API interface

Shareable nodes used by SplitEnd instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- *module* ``pythonic_fp.splitends.splitend_node``
- *class* ``SENode``: Shareable nodes used by SplitEnd instances

  - This class is designed to be inaccessible to client code
  - It is intended to be a implementation detail for the ``SplitEnd`` class

Installation:
-------------

| $ pip install pythonic-fp.splitends

Contribute:
-----------

- Project on PyPI: https://pypi.org/project/pythonic-fp.splitends
- Source Code: https://github.com/grscheller/pythonic-fp-splitends
- Issue Tracker: https://github.com/grscheller/pythonic-fp-splitends/issues
- Pull Requests: https://github.com/grscheller/pythonic-fp-splitends/pulls
- CHANGELOG: https://github.com/grscheller/pythonic-fp-splitends/blob/main/CHANGELOG.rst

+------------------------------------------------+----------------------+--------------------+
| Contributors                                   | Name                 | Role               |
+================================================+======================+====================+
| `@grscheller <https://github.com/grscheller>`_ | Geoffrey R. Scheller | author, maintainer |
+------------------------------------------------+----------------------+--------------------+

License Information
^^^^^^^^^^^^^^^^^^^

This project is licensed under the Apache License Version 2.0, January 2004.

See the `LICENCE file <https://github.com/grscheller/pythonic-fp-splitends/blob/main/LICENSE>`_
for details.
