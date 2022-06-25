###  Problem sets


This notebook may be used to generate answers to problem sets that can be stored in the git repo.

However, we don't want to store the actual answers in the git repo. Instead, we store something like a hash of the answer and compare against that on the fly.


The base of the repo stores `problems.yaml` which will containing both the problems and their.

```python
cat problems.yaml
```

As we can see, the keys are named after currently active tab in the dashboard, the idea being that all the problems for a given lesson will be presented on the corresponding tab.

Under each key is a list of problems, which will be rendered in order. Each problem is composed of:

* question: (str) defining the problem for the student to answer.
* answer_z30: result of `get_z30` applied to answer
* type: what type of answer should be provided - determines how the input/output will be rendered


The function `get_z` will assign a (mostly) unique integer to any input message string.


Load the questions

```python
from omegaconf import OmegaConf

problems = OmegaConf.to_container(OmegaConf.load('problems.yaml'))

answer_0 = problems['point-multiplication'][0]['answer_z30'] # get first answer
```

```python
from elliptic.dashboard import get_z
```

```python
help(get_z)
```

```python
get_z('5')
```

```python
get_z('5', 30) == answer_0
```
