# Update GRPC Interface

Geocube-Client-Python uses the protobuf GRPC interface, automatically generated from the protobuf files provided by [the Geocube](https://github.com/airbusgeo/geocube/api/v1/pb).

The `pb` files can be generated using the package `grpcio-tools`, the geocube [protobuf folder](https://github.com/airbusgeo/geocube/api/v1/) and the following commands:

```bash
sed -i "s/import \"pb/import \"geocube\/pb/g" <temp folder>/geocube/pb/*.proto
python3 -m grpc_tools.protoc -I <temp folder> -I ../geocube/api/v1/ --python_out=. geocube/pb/geocube.proto geocube/pb/catalog.proto geocube/pb/records.proto geocube/pb/dataformat.proto geocube/pb/variables.proto geocube/pb/layouts.proto geocube/pb/operations.proto
python3 -m grpc_tools.protoc -I <temp folder> -I ../geocube/api/v1/ --grpc_python_out=. geocube/pb/geocube.proto
python3 -m grpc_tools.protoc -I <temp folder> -I ../geocube/api/v1/ --python_out=. --grpc_python_out=. geocube/pb/admin.proto
```

