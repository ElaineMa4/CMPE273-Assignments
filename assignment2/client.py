import grpc
import datastore_pb2
import argparse

PORR = 3000
DEFAULT_VALUE = ""

class MyClient():
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = Datastore_pb2.DatastoreStub(self.channel)

    def test(self, operation, key, value = DEFAULT_VALUE):
        return self.stub.operation(Datastore_pb2.Request(operation = operation, key = key, value = value))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number")
    args = parser.parse_args()
    print("Client is connecting to Server at {}:{}...".format(args.host, PORT))
    client = MyClient(host=args.host)

    key = '1'
    value = 'foo'
    
    print("## PUT Request: value = " + value) 
    res = client.test('put', key, value)
    print("## PUT Response: " + res.data)

    print("## GET Request: key = " + key) 
    res = client.test('get', key)
    print("## GET Response: " + res.data)

    print("## DELETE Request: key = " + key) 
    res = check.db_operation('delete', key)
    print("## DELETE Response: " + res.data)


if __name__ == "__main__":
    main()