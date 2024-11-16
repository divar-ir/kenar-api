from setuptools import setup, find_packages

setup(
    name='Kenar',
    version='0.6.0',
    author='Kenar',
    author_email='kenar@divar.ir',
    description='facilitate using kenar divar APIs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/divar-ir/kenar-api',
    packages=find_packages(),
    install_requires=[
        'httpx >= 0.26.0',
        'pydantic >= 2.6.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
