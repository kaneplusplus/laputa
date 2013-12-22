try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='cnidaria',
    version='0.1',
    author='Michael J. Kane',
    author_email='kaneplusplus@gmail.com',
    packages=['cnidaria'],
#    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
#    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Distributed computing with Redis.',
    long_description=open('README.md').read(),
    install_requires=["argparse", "redis"]
#        "Django >= 1.1.1",
#        "caldav == 0.1.4",
#    ],
)
