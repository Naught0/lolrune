|lolrune|

lolrune
-------------------

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
  <RunePage keystone=Press the Attack secondary=Domination>
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

Attribution
~~~~~~~~~~~
|rfgg|

A big thanks to the Runeforge.gg guys for making this data available through their website! I recommend you check them out.

Issues
~~~~~~

If you have any trouble, or see some way to improve the code, please
submit a PR or an issue.

.. |docs| image:: https://readthedocs.org/projects/lolrune/badge/?version=latest
  :target: http://lolrune.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. |pypi| image:: https://badge.fury.io/py/lolrune.svg
  :target: https://badge.fury.io/py/lolrune

.. |rfgg| image:: http://runeforge.gg/wp-content/themes/rune_forge/imgs/logo-shiny.svg
  :target: http://runeforge.gg/

.. |rfggsmall| image:: http://d181w3hxxigzvh.cloudfront.net/wp-content/themes/rune_forge/favicon-32x32.png

.. |lolrune| image::  https://image.ibb.co/emXvWb/300x300ogo.png
