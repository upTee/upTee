import os
from setuptools import setup, find_packages

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

# Use the docstring of the __init__ file to be the description
DESC = " ".join(__import__('uptee').__doc__.splitlines()).strip()

setup(
    name = "uptee",
    version = __import__('uptee').get_version().replace(' ', '-'),
    url = 'http://github.com/SushiTee/upTee',
    author = 'Sascha Weichel',
    author_email = 'sascha.weichel@xxx.xx',
    description = DESC,
    long_description = read_file('README'),
    packages = find_packages(),
    include_package_data = True,
    install_requires=read_file('requirements.txt'),
    classifiers = [
        'Framework :: Django',
    ],
)
