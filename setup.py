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
    version="0.0.3",
    author="Varoquaux Vincent",
    author_email="vincent.varoquaux[at]]airbus.com",
    description="Geocube Python Client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://code.webfactory.intelligence-airbusds.com/geocube/geocube-client-python",
    packages=['geocube', 'geocube.utils', 'geocube.pb', 'geocube.entities'],
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
