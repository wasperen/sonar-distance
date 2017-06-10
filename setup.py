from distutils.core import setup

setup(
    name='sonar-distance',
    version='0.1',
    packages=[''],
    url='https://github.com/wasperen/sonar-distance',
    license='MIT',
    author='wasperen',
    author_email='willem@van.asperen.org',
    install_requires=[
        'pigpio',
    ],
    description='A python module to use a duo of SRF04 sonar sensors to measure distance on a Raspberry PI'
)
