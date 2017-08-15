import setuptools 

setuptools.setup(
    name='mgrslib',
    license='MIT',
    author='Peter E Lenz',
    author_email='pelenz@pelenz.com',
    install_requires=[['mgrs','nvector' ]],
    version='0.0.1',
    packages=setuptools.find_packages(['mgrs','nvector']),
    description='Geodetic operations in MGRS space for Data Scientists',
    url=' http://pelenz.com/mgrslib/'
    long_description=""
)
