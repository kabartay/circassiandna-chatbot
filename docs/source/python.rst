Python modules
==============

.. note::
   This page shows **literal source listings** only — Sphinx does **not** import
   or execute these modules. Paths are relative to this file (``docs/source/python.rst``),
   so ``../../app.py`` points to the repo root.

   If you later switch to autodoc (e.g. ``.. automodule:: app``), ensure your
   modules have **no import-time side effects** (no network calls, file I/O, or
   starting servers). Put run logic under:

   .. code-block:: python

      if __name__ == "__main__":
          main()

.. warning::
   Don’t expose secrets. Keep ``.env`` out of the repo and out of docs builds.
   In ``conf.py`` you can guard with:

   .. code-block:: python

      exclude_patterns += ["**/.env", "**/*.env"]

.. tip::
   Long files? Show a slice with ``:lines:``,
   or highlight parts with ``:emphasize-lines:``:

   .. code-block:: rst

      .. literalinclude:: ../../app.py
         :language: python
         :lines: 1-120
         :emphasize-lines: 12-18,45-47


.. literalinclude:: ../../app.py
   :language: python
   :linenos:
   :caption: app.py

.. literalinclude:: ../../combine_jsons.py
   :language: python
   :linenos:
   :caption: combine_jsons.py

.. literalinclude:: ../../lambda_handler.py
   :language: python
   :linenos:
   :caption: lambda_handler.py

.. literalinclude:: ../../utils.py
   :language: python
   :linenos:
   :caption: utils.py
