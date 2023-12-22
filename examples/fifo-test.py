"""
An very simple example of using the test the packet drop in FairPacketSwitch.
It shows a bug in packet dropping process.
"""
import simpy
from ns.packet.dist_generator import DistPacketGenerator
from ns.packet.sink import PacketSink
from ns.switch.switch import SimplePacketSwitch

def truncate(n, decimals=0):
    multiplier = 10**decimals
    return int(n * multiplier) / multiplier

def packet_arrival_1():
    return 2

def packet_arrival_2():
    return 1



def const_size_1():
    return 2000

def const_size_2():
    return 1000


env = simpy.Environment()
pg1 = DistPacketGenerator(env,
                          "flow_0",
                          packet_arrival_1,
                          const_size_1,
                          initial_delay=0.5,
                          finish=100.5,
                          flow_id=0,
                          debug=False)
pg2 = DistPacketGenerator(env,
                          "flow_1",
                          packet_arrival_2,
                          const_size_2,
                          initial_delay=1.0,
                          finish=101,
                          flow_id=1,
                          debug=False)

ps = PacketSink(env)


port_rate = 8000  # in bits
buffer_size = 1100  # in bytes

switch = SimplePacketSwitch(
    env,
    nports=1,
    port_rate=port_rate,
    buffer_size=buffer_size,
    debug=False,
)
# switch.egress_ports[0].limit_bytes = True
pg1.out = switch
pg2.out = switch
switch.demux.fib = {0: 0, 1: 0}
switch.ports[0].out = ps

env.run()

# print("At the packet sink, packet arrival times for flow 0 are:")
# for i in range(len(ps.arrivals[0])):
#     print(truncate(ps.arrivals[0][i]), end=", ") 

# print("At the packet sink, packet arrival times for flow 1 are:")
# for i in range(len(ps.arrivals[1])):
#     print(truncate(ps.arrivals[1][i]), end=", ") 

for f in range(len(ps.arrivals)):
    for i in range(len(ps.arrivals[f])):
        if i % 2 == 0:
            print(truncate(ps.arrivals[f][i]), end=", ") 
    print("")