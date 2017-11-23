'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import datastore_pb2
import argparse
import rocksdb

PORT = 3000
SEC = 20

class MySlave():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)
        self.db = rocksdb.DB("slave.db", rocksdb.Options(create_if_missing=True))

    def get_update(self):
        print("in slave get_update")
        real_queue = self.stub.init_connection(datastore_pb2.UpdateReq())
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
                print("in slave, get {} : {}".format(element.key, value))
                value = self.db.get(element.key.encode())         
            else:
                print("in slave, wrong operation!")
                pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="slave")
    args = parser.parse_args()    
    slave = MySlave(host=args.host)
    res = slave.get_update()

if __name__ == '__main__':
    main()