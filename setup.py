from setuptools import setup, find_packages

setup(
    name='mymemory',
    version='0.0.1',
    packages=find_packages(exclude='venv'),
    url='',
    license='MIT',
    author='kuronbo',
    author_email='kurinbo.i2o@gmail.com',
    description='web client with memoplat programs',
    install_requires=['flask',
                      'flask_bootstrap',
                      'flask_bootstrap4',
                      ]
)
