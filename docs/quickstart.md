# Quickstart

## Requirements
- Python >= 3.7
- An instance of the [Geocube Server](https://www.github.com/airbusgeo/geocube), its url and, depending on the configuration, its ApiKey

## Installation
```bash
pip install git+https://github.com/airbusgeo/geocube-client-python.git
```

## Connect to the server
Start a python console and type
```python
import geocube
import os

client = geocube.Client("127.0.0.1:8080")
# Or
client = geocube.Client(os.environ['GEOCUBE_SERVER'], True, os.environ['GEOCUBE_CLIENTAPIKEY'])
```
You are connected !

Then, you can do the [tutorials](user-guide/tutorials.md) to learn how to feed the geocube, access and optimize the data.

