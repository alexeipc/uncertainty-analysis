# Basic Uncertainty Analysis

## Motivation
I came up with this idea while doing uncertainty analysis for my Physics Lab report. \
This is just a quadrature addition for function *f(a,b,...,z)*:
$$\delta_f = \sqrt{\delta_{fa}+\delta_{fb}+...+\delta_{fz}}$$


## Implementation
### Install
```
pip install PyQt6
```
### Run
```
python ui.py
```

## Features

* Add variable: click on add variable (uncertainties must be seperated with value by "+-")
* Change variable's name: click on the label with the variable's name
* Add function: click on add function (use python arithmetic syntax)
* Change significant figure
