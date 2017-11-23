'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import datastore_pb2
import argparse

PORT = 3000
SEC = 20

class MySlave():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)
        self.db = rocksdb.DB("slave.db", rocksdb.Options(create_if_missing=True))

    def get_update(self):
        self.stub.


    def put(self, value):
        //TODO: put into db
        return self.stub.put(datastore_pb2.Request(data=value))

    def get(self, key):
        return self.stub.get(datastore_pb2.Request(data=key))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="the ip of the server")
    args = parser.parse_args()
    host=args.host
    print("Slave is connecting to Master at {}:{}...".format(args.host, MASTER_PORT))
    slave = MySlave(host)

    try:
        while True:
            time.sleep(SEC)
            slave.get_update()
    except KeyboardInterrupt:
        sys.exit("Stop sync slave!")

if __name__ == '__main__':
    main()