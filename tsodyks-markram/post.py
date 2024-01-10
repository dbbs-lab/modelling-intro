import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from synapse import TsodyksMarkramSynapse
from simulator import Simulator

syn = TsodyksMarkramSynapse(
    A=1,
    U=0.45,
    tau_s=0.020,
    tau_d=0.750,
    tau_f=0.050,
    spikes=[0.02, 0.085, 0.15, 0.2, 0.23],
)

sim = Simulator()
sim.add_component(syn)
sim.add_monitor("u", syn.u_monitor)
sim.add_monitor("x", syn.x_monitor)
sim.add_monitor("I", syn.I_monitor)

sim.run(0, 0.3, 0.001)
sim.save("sim2.html")
