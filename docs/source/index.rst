.. Pythonic FP - Circular Array documentation master file, created by
   sphinx-quickstart on Fri Jun 27 11:13:22 2025.
   To regenerate the documentation do: ``$ Sphinx-build -M html docs/source/ docs/build/``
   from the root repo directory.

Pythonic FP - Splitends project
===============================

Part of of the `pythonic-fp namespace projects <https://github.com/grscheller/pythonic-fp/blob/main/README.md>`_.

Overview
--------

PyPI project `pythonic.splitends <https://pypi.org/project/pythonic-fp.splitends/>`_
implementing a singularly linked data structures allowing data to be
safely shared between multiple instances.

- Singularly link stack with shareable data nodes

  - *module* `pythonic_fp.splitends.splitend`
  - *class* `SplitEnd`

- Shareable nodes used by SplitEnd instances

  - *module* `pythonic_fp.splitends.splitend_node`
  - *class* `SENode`

    - shareable nodes used by SplitEnd instances

      - this class is designed to be inaccessible to client code


Documentation
-------------

:doc:`Installation <installing>`
    Installing and importing the module.

:doc:`API docs <api>`
    Detailed API documentation.

Development
-----------

:doc:`changelog`
    CHANGELOG for the current and predecessor projects.

.. Hidden TOCs

.. toctree::
   :caption: Documentation
   :maxdepth: 2
   :hidden:

   installing
   api

.. toctree::
   :caption: Development
   :maxdepth: 2
   :hidden:

   changelog

