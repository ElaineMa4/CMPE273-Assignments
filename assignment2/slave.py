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
        real_queue = self.stub.getConnection(Datastore_pb2.ConnectionRequest())
        for element in real_queue:
            if element.operation == 'put':
                key = element.key.encode()
                value = element.value.encode()                
                print("in slave, put {} : {} ".format(key, value))
                self.db.put(key, value)
            elif element.operation == 'delete':
                d_key = element.key.encode()
                print("in slave, delete {} ".format(d_key))
                self.db.delete(d_key)
            elif element.operation == 'get':
                print("in slave, get {} : {}".format(element.key,v))
                value = self.db.get(element.key.encode())         
            else:
                print("in slave, wrong operation!")
                pass

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