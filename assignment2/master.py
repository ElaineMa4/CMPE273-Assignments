'''
################################## server.py #############################
# Lab1 gRPC RocksDB Server 
################################## server.py #############################
'''
import time
import grpc
import datastore_pb2
import datastore_pb2_grpc
import uuid
import rocksdb

import queue
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyDatastoreServicer(datastore_pb2.DatastoreServicer):
    def __init__(self):
        self.my_queue = queue.Queue()
        self.db = rocksdb.DB("master.db", rocksdb.Options(create_if_missing=True))

    def decorator(my_func):
        def wrapper(self, request, context):
            print("in wrapper")
            operation = request.operation
            key = request.key.encode()
            value = request.value.encode()
            # init operation
            operation = datastore_pb2.UpdateInfo(operation=operation, key=key, value=value) 
            self.my_queue.put(operation)
            return my_func(self, request, context)
        return wrapper
    
    @decorator
    def update(self, request, context):
        print("master in update")
        if request.operation == 'put':
            key = request.key.encode()
            value = request.value.encode()
            self.db.put(key, value)
            return datastore_pb2.Response(data='put success : {}'.format(request.key))
        elif request.operation == 'delete':
            d_key = request.key.encode()
            self.db.delete(d_key)
            return datastore_pb2.Response(data='delete success : {}'.format(request.key))
        elif request.operation == 'get':
            g_key = request.key.encode()
            value = self.db.get(g_key)
            return datastore_pb2.Response(data='get success : {} : {}'.format(request.key, value))
        else:
            print("wrong operation!")
            return datastore_pb2.Response(data='wrong operation!')

    def init_connection(self, request, context):
        print('slave connected to master...')
        while True: 
            if self.my_queue.qsize() != 0:
                real_queue = self.my_queue.get()
                yield real_queue
                


def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    datastore_pb2_grpc.add_DatastoreServicer_to_server(MyDatastoreServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)