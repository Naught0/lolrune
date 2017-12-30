.. lolrune documentation master file, created by
   sphinx-quickstart on Tue Dec 19 22:23:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
 
.. image:: /images/logo.png
   :scale: 40%
   :align: center

lolrune is a package which contains two clients (async and non-async), through which you can fetch League of Legends rune information for any champion. 

Installation
------------

On Unix-based OSes (you may need sudo)

.. code:: bash
    
    $ python3 -m pip install lolrune

or on Windows

.. code:: bat
    
    > py -3 -m pip install lolrune

Alternatively, install in a virtual environment by using pipenv_.

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

.. _Runeforge: http://runeforge.gg

.. |rfgg| image:: http://runeforge.gg/wp-content/themes/rune_forge/imgs/logo-shiny.svg
  :target: http://runeforge.gg/