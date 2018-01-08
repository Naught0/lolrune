.. lolrune documentation master file, created by
   sphinx-quickstart on Tue Dec 19 22:23:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
 
.. image:: /images/logo.svg
   :height: 300px
   :width: 300px
   :align: center

lolrune is a package which contains two clients (async and non-async), through which you can fetch League of Legends rune information for any champion. 

Installation
------------

There are two clients included with lolrune. You can install the default 
which uses the requests_ library like so:

On Unix-based OSes (you may need sudo)

.. code:: bash
    
    $ python3 -m pip install -U lolrune

or on Windows

.. code:: bat
    
    > py -3 -m pip install -U lolrune

In order to install dependencies required for the asynchronous client,
which uses aiohttp_, you may do the following:

.. code:: bash

    $ python3 -m pip install -U lolrune[async]

The ``[async]`` part is 100% necessary in order to use the ``AioRuneClient``,
unless of course you have aiohttp_ installed already.

.. note::

    It is typically recommended to install packages in a virtual 
    environment by using pipenv_.

Contents
---------

.. toctree::
   :name: Contents
   :maxdepth: 3
   
   examples
   api

Attribution
-----------

All lolrune data is obtained via scraping Runeforge_.

I highly recommend you check them out!

|rfgg|

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`


.. _pipenv: https://github.com/pypa/pipenv

.. _requests: http://docs.python-requests.org/

.. _aiohttp: https://aiohttp.readthedocs.io/

.. _Runeforge: http://runeforge.gg

.. |rfgg| image:: http://runeforge.gg/wp-content/themes/rune_forge/imgs/logo-shiny.svg
  :target: http://runeforge.gg/