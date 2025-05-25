# Pythonic FP - SplitEnds

Python package containing implementing a lifo queue-like data
structures. This project is part of the [Pythonic FP][1]
**pythonic-fp** namespace project.

- **Repositories**
  - [pythonic-fp.splitends][2] project on *PyPI*
  - [Source code][3] on *GitHub*
- **Detailed documentation**
  - [Detailed API documentation][4] on *GH-Pages*

## Package pythonic_fp.splitends

Singularly linked data structures allowing data to be safely shared
between multiple instances by making shared data immutable and
inaccessible to client code.

- *module* pythonic_fp.splitends.splitend
  - *class* SplitEnd: Singularly link stack with shareable data nodes
- *module* pythonic_fp.splitends.splitend_node
  - *class* SENode: shareable nodes used by SplitEnd instances

______________________________________________________________________

[1]: https://github.com/grscheller/pythonic-fp/blob/main/README.md
[2]: https://pypi.org/project/pythonic-fp.splitends/
[3]: https://github.com/grscheller/pythonic-fp-splitends/
[4]: https://grscheller.github.io/pythonic-fp/maintained/splitends/
