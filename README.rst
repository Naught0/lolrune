lolrune
-------

|docs| |pypi|

A set of clients which can fetch optimal rune data for a given champion.
``RuneClient`` utilizes ``requests``, while ``AioRuneClient`` utilizes ``aiohttp`` and ``asyncio``.

Installation
~~~~~~~~~~~~

Simply run ``python3 -m pip install lolrune -U``. Be sure to update
regularly as this is being actively developed.

Documentation
~~~~~~~~~~~~~

You can find the docs at http://lolrune.readthedocs.io/ and a quick example below.

Quick Example
~~~~~~~~~~~~~

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

Issues
~~~~~~

If you have any trouble, or see some way to improve the code, please
submit a PR or an issue.

.. |docs| image:: https://readthedocs.org/projects/lolrune/badge/?version=latest
  :target: http://lolrune.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. |pypi| image:: https://badge.fury.io/py/lolrune.svg
  :target: https://badge.fury.io/py/lolrune