from setuptools import setup

setup(
    name="python_plc_connection",
    version="0.1",
    packages=['python_plc_connection'],
    url='https://github.com/AhmedCemil/python_plc_connection',
    license='MIT',
    author="Ahmed Cemil Bilgin",
    author_email="ahmed.c.bilgin@gmail.com",
    description="Python PLC Connection Form Application",
    install_requires=[
        'Pillow',
        'pyads'
    ],
)
