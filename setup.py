import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def parse_requirements(file):
    return sorted(set(
        line.partition('#')[0].strip()
        for line in open(os.path.join(os.path.dirname(__file__), file))
    ) - set(''))


setuptools.setup(
    name="geocube_client",
    version="1.0.1",
    author="Varoquaux Vincent",
    author_email="vincent.varoquaux[at]airbus.com",
    description="Geocube Python Client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/airbusgeo/geocube-client-python",
    packages=['geocube', 'geocube.utils', 'geocube.pb', 'geocube.entities', 'geocube.sdk'],
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Apache 2.0",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "xarray.backends": ["geocube=geocube.sdk.geocube_xarray:GeocubeBackendEntrypoint"],
    },
    python_requires='>=3.7',
)
