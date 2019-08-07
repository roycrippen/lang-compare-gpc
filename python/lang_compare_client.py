import logging

import grpc

import lang_compare_pb2
import lang_compare_pb2_grpc


def run():
    port_python = 'localhost:50052'
    print("Connecting to python lang-compare server at: {}".format(port_python))
    channel_python = grpc.insecure_channel(port_python)
    stub_python = lang_compare_pb2_grpc.LangCompareStub(channel_python)

    port_cpp = 'localhost:50051'
    print("Connecting to C++    lang-compare server at: {}".format(port_cpp))
    channel_cpp = grpc.insecure_channel(port_cpp)
    stub_cpp = lang_compare_pb2_grpc.LangCompareStub(channel_cpp)

    key = "my key"
    num = 1000
    print("calling python then C++ xor_cipher {} times".format(num * 2))
    decrypted = ""
    for i in range(num):
        in_str = "message{0:05d}".format(i)
        response_python = stub_python.XorCipher(lang_compare_pb2.XorCipherRequest(in_str=in_str, key=key))
        response_cpp = stub_cpp.XorCipher(lang_compare_pb2.XorCipherRequest(in_str=response_python.out_str, key=key))
        decrypted = response_cpp.out_str
        assert (decrypted == in_str)

    print("last decrypted string: '{}'".format(decrypted))


if __name__ == '__main__':
    logging.basicConfig()
    run()