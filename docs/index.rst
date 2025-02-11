.. Rest API documentation master file, created by
   sphinx-quickstart on Fri Feb  7 13:10:54 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Rest API documentation
======================

This documentation provides an overview of the FastAPI application, including
API endpoints, repository interactions, services, database, and schemas.

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

REST API main
===================
.. automodule:: main
  :members:
  :undoc-members:
  :show-inheritance:

REST API repository Contacts
============================
.. automodule:: src.repository.contacts
  :members:
  :undoc-members:
  :show-inheritance:

REST API repository Users
=========================
.. automodule:: src.repository.users
  :members:
  :undoc-members:
  :show-inheritance:

REST API services
=================
.. automodule:: src.services.auth
  :members:
  :undoc-members:
  :show-inheritance:

.. automodule:: src.services.contacts
  :members:
  :undoc-members:
  :show-inheritance:

.. automodule:: src.services.email
  :members:
  :undoc-members:
  :show-inheritance:

.. automodule:: src.services.upload_file
  :members:
  :undoc-members:
  :show-inheritance:

.. automodule:: src.services.users
  :members:
  :undoc-members:
  :show-inheritance:

.. automodule:: src.services.cache
  :members:
  :undoc-members:
  :show-inheritance:

REST API database
=================
.. automodule:: src.database.db
  :members:
  :undoc-members:
  :show-inheritance:

REST API schemas
================
.. automodule:: src.schemas.contacts
  :members:
  :undoc-members:
  :show-inheritance:

.. automodule:: src.schemas.users
  :members:
  :undoc-members:
  :show-inheritance:

REST API configuration
======================
.. automodule:: src.conf.config
  :members:
  :undoc-members:
  :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

