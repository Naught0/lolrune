.. lolrune documentation master file, created by
   sphinx-quickstart on Tue Dec 19 22:23:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
 
.. image:: /images/logo.png
    :scale: 60%
    :align: center


lolrune is a package which contains two separate clients through which you can fetch
League of Legends rune information for any champion. 

Warning
--------

This is the dev code which is a major breaking change to previous schemas in earlier versions of lolrune.

Contents
---------

.. toctree::
   :name: Contents
   :maxdepth: 3

   api

Quick Example
-------------

.. code:: python3

  >>> from lolrune import RuneClient
  >>> client = RuneClient()
  >>> champ = client.get_runes('kalista')[0]
  >>> runes = champ.runes
  >>> champ.name
  'Kalista'
  >>> champ.title
  'Hip Hop a Potamus'
  >>> champ.description
  'Maximum execute damage.'
  >>> runes
  <lolrune.runepage.RunePage object at 0x7fce9b5fc940>
  >>> runes.keystone
  'Press the Attack'
  >>> runes.primary.name
  'Precision'
  >>> runes.primary.runes
  ['Overheal', 'Legend: Bloodline', 'Coup De Grace']
  >>> runes.secondary.name
  'Domination'
  >>> runes.secondary.runes
  ['Sudden Impact', 'Ghost Poro']

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
