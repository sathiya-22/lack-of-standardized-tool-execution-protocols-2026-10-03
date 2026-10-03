from setuptools import setup, find_packages

setup(
    name='agenttoolkit',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pydantic>=2.0',
        'pydantic-settings',
        'httpx',
        'anyio',
    ],
    author='AutoScout',
    description='Standardized Tool Execution Protocols for Agentic AI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your-org/agenttoolkit', # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.9',
)
