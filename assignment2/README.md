# Master-Slave Replication
## Instruction
**Initialize bridge**: `docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet`

**Compile GRPC**: `docker run -it --rm --name grpc-tools -v "$PWD":/path/to/assignment2 -w /path/to/assignment2 assignment2 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto`

**Run master node**: `docker run -p 3000:3000 -it --rm --name master-node -v "$PWD":/path/to/assignment2 -w /path/to/assignment2 assignment2 python3.6 master.py`

**Run slave node**: `docker run -it --rm --name slave-node -v "$PWD":/path/to/assignment2 -w /path/to/assignment2 assignment2 python3.6 slave.py 192.168.0.1`

**Run client**: `docker run -it --rm --name client -v "$PWD":/path/to/assignment2 -w /path/to/assignment2 assignment2 python3.6 client.py 192.168.0.1`



## Technologies
### Master
1. generator for sending requests to slave
2. decorator for recording incoming requests from client and processing those requests
### Slave
Keep checking if master has update
