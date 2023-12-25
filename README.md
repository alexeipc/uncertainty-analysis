# Basic Uncertainty Analysis

## Motivation
I came up with this idea while doing uncertainty analysis for my Physics Lab report. \
This is just a quadrature addition for function *f(a,b,...,z)*:
$$\delta_f = \sqrt{\delta_{fa}^2+\delta_{fb}^2+...+\delta_{fz}^2}$$


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
![GUI](https://github.com/alexeipc/uncertainty-analysis/blob/main/gui.png)

* Add variable: click on add variable (uncertainties must be seperated with value by "+-")
* Change variable's name: click on the label with the variable's name
* Add function: click on add function (use python arithmetic syntax)
* Change significant figure
