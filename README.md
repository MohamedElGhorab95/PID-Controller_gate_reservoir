# PID-Controller_gate_reservoir
This code is for solving a reservoir operation problem with the following description.
Consider a reservoir with an area of 10.0 km2 that is fed by a river, with a given input discharge Qinp that changes in time. The reservoir serves various users with different requirements, who agreed (after a long consultation process) on having a water level setpoint of 3.5m. They are willing to allow for some fluctuation, as long as the water level is within the drought (3.2m) and flood (4.5m) levels.
---------------------------------------------------------------------------------------------------------------------------------
The water level in the reservoir can be controlled by a sluice gate that gives an output discharge Qout in m3/s given by the gate equation where y1 is the water level in the reservoir (m); y2 is the gate opening with respect to the gate bed (m); W is the width of the gate (W = 3m), g=9.81 m/s2, and Cd is the discharge coefficient, given by: Cd = (Cc / sqrt(1 + Cc*y2/y1)) with Cc = 0.61
---------------------------------------------------------------------------------------------------------------------------------
The gate can be opened from 2.0m to 4.0m. Assume the gate is never submerged, so the Qout equation is always valid.
---------------------------------------------------------------------------------------------------------------------------------
An assumption is made regarding the initial conditions at t=0 , y2 = y1 = 3.0m
---------------------------------------------------------------------------------------------------------------------------------
An assumption is made regarding the downstream channel in case the water level in the reservoir is less than the gate opening; manning's equation is to be used for the discharge estimation with parameters (n = 0.015 s/m1/3, S = 0.001 m/m)
---------------------------------------------------------------------------------------------------------------------------------
