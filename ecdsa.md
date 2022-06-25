---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region -->
## ECDSA


1. choose $k \in [1, n]$ for subgroup order $n$
1. calculate $P=kG$
1. r = P_x mod n # get x coordinate of P (unless $r=0$)
1. $s = k^{-1}(z+rd_A) modn$
<!-- #endregion -->

```python
from random import randrange
from elliptic.dashboard import subgroup_order

G_ = (9,24) # generator
n_ = subgroup_order(G_, **e1) # should be 37 for {'p': 29, 'a': -1, 'b': 1}
G_, n_
```

```python

```
