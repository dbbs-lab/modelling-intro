import numpy as np
import plotly.graph_objs as go


def dudt(u, tau_f, U, n_spikes):
    return -u / tau_f + U * (1 - u) * n_spikes


def dxdt(x, tau_d, u, n_spikes):
    return (1 - x) / tau_d - u * x * n_spikes


def dIdt(I, tau_s, A, u, x, n_spikes):
    return -I / tau_s + A * u * x * n_spikes


# State variables
t = 0
x = 1
u = 0
I = 0

# Constants
tmax = 0.3
dt = 0.001
A = 1
U = 0.45
tau_s = 20
tau_d = 750
tau_f = 50
spike_times = [0.02, 0.085, 0.15, 0.2, 0.23]

spike_iter = iter(np.histogram(spike_times, int(tmax // dt) + 2, range=(0, tmax))[0])

rt, rn, ru, ri, rx = [0], [0], [0], [0], [1]
while t < tmax:
    n_spikes = next(spike_iter)
    u += dudt(u, tau_f, U, n_spikes)
    I += dIdt(I, tau_s, A, u, x, n_spikes)
    x += dxdt(x, tau_d, u, n_spikes)
    t += dt
    rt.append(t)
    rn.append(n_spikes)
    ru.append(u)
    ri.append(I)
    rx.append(x)

go.Figure(
    [
        go.Scatter(x=rt, y=ru, name="u"),
        go.Scatter(x=rt, y=rx, name="x"),
        go.Scatter(x=rt, y=ri, name="i"),
    ]
).write_html("result.html")
