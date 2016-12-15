import setuptools 


long_description = ""
requirements=[['mgrs','nvector' ]]


setuptools.setup(
    name='mgrslib',
    license='MIT',
    author='Peter E Lenz',
    author_email='pelenz@pelenz.com',
    install_requires=requirements,
    version='0.0.1',
    packages=setuptools.find_packages(),
    description=' Mgrslib is a python library that greatly simplifies doing geodetic operations in MGRS space',
    long_description=long_description
)
