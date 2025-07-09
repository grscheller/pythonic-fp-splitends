..
   Pythonic FP - Splitends documentation master file. To regenerate the sphinx
   documentation do: "$ make html" from the "docs/" directory.

Pythonic FP - Splitends
=======================

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

Part of of the
`pythonic-fp namespace projects <https://github.com/grscheller/pythonic-fp/blob/main/README.md>`_.

Documentation
-------------

:doc:`Current Development API <api>`
    Development environment API documentation.

:doc:`CHANGELOG <changelog>`
    For the current and predecessor projects.

.. toctree::
   :caption: Documentation
   :maxdepth: 2
   :hidden:

   installing
   api_pypi
   api

.. toctree::
   :caption: Development
   :maxdepth: 1
   :hidden:

   changelog

.. toctree::
   :caption: Back to start
   :maxdepth: 1
   :hidden:

   self
