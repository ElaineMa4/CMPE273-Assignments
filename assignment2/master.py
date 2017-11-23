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
sample_data = { "1" : "abc", "2" : "def", "3" : "wxyz"}

# MyDatastoreServicer
class MasterServicer(datastore_pb2.DatastoreServicer):
    def __init__(self):
        self.db = rocksdb.DB("master.db", rocksdb.Options(create_if_missing=True))

    def decorator(my_func):
        def wrapper(self, request, context):
            operation=request.operation
            key=request.key.encode()
            value=request.value.encode()
            # init operation
            operation = Datastore_pb2.UpdateInfo(operation, key, value) 
            self.connection_queue.put(operation)
            return my_func(self, request, context)
        return wrapper
    
    @decorator
    def operation(self, request, context):
        if request.operation == 'put':
            self.db.put(request.key.encode(), request.value.encode())
            return Datastore_pb2.Response(data='put success : {}'.format(request.key))
        elif request.operation == 'delete':
            self.db.delete(request.key.encode())
            return Datastore_pb2.Response(data='delete success : {}'.format(request.key))
        elif request.operation == 'get':
            value = self.db.get(request.key.encode())
            return Datastore_pb2.Response(data='get success : {} : {}'.format(request.key, value))
        else:
            print("wrong operation")
            return Datastore_pb2.Response(data='wrong operatio')

    def init_connection(self, request, context):
            print('slave connected to master...')
            while True:            
                value_queue = self.connection_queue.get()
                print('Got a request to perform {} operation'.format(value_queue.operation))
                yield value_queue


def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
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