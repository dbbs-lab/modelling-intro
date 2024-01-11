from collections import defaultdict

import plotly.graph_objs as go


def store(state, **kwargs):
    for k, v in kwargs.items():
        state[k].append(v)


def f(x, dt):
    return x * dt


def bin_spikes(spikes, t0, tmax, dt):
    n_bins = int((tmax - t0) // dt + 3)

    spike_bins = [0 for _ in range(n_bins)]
    for spike in spikes:
        timestep = (spike - t0) // dt
        spike_bins[int(timestep)] += 1

    return iter(spike_bins)


def simulate(t0, tmax, dt, spikes):
    # Initialize state
    state = defaultdict(list)
    # Constants
    A, U, tau_d, tau_f, tau_s = 1, 0.45, 0.02, 0.45, 0.08
    # Initial condition
    t, x, u, I = t0, 1, 0, 0
    store(state, t=t, x=x, u=u, I=I)
    # Calculate timesteps at which spikes occur
    spike_bins = bin_spikes(spikes, t0, tmax, dt)

    # Solve simulation timestep
    while t < tmax:
        n_spikes = next(spike_bins)
        # (1) Potentiate the synapse
        u += -u / tau_f + U * (1 - u) * n_spikes
        # (2) Produce current jump
        I += -I / tau_s + A * u * x * n_spikes
        # (3) Expend resources
        x += (1 - x) / tau_d - u * x * n_spikes
        # Advance timestep
        t += dt
        # Store state
        store(state, t=t, x=x, u=u, I=I)

    return state


def plot(state):
    t = state["t"]
    go.Figure([go.Scatter(x=t, y=v, name=k) for k, v in state.items()]).write_html(
        "out.html"
    )


plot(simulate(0, 100, 0.1, [90, 91, 91, 92, 92.1]))
