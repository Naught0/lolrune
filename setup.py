from pkg_resources import get_distribution, DistributionNotFound
from setuptools import setup

try:
    __version__ = get_distribution('lolrune').version
except DistributionNotFound:
    pass

try:
    with open('README.rst') as f:
        long_description = f.read()
except (FileNotFoundError, IOError):
    long_description = ''

setup(
    name='lolrune',
    packages=['lolrune'],
    description='A set of clients which allows you to gather optimal runes for a given League of Legends champion.',
    long_description=long_description,
    use_scm_version={
        'version_scheme': 'guess-next-dev',
        'local_scheme': 'dirty-tag'
    },
    setup_requires=['setuptools_scm'],
    install_requires=['requests', 'bs4', 'lxml'],
    extras_require={
        'async': ['aiohttp>=2.3.3']
    },
    author='James E',
    author_email='naught0@github.com',
    url='https://github.com/naught0/lolrune',
    license='MIT'
)
