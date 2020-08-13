#!/usr/bin/python
# -*- coding=utf-8 -*-
from setuptools import setup

# to install type:
# python setup.py install --root=/
from io import open
def readme():
    with open('README.rst', encoding="utf8") as f:
        return f.read()

setup (name='mishkal', version='0.4',
      description="Mishkal: Arabic text diacritization library for Python",
      long_description = readme(),      

      author='Taha Zerrouki',
      author_email='taha.zerrouki@gmail.com',
      url='http://mishkal.sourceforge.net/',
      license='GPL',
      package_dir={'mishkal': 'mishkal'},
      packages=['mishkal'],
      install_requires=["libqutrub>=1.0",
            "naftawayh>=0.2",
            "pyarabic>=0.6.2",
            "tashaphyne>=0.3.1",
            "arramooz-pysqlite>=0.1",
            "qalsadi>=0.2",
            "mysam-tagmanager>=0.1",
            "alyahmor>=0.1",
            "asmai>=0.1",
            "sylajone>=0.1",
            "maskouk-pysqlite>=0.1",
            'pickledb>=0.9.0',
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

