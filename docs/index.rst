.. lolrune documentation master file, created by
   sphinx-quickstart on Tue Dec 19 22:23:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: /images/logo.png
    :scale: 80%
    :align: center

lolrune is a package which contains two separate clients through which you can fetch
League of Legends rune information for any champion. 

The information is scraped from Runeforge.gg and returned in a tuple, containing dicts (i.e. JSON friendly).

Quick Start
-----------

I'll use the default ``RuneClient`` here, using JSON only to prettify the formatting::

    >>> import json
    >>> from lolrune import RuneClient
    >>> client = RuneClient()
    >>> print(json.dumps(client.get_runes('varus'), indent=2))
    [
      {
        "name": "Varus",
        "title": "Bloodshed Carries a Price",
        "description": "Lethality focused long range poke with [Q].",
        "runes": {
          "primary": {
            "name": "Sorcery",
            "keystone": "Arcane Comet",
            "rest": [
              "Manaflow Band",
              "Celerity",
              "Scorch"
            ]
          },
          "secondary": {
            "name": "Precision",
            "rest": [
              "Triumph",
              "Coup De Grace"
            ]
          }
        }
      }, ...
    ]

Be aware, despite ``[]`` displaying here (per the ``json`` module), the return type will be a ``tuple`` for each client.

Contents
---------

.. toctree::
   :name: Contents
   :maxdepth: 3

   api


Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
