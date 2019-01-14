
# Development

## Introduction

Respository description. Module functions.

## Model

- ```/tb/models/cordic_model.py```
- Test model: ```python ./tb/models/cordic_model_tb.py```

## Tests
```
cd ./tb; python cordic_sincos_engine_run.py
```

### Testbenchs dependencies

- VUnit
```
sudo pip install vunit_hdl
```
- numpy
```
sudo pip install numpy
```
- pandas
```
sudo pip install pandas
```
- lcov: code coverage.
```
sudo apt-get install lcov
```
- gtkwave: visualization.


### Documentation dependencies
- doxygen: Documentation generation

### Documentation generation

```
cd ./doc; doxygen Doxyfile
```
The generated documentation is in /doc/gen/html

To generate documentation in .pdf

```
cd doc/gen/latex
make pdf
```

Generated in doc/latex
