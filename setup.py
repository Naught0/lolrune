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
    use_scm_version={
        'version_scheme': 'guess-next-dev',
        'local_scheme': 'dirty-tag'
    },
    setup_requires=['setuptools_scm', 'aiohttp', 'requests', 'bs4', 'lxml'],
    description='A set of clients which allows you to gather optimal runes for a given League of Legends champion.',
    long_description=long_description,
    author='James E',
    author_email='naught0@github.com',
    url='https://github.com/naught0/lolrune',
    license='MIT',
    python_requires='>=3.5.2'
)
