NEURON {
    SUFFIX glia__mechanisms__bridge__0
    NONSPECIFIC_CURRENT i
    RANGE i, ii
}

ASSIGNED {
  i  (milliamp/cm2)
  v  (millivolt)
}

PARAMETER {
    ii = 0
}

BREAKPOINT {
    i = ii
}
