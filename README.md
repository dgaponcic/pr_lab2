# protocol stack
Work in progress
## Task
Implement a protocol stack.
* a transport protocol based on UDP
* a session-level security protocol inspired by SSL/TLS

## Overview
More details on master branch. 

The protocol stack:
* is build on top of UDP sockets
* allocates new ports for connections
* has packet splitting and in order delivery 
* has congestion Control
* implements Diffie Hellman to compute private key for encryption


## Docker
In order to have access to the interactive terminal I start the container with a dummy infinite loop as the main process and use 

```docker exec -it server bash``` 
to start an interactive shell inside the container and start client.py or server.py from there.

I use tc in order to corrupt the network.

* ```tc qdisc add dev eth0 root netem loss 1%```

* ```tc qdisc add dev eth0 root netem delay 100ms```


The application can recover for a loss of packets of up to 7% or a delay of up to 100ms, but there can happen unhandled cases.

