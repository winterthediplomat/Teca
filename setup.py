#from distutils.core import setup
from setuptools import setup

setup(
    name='Teca',
    version='0.1.11',
    author='alfateam123',
    author_email='alfateam123@gmail.com',
    packages=['teca'],
    #scripts=['bin/index', 'bin/post_details', 'bin/thread_details', 'bin/search'],
    url='http://github.com/alfateam123/Teca',
    # license='LICENSE.txt',
    description='simple static gallery generator',
    long_description=open('README.md').read(),
    install_requires=[
        "jinja2",
        "pillow",
        "six"
    ],
    extras_require={
        "test": ["nose", "mockfs", "coverage"]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    test_suite="tests"
)
