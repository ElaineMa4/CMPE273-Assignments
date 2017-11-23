import grpc
import datastore_pb2
import argparse


PORT = 3000
DEFAULT_VALUE = ""

class MyClient():
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)

    def test(self, operation, key, value):
        print("key : " + key)
        return self.stub.update(datastore_pb2.Request(operation=operation, key=key, value=value))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number")
    args = parser.parse_args()
    print("Client is connecting to Server at {}:{}...".format(args.host, PORT))
    client = MyClient(host=args.host)

    key = '1'
    value = 'foo'
    updated_value = 'bar'

    print("## PUT Request: value = " + value) 
    res = client.test('put', key, value)
    print("## PUT Response: " + res.data)

    print("## Change Request: value = " + value) 
    res = client.test('put', key, updated_value)
    print("## Change Response: " + res.data)

    print("## GET Request: key = " + key) 
    res = client.test('get', key, DEFAULT_VALUE)
    print("## GET Response: " + res.data)

    print("## DELETE Request: key = " + key) 
    res = client.test('delete', key, DEFAULT_VALUE)
    print("## DELETE Response: " + res.data)

    print("## GET Request: key = " + key) 
    res = client.test('get', key, DEFAULT_VALUE)
    print("## GET Response: " + res.data)


if __name__ == "__main__":
    main()