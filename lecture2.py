from pathlib import Path

from neuron import h

h.nrnmpi_init()

from simulator import Simulator
from simulator.tsodyks_markram import TsodyksMarkramSynapse
from simulator.cable import Compartment

syn = TsodyksMarkramSynapse(
    A=1,
    U=0.45,
    tau_s=0.020,
    tau_d=0.750,
    tau_f=0.050,
    spikes=[0.02, 0.85, 1.15, 2, 2.3],
)

pas = Compartment(L=100, r=1, Ra=35.2, Vrest=-65)
pas.connect(syn)


sim = Simulator()
sim.add_component(syn)
sim.add_monitor("u", syn.u_monitor)
sim.add_monitor("x", syn.x_monitor)
sim.add_monitor("I", syn.I_monitor)
sim.add_component(pas)
sim.add_monitor("Vm", pas.monitor_vm)

sim.run(0, 10, 0.001)
sim.save(Path(__file__).resolve().with_suffix(".html"))
