lolrune
-------

A set of clients which can fetch optimal rune data for a given champion.
``RuneClient`` utilizes requests, while ``AioRuneClient`` utilizes ``aiohttp`` and ``asyncio``.

Installation
~~~~~~~~~~~~

Simply run ``python3 -m pip install lolrune -U``. Be sure to update
regularly as this is being actively developed.

Documentation
~~~~~~~~~~~~~

You can find the docs at http://lolrune.readthedocs.io/ and a quick example below.

Examples
~~~~~~~~

.. code:: py

    >>> import json
    >>> from lolrune import RuneClient, AioRuneClient
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
      },
      {
        "name": "Varus",
        "title": "Blighted Arrow Dominance",
        "description": "Massive sustained shred damage.",
        "runes": {
          "primary": {
            "name": "Precision",
            "keystone": "Press the Attack",
            "rest": [
              "Triumph",
              "Legend: Bloodline",
              "Coup De Grace"
            ]
          },
          "secondary": {
            "name": "Domination",
            "rest": [
              "Taste of Blood",
              "Ravenous Hunter"
            ]
          }
        }
      }
    ]
    >>> import asyncio
    >>> loop = asyncio.get_event_loop()
    >>> run = loop.run_until_complete
    >>> aioclient = AioRuneClient(loop=loop)
    >>> zoe = run(aioclient.get_runes('zoe'))
    >>> print(json.dumps(zoe, indent=2))
    [
      {
        "name": "Zoe",
        "title": "We all grow up! Well, you died",
        "description": "Maximum damage, assassination, and one-shot threat.",
        "runes": {
          "primary": {
            "name": "Domination",
            "keystone": "Electrocute",
            "rest": [
              "Sudden Impact",
              "Eyeball Collection",
              "Ravenous Hunter"
            ]
          },
          "secondary": {
            "name": "Sorcery",
            "rest": [
              "Scorch",
              "Transcendence"
            ]
          }
        }
      },
      {
        "name": "Zoe",
        "title": "Sorry! Beauty Always Has Tears",
        "description": "Efficient lane trading/poking and mid game power spikes.",
        "runes": {
          "primary": {
            "name": "Sorcery",
            "keystone": "Arcane Comet",
            "rest": [
              "The Ultimate Hat",
              "Transcendence",
              "Scorch"
            ]
          },
          "secondary": {
            "name": "Domination",
            "rest": [
              "Sudden Impact",
              "Zombie Ward"
            ]
          }
        }
      }
    ]

Issues
~~~~~~

If you have any trouble, or see some way to improve the code, please
submit a PR or an issue.
