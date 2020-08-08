#!/usr/bin/python
# -*- coding=utf-8 -*-
from setuptools import setup

# to install type:
# python setup.py install --root=/
from io import open
def readme():
    with open('README.rst', encoding="utf8") as f:
        return f.read()

setup (name='mishkal', version='0.1',
      description="Mishkal: Arabic text diacritization library for Python",
      long_description = readme(),      

      author='Taha Zerrouki',
      author_email='taha.zerrouki@gmail.com',
      url='http://mishkal.sourceforge.net/',
      license='GPL',
      package_dir={'mishkal': 'mishkal'},
      packages=['mishkal'],
      install_requires=[ 'pyarabic>=0.6.2',
      ],         
      include_package_data=True,
      package_data = {
        'mishkal': ['doc/*.*','doc/html/*', 'data/*.sqlite', 'data/*.sql'],
        },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: End Users/Desktop',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          ],
    );

