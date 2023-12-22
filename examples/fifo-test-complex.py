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
    return 10

def packet_arrival_2():
    return 9

def packet_arrival_3():
    return 8

def packet_arrival_4():
    return 7

def packet_arrival_5():
    return 6

def packet_arrival_6():
    return 5

def packet_arrival_7():
    return 4

def packet_arrival_8():
    return 3

def packet_arrival_9():
    return 2

def packet_arrival_10():
    return 1


def const_size_1():
    return 8000.0

def const_size_2():
    return 7000.0

def const_size_3():
    return 6000.0

def const_size_4():
    return 5500.0

def const_size_5():
    return 5000.0

def const_size_6():
    return 4000.0

def const_size_7():
    return 3000.0

def const_size_8():
    return 2500.0

def const_size_9():
    return 2000.0

def const_size_10():
    return 1000.0


env = simpy.Environment()
pg1 = DistPacketGenerator(env,
                          "flow_0",
                          packet_arrival_1,
                          const_size_1,
                          initial_delay=1,
                          finish=101,
                          flow_id=0,
                          debug=False)
pg2 = DistPacketGenerator(env,
                          "flow_1",
                          packet_arrival_2,
                          const_size_2,
                          initial_delay=0.9,
                          finish=100.9,
                          flow_id=1,
                          debug=False)
pg3 = DistPacketGenerator(env,
                          "flow_2",
                          packet_arrival_3,
                          const_size_3,
                          initial_delay=0.8,
                          finish=100.8,
                          flow_id=2,
                          debug=False)
pg4 = DistPacketGenerator(env,
                          "flow_3",
                          packet_arrival_4,
                          const_size_4,
                          initial_delay=0.7,
                          finish=100.7,
                          flow_id=3,
                          debug=False)
pg5 = DistPacketGenerator(env,
                          "flow_4",
                          packet_arrival_5,
                          const_size_5,
                          initial_delay=0.6,
                          finish=100.6,
                          flow_id=4,
                          debug=False)
pg6 = DistPacketGenerator(env,
                          "flow_5",
                          packet_arrival_6,
                          const_size_6,
                          initial_delay=0.5,
                          finish=100.5,
                          flow_id=5,
                          debug=False)
pg7 = DistPacketGenerator(env,
                          "flow_6",
                          packet_arrival_7,
                          const_size_7,
                          initial_delay=0.4,
                          finish=100.4,
                          flow_id=6,
                          debug=False)
pg8 = DistPacketGenerator(env,
                          "flow_7",
                          packet_arrival_8,
                          const_size_8,
                          initial_delay=0.3,
                          finish=100.3,
                          flow_id=7,
                          debug=False)
pg9 = DistPacketGenerator(env,
                          "flow_8",
                          packet_arrival_9,
                          const_size_9,
                          initial_delay=0.2,
                          finish=100.2,
                          flow_id=8,
                          debug=False)
pg10 = DistPacketGenerator(env,
                          "flow_9",
                          packet_arrival_10,
                          const_size_10,
                          initial_delay=0.1,
                          finish=100.1,
                          flow_id=9,
                          debug=False)
ps = PacketSink(env)


port_rate = 80000  # in bits
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
pg3.out = switch
pg4.out = switch
pg5.out = switch
pg6.out = switch
pg7.out = switch
pg8.out = switch
pg9.out = switch
pg10.out = switch
switch.demux.fib = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
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
            print(ps.arrivals[f][i], end=", ") 
    print("")