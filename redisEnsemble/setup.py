from distutils.core import setup

setup(
    name='redisEnsemble',
    version='0.1',
    author='Michael J. Kane',
    author_email='kaneplusplus@gmail.com',
    packages=['redisEnsemble'],
#    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
#    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Ensemble learners with Redis.',
    long_description=open('README.txt').read()
#    install_requires=[
#        "Django >= 1.1.1",
#        "caldav == 0.1.4",
#    ],
)
