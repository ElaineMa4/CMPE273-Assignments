import grpc
import datastore_pb2
import argparse

PORR = 3000

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number")
    args = parser.parse_args()
    print("Client is connecting to Server at {}:{}...".format(args.host, PORT))
    client = DatastoreClient(host=args.host)
    
    value = 'foo'
    print("## PUT Request: value = " + value) 
    resp = client.put(value)
    key = resp.data
    print("## PUT Response: key = " + key)

    print("## GET Request: key = " + key) 
    resp = client.get(key)
    print("## GET Response: value = " + resp.data) 


if __name__ == "__main__":
    main()