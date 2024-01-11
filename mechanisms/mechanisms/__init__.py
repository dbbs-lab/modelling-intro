"""
Lecture Mechanisms

My collection of NMODL assets.

Glia asset bundle. If the Glia Asset Manager (`nmodl-glia`) is installed, the NMODL assets
in this package will automatically be available in your Glia library for use in the Arbor
and NEURON brain simulation engines.
"""
from pathlib import Path
from glia import Package, Mod

__version__ = "0.1.0"
package = Package(
    "mechanisms",
    Path(__file__).resolve().parent,
    mods=[Mod("mods/bridge__0.mod", "bridge")],
)
