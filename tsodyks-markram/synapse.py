import dataclasses
import os, sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from simulator import Component


@dataclasses.dataclass
class TsodyksMarkramSynapse(Component):
    A: float
    U: float
    tau_f: float
    tau_d: float
    tau_s: float
    spikes: list[float] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.u: float = 0
        self.x: float = 1
        self.I: float = 0
        self.t: float = 0

    def init(self, t0):
        self.__post_init__()
        self._spike_buffer = np.array(self.spikes) - t0

    def step(self, dt):
        self._flush_spikes(dt)
        self.u += self.du(dt)
        self.I += self.dI(dt)
        self.x += self.dx(dt)

    def du(self, dt):
        return -self.u / self.tau_f * dt + self.U * (1 - self.u) * self._n_spikes

    def dx(self, dt):
        return (1 - self.x) / self.tau_d * dt - self.u * self.x * self._n_spikes

    def dI(self, dt):
        return -self.I / self.tau_s * dt + self.A * self.u * self.x * self._n_spikes

    def _flush_spikes(self, dt):
        pre = len(self._spike_buffer)
        self._spike_buffer = self._spike_buffer[self._spike_buffer > dt] - dt
        self._n_spikes = pre - len(self._spike_buffer)

    def u_monitor(self):
        return self.u

    def x_monitor(self):
        return self.x

    def I_monitor(self):
        return self.I
