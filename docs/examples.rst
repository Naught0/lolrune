.. currentmodule:: lolrune

Examples
========
The lolrune library has quite a bit of flexibility between sync/async clients, as well as return formatting.

Clients
-------
There are two clients you can use to fetch champion rune data.

.. note:: If you're looking for ``Wukong``, search instead for ``monkeyking``. Riot decided that's what they're going to call him, so here we are.

.. _rune_client_ex:

RuneClient
~~~~~~~~~~
This client utilizes a :class:`requests.Session` to retrieve rune data, and is therefore blocking/synchronous.

.. code:: python3
   
   from lolrune import RuneClient

   
   client = RuneClient()
   champ_tup = client.get_runes('velkoz')

   for champ in champ_tup:
      print('{0.name}: {0.description}'.format(champ))

Will yield ``Vel'Koz: Maximum AP and 1-shot potential.``

Searching for a champion with more than one rune page, like Zoe, will yield:

.. code::

   Zoe: We all grow up! Well, you died
   Zoe: Sorry! Beauty Always Has Tears

**Note:** All champion names are case insensitive with any special characters and spaces removed.
For example, ``Vel'Koz`` becomes ``velkoz`` and ``Lee Sin`` becomes ``leesin``.

.. _aio_client_ex:

AioRuneClient
~~~~~~~~~~~~~
This client utilizes an :class:`asyncio.AbstractEventLoop` and an :class:`aiohttp.ClientSession` to retrieve data, and is therefore non-blocking/asynchronous.

.. code:: python3
   
   import asyncio
   from lolrune import AioRuneClient

   loop = asyncio.get_event_loop()
   run = loop.run_until_complete

   client = AioRuneClient()
   # If you're in an async environment, you'll use await for all coroutines.
   champ_tup = run(client.get_runes('velkoz'))

   for champ in champ_tup:
      print('{0.name}: {0.description}'.format(champ))

Yields ``Vel'Koz: Maximum AP and 1-shot potential.``

Searching for a champion with more than one rune page, like Riven, will yield:

.. code::
   
   Riven: Sacrifices Must be Made
   Riven: No More Hesitation

**Note:** All champion names are case insensitive with any special characters and spaces removed.
For example, ``Vel'Koz`` becomes ``velkoz`` and ``Lee Sin`` becomes ``leesin``.

Return data format
------------------
There are a few ways in which you can interact with the data retrieved by lolrune.

.. _raw_return_formatting:

Raw return formatting
~~~~~~~~~~~~~~~~~~~~~
The lolrune API returns its data in a :class:`Tuple[dict]` format. You can easily interact with the raw data on this level.

**Note**: Most champions will return a tuple with a *single item*, i.e. a *single rune page*. Both :meth:`RuneClient.get_raw()` and :meth:`AioRuneClient.get_raw()` will automatically return data in this format:

.. code:: python3
   
   (
      {
       'name': 'Varus',
       'title': 'Bloodshed Carries a Price',
       'url': 'http://runeforge.gg/loadouts/bloodshed-carries-price/'
       'description': 'Lethality focused long range poke with [Q].',
       'runes': {
         'primary': {
           'name': 'Sorcery',
           'keystone': 'Arcane Comet',
           'rest': [
             'Manaflow Band',
             'Celerity',
             'Scorch'
           ]
         },
         'secondary': {
           'name': 'Precision',
           'rest': [
             'Triumph',
             'Coup De Grace'
           ]
         }
       }
     },
     {
       'name': 'Varus',
       'title': 'Blighted Arrow Dominance',
       'url': 'http://runeforge.gg/loadouts/blighted-arrow-dominance/'
       'description': 'Massive sustained shred damage.',
       'runes': {
         'primary': {
           'name': 'Precision',
           'keystone': 'Press the Attack',
           'rest': [
             'Triumph',
             'Legend: Bloodline',
             'Coup De Grace'
           ]
         },
         'secondary': {
           'name': 'Domination',
           'rest': [
             'Taste of Blood',
             'Ravenous Hunter'
           ]
         }
       }
     }
   )

.. _abs_return_formatting:

Abstract return formatting
~~~~~~~~~~~~~~~~~~~~~~~~~~
If you would prefer a more pythonic interface, one is provided.

lolrune includes a :class:`Champion` class, which contains the returned :class:`RunePage`, which holds the two rune :class:`Tree`\s. In order to access this interface, you may call :meth:`RuneClient.get_runes()` and :meth:`AioRuneClient.get_runes()`\, depending on your client of choice.

**Structure:**

.. code::

   Champion
   ├───description : str
   ├───name : str
   ├───runes : RunePage
   │   ├───keystone : str
   │   ├───primary : Tree
   │   │   ├───name : str
   │   │   └───runes : List[str]
   │   └───secondary : Tree
   │       ├───name : str
   │       └───runes : List[str]
   ├───title : str
   └───url : str

**Usage:**

.. code:: python3
   
   >>> from lolrune import RuneClient
   >>> client = RuneClient()
   >>> champ = client.get_champ('varus')[0] # This method returns a tuple
   >>> runes = champ.runes
   >>> champ.name
   'Varus'
   >>> champ.title
   'Bloodshed Carries a Price'
   >>> champ.description
   'Lethality focused long range poke with [Q].'
   >>> runes.keystone
   'Arcane Comet'
   >>> runes.primary
   Tree(name='Sorcery', runes=['Manaflow Band', 'Celerity', 'Scorch'])
   >>> runes.secondary
   Tree(name='Precision', runes=['Triumph', 'Coup De Grace'])
