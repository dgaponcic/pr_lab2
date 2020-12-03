# protocol stack

## Task
Implement a protocol stack.
* transport protocol based on UDP
* session-level security protocol inspired by SSL/TLS
* application-level protocol

## Transport protocol
Built on UDP sockets.

In order to communicate, the client has to connect to some address and the server has to listen for incoming clients and accept them.

When a client has requested to connect, a new port is opened for the connection.



#### Packet splitting and in order delivery 
The information is splitted into packets and every packet has a index in order to reassemble the message when read.

#### Congestion Control
To ensure congestion control used Slow Start method.
Window variable denotes how many packets can be sent without getting an acknowledgement. The initial value of window is 1. For every ACK
if window is smaller than ssthresh(an average nb of packets to be sent) than we increase window rapidly, if is greater than increase slow. (in the repository 
increase with 1 and 0.5 respectively). For every NACK window is decreased by 1/3. 
So is the network is congested and we receive NACKs, we send fewer packets, if everything is fine we increase the value.

```
      while True:
        payload, addr = sender.recvfrom(1024, socket.MSG_DONTWAIT)
        packet = get_packet(payload)

        if packet["type"] == "CONTROL" and packet["data"] == "NACK":
          index = packet["index"]
          sender.sendto(data2send[index], receiver)
          window *= 2 / 3

        elif packet["type"] == "CONTROL" and packet["data"] == "ACK":
          index = packet["index"]
          if index in waiting:
            waiting.remove(index)
          window = window + 1 if window < ssthresh else window + 0.5
```

## Session level
Implemented Diffie Helman is used in order to get the private key for 
encryption (use data sent on network together with some private values and some smart modulo math).

```
def calculate_key(public_g, public_p, private):
  sympy_exp = parse_expr('(a ** b) % c')
  return int(sympy_exp.evalf(subs={a:public_g, b:private, c:public_p}))
```



## Application level

A protocol based on the state machine of a stationary telephone.

TODO: draw state machine

## Demo
TODO: demo

## Extra notes
Improvements and/or Known bugs:
* Vulnerable to SYN flood
