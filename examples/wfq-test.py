"""
An example of using the Weighted Fair Queueing (WFQ) scheduler.
"""
from functools import partial
from random import expovariate


import simpy
from ns.packet.dist_generator import DistPacketGenerator
from ns.packet.sink import PacketSink
from ns.scheduler.monitor import ServerMonitor
from ns.scheduler.wfq import WFQServer


def packet_arrival_1():
    return 2.0

def packet_arrival_2():
    return 1.0

def const_size_1():
    return 2000.0

def const_size_2():
    return 1000.0

env = simpy.Environment()
pg1 = DistPacketGenerator(env,
                          "flow_0",
                          packet_arrival_1,
                          const_size_1,
                          initial_delay=0.5,
                          finish=10.5,
                          flow_id=0,
                          debug=False)
pg2 = DistPacketGenerator(env,
                          "flow_1",
                          packet_arrival_2,
                          const_size_2,
                          initial_delay=1.0,
                          finish=11,
                          flow_id=1,
                          debug=False)
ps = PacketSink(env)

source_rate = 8000.0
wfq_server = WFQServer(env, source_rate, [1, 2], debug=False)
monitor = ServerMonitor(env,
                        wfq_server,
                        partial(expovariate, 0.1),
                        pkt_in_service_included=True)


pg1.out = wfq_server
pg2.out = wfq_server

wfq_server.out = ps

env.run(until=100)

for f in range(len(ps.arrivals)):
    for i in range(len(ps.arrivals[f])):
        if i % 2 == 0:
            print(ps.arrivals[f][i], end=", ") 
    print("")