#!/usr/bin/env python3
'''
unalignedrop finds unaligned rop gadgets in x86 x64 x86_64
'''
import os
from setuptools import setup, find_packages

# Get the version
with open(os.path.join('unalignedrop', 'version.py'), 'rb') as fd:
    VERSION = fd.read().decode('utf-8').split()[-1].replace('\'', '')

# Find all of the console scripts
CONSOLE_SCRIPTS = []
for filename in os.listdir(os.path.join('unalignedrop', 'cli')):
    if not '__init__' in filename and '.py' in filename:
        filename = filename.replace('.py', '')
        CONSOLE_SCRIPTS.append('%s=%s:main' %
                               (filename, 'unalignedrop.cli.' + filename))

setup(
    name='unalignedrop',
    packages=find_packages(),
    version=VERSION,
    data_files=[('', ['LICENSE.md']), ],
    entry_points={'console_scripts': CONSOLE_SCRIPTS},
    scripts=[os.path.join('bin', s) for s in os.listdir('bin')],
    description='Find unaligned rop gadgets in x86 x64 x86_64',
    author='John Andersen',
    author_email='johnandersenpdx@gmail.com',
    url='https://github.com/pdxjohnny/unalignedrop',
    download_url='https://github.com/pdxjohnny/unalignedrop/tarball/%s' % VERSION,
    license='GPLv3, see LICENSE.md',
    classifiers=[
        'Topic :: Security',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers'
    ]
)
