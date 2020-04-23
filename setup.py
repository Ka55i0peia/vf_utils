import os
import sys

from setuptools import setup

name = 'Jan Gietzel'
mail = 'jan.gietzel@gmail.com'
__author__ = f'{name} <{mail}>'


with open('readme.md') as readme_file:
    long_description = readme_file.read()


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()
elif sys.argv[-1] == 'clean':
    import shutil
    if os.path.isdir('build'):
        shutil.rmtree('build')
    if os.path.isdir('dist'):
        shutil.rmtree('dist')
    if os.path.isdir('vf_utils.egg-info'):
        shutil.rmtree('vf_utils.egg-info')


setup(
    name="vf_utils",
    version="0.1.0",
    author=name,
    author_email=mail,
    description="Doing bulk edit jobs for vereinsflieger.de",
    license="MIT",
    keywords="vereinsflieger.de",
    url="https://github.com/Ka55i0peia/vf_utils",
    packages=['bulk_edit'],
    long_description_content_type='text/markdown',
    long_description=long_description,
    python_requires='>=3',
    install_requires=[
          'selenium>=3.141.0',
          'argparse>=1.4.0'
    ]
)