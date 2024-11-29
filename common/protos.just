set quiet := true

PROTO_SRC_DIR := source_directory() + "/src/protos"

PROTO_OUT_DIR := source_directory() + '/src/common/protobufs/'
PROTOC := "python -m grpc_tools.protoc"
PROTOC_GEN_MYPY := "python -m mypy_protobuf.main"

# Recipe to generate protos
generate_protos:
  find {{PROTO_SRC_DIR}} -name \*.proto -exec {{PROTOC}} \
    -I/usr/local/include \
    -I{{PROTO_SRC_DIR}} \
    --python_out={{PROTO_OUT_DIR}} \
    --grpc_python_out={{PROTO_OUT_DIR}} \
    --mypy_out={{PROTO_OUT_DIR}} \
    {} \;

