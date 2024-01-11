import numpy as np
import plotly.graph_objs as go

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

# Bin the spikes into dt-wide bins with numpy's histogram function.
spike_bin = iter(np.histogram(spike_times, int(tmax // dt) + 2, range=(0, tmax))[0])

rt, rn, ru, ri, rx = [0], [0], [0], [0], [1]
while t < tmax:
    n_spikes = next(spike_bin)
    # Solve the timestep
    u += -u / tau_f * dt + U * (1 - u) * n_spikes
    I += -I / tau_s * dt + A * u * x * n_spikes
    x += (1 - x) / tau_d * dt - u * x * n_spikes
    t += dt
    # Store timestep results
    rt.append(t)
    rn.append(n_spikes)
    ru.append(u)
    ri.append(I)
    rx.append(x)

# Plot results
go.Figure(
    [
        go.Scatter(x=rt, y=ru, name="u"),
        go.Scatter(x=rt, y=rx, name="x"),
        go.Scatter(x=rt, y=ri, name="i"),
    ]
).write_html("lecture1.html")
