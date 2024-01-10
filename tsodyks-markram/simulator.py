import abc
from collections import defaultdict
from os import PathLike
from typing import Callable, Union
import plotly.graph_objs as go


class Component:
    @abc.abstractmethod
    def init(self, t0):
        pass

    @abc.abstractmethod
    def step(self, dt):
        pass


class Simulator:
    def __init__(self):
        self._components: list[Component] = []
        self._monitors: dict[str, Callable[[], float]] = {}
        self._measures: dict[str, list[float]] = defaultdict(list)
        self._time: list[float] = []

    def add_component(self, component: Component):
        self._components.append(component)

    def add_monitor(self, name: str, monitor: Callable[[], float]):
        self._monitors[name] = monitor

    def run(self, t0: float, tmax: float, dt: float):
        self.init(t0)
        t = t0
        while t < tmax:
            self._step(dt)
            t += dt
            self._measure(t)

    def init(self, t0: float):
        # Reset
        self._time = []
        self._measures = defaultdict(list)
        # Init
        for component in self._components:
            component.init(t0)
        self._measure(t0)

    def _step(self, dt: float):
        for component in self._components:
            component.step(dt)

    def _measure(self, t: float):
        self._time.append(t)
        for name, monitor in self._monitors.items():
            self._measures[name].append(monitor())

    def save(self, filename: Union[str, PathLike]):
        go.Figure(
            [
                go.Scatter(x=self._time, y=measures, name=name)
                for name, measures in self._measures.items()
            ]
        ).write_html(filename)
