import dataclasses

import glia
from glia import MechAccessor
from patch import p

from . import Component


@dataclasses.dataclass
class Compartment(Component):
    L: float
    r: float
    Ra: float
    Cm: float = 1.0
    Vrest: float = -65

    def __post_init__(self):
        self._inputs = []
        self._sec = p.Section()
        self._sec.nseg = 1
        self._sec.insert("pas")
        self._sec.insert("hh")
        self._bridge: MechAccessor = glia.insert(self._sec, "bridge")
        self._sec(0.5).pas.e = self.Vrest
        self._update_sec()

    def _update_sec(self):
        self._sec.L = self.L
        self._sec.diam = self.r * 2
        self._sec.Ra = self.Ra
        self._sec.Cm = self.Cm

    def init(self, t0, dt, tmax):
        self._sec(0.5).v = self.Vrest
        p.t = t0

    def step(self, dt):
        p.dt = dt
        self.set_input(sum(input.output() for input in self._inputs))
        p.run(p.t + dt, reset=False)

    def connect(self, dep):
        self._inputs.append(dep)

    def set_input(self, i):
        self._bridge.set_parameter("ii", i)

    def monitor_vm(self):
        return self._sec(0.5).v
