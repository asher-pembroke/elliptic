###  Problem sets


This notebook may be used to generate answers to problem sets that can be stored in the git repo.

However, we don't want to store the actual answers in the git repo. Instead, we store something like a hash of the answer and compare against that on the fly.


### Problem definitions


The base of the repo stores `problems.yaml` which will containing both the problems and their.

```python
cat problems.yaml
```

The keys are named after currently active tab in the dashboard, the idea being that all the problems for a given lesson will be presented on the corresponding tab.

Under each key is a list of problems, which will be rendered in order. Each problem is composed of:

* question: (str) defining the problem for the student to answer.
* answer_z30: result of `get_z30` applied to answer
* type: what type of answer should be provided - determines how the input/output will be rendered


The function `get_z` will assign a (mostly) unique integer to any input message string.


### Processing answers


Load the questions from the base of the repo. We'll use these to programmatically set up the questions in the layout.

```python
from omegaconf import OmegaConf # may be overkill, but has some merits

problems = OmegaConf.to_container(OmegaConf.load('problems.yaml')) # cast into dictionary
```

Let's get the problem question from the `point-multiplication` section.

```python
problem = problems['point-multiplication'][0] # get first answer
```

```python
question = problem['question']
question # latex will be rendered if you copy and paste this into a markdown cell
```

1. For the elliptic curve defined by `a=0, b=7,` embedded in the finite field `p=37` and assuming the generator point `(4,21)`, for what value of `n` does
$$ n \cdot (4,21) = (17,6) ?$$ 

```python
answer_z30 = problem['answer_z30'] 
answer_z30 # always an integer
```

The above "answer" comes from hash of the real answer (which happens to be 5). Here's how we generate these `z` values. 

```python
from elliptic.dashboard import get_z
```

```python
help(get_z)
```

Check that the answer matches what we expect

```python
assert answer == get_z('5')
```

```python
get_z('5', 30) == answer_0
```
