# Pythonic FP - SplitEnds

Singularly linked data structures allowing data to be safely shared
between multiple instances.

This project is part of the PyPI
[PyPI
pythonic-fp](https://github.com/grscheller/pythonic-fp/blob/main/README.rst)
Namespace Projects.

Detailed API documentation
[documentation](https://grscheller.github.io/pythonic-fp/maintained/splitends)
on *GH-Pages*.

## Features:

Stateful singularly linked data structures allowing data to be safely shared
between multiple instances by making shared data immutable and inaccessible to
client code. Also the infrastructure supporting the entire head of hair.

**Warning:** The PyPI ``pythonic_fp.splitends`` project is Alpha level software
and subject to change. It will probably remain Alpha for quite a while.

### Singularly link stack with shareable data nodes

- *module* `pythonic_fp.splitends.splitend`
- *class* `SplitEnd`: Singularly link stack with shareable data nodes
  - This class provides the primary client code API interface

### Shareable nodes used by SplitEnd instances

- *module* ``pythonic_fp.splitends.splitend_node``
- *class* ``SENode``: Shareable nodes used by SplitEnd instances
  - This class is designed to be inaccessible to client code
  - It is intended to be an implementation detail for the ``SplitEnd`` class

This PyPI project is part of of the grscheller
[pythonic-fp namespace projects](https://grscheller.github.io/pythonic-fp/).

## Documentation

Documentation hosted on
[GitHub Pages](https://grscheller.github.io/pythonic-fp-splitends/).

## Copyright and License

Copyright (c) 2023-2025 Geoffrey R. Scheller. Licensed under the Apache
License, Version 2.0. See the LICENSE file for details.
