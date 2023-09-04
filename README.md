# Geocube Python Client Library

Geocube Python Client Library is delivered as an example of Geocube Client.

## Installation

### Package
```bash
pip install git+https://github.com/airbusgeo/geocube-client-python.git
```

### Docker with a Geocube Downloader embedded
```bash
docker build -f docker/Dockerfile.geocube-client-downloader -t geocube-client-downloader:latest .
```

## Quickstart

### Requirements
- Python >= 3.7
- An instance of the Geocube Server, its url and, depending on the configuration, its ApiKey

### Feed the Geocube - Indexation

Please follow the [Data Indexation Jupyter notebook](https://github.com/airbusgeo/geocube-client-python/Jupyter/Geocube-Client-DataIndexation.ipynb)

### Access to the Geocube

Please follow the [Data Access Jupyter notebook](https://github.com/airbusgeo/geocube-client-python/Jupyter/Geocube-Client-DataAccess.ipynb)

### Optimize the dataformat (Consolidation)

Please follow the [Consolidation Jupyter notebook](https://github.com/airbusgeo/geocube-client-python/Jupyter/Geocube-Client-Consolidation.ipynb)

### Scale-up

Please follow the [SDK Jupyter notebook](https://github.com/airbusgeo/geocube-client-python/Jupyter/Geocube-Client-SDK.ipynb)

## Documentation

Available as docstrings in source code.

## Status

Geocube-Client-Python is under development. The API might evolve in backwards incompatible ways until essential functionality is covered.

## Update GRPC Interface

Geocube-Client-Python uses the protobuf GRPC interface, automatically generated from the protobuf files provided by [the Geocube](https://github.com/airbusgeo/geocube/api/v1/pb).

The `pb` files can be generated using the package `grpcio-tools`, the geocube [protobuf folder](https://github.com/airbusgeo/geocube/api/v1/) and the following commands:

```bash
sed -i "s/import \"pb/import \"geocube\/pb/g" <temp folder>/geocube/pb/*.proto
python3 -m grpc_tools.protoc -I <temp folder> -I ../geocube/api/v1/ --python_out=. geocube/pb/geocube.proto geocube/pb/catalog.proto geocube/pb/records.proto geocube/pb/dataformat.proto geocube/pb/variables.proto geocube/pb/layouts.proto geocube/pb/operations.proto
python3 -m grpc_tools.protoc -I <temp folder> -I ../geocube/api/v1/ --grpc_python_out=. geocube/pb/geocube.proto
python3 -m grpc_tools.protoc -I <temp folder> -I ../geocube/api/v1/ --python_out=. --grpc_python_out=. geocube/pb/admin.proto
```

## Contributing

Contributions are welcome. Please read the [contributing guidelines](https://github.com/airbusgeo/geocube-client-python/CONTRIBUTING.MD) before submitting fixes or enhancements.

## Licensing

Geocube-Client-Python is licensed under the Apache License, Version 2.0. See [LICENSE](https://github.com/airbusgeo/geocube-client-python/LICENSE) for the full license text.

## Credits

Geocube is a project under development by [Airbus DS Geo SA](http://www.intelligence-airbusds.com) with the support of [CNES](http://www.cnes.fr).
