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

```python
%load_ext autoreload

%autoreload 2
```

<!-- #region -->
## ECDSA


1. choose $k \in [1, n]$ for subgroup order $n$
1. calculate $P=kG$
1. r = P_x mod n # get x coordinate of P (unless $r=0$)
1. $s = k^{-1}(z+rd_A) modn$
<!-- #endregion -->

```python
from random import randrange
from elliptic.dashboard import subgroup_order, point_in_curve
```

```python
help(point_in_curve)
```

```python
e1 = dict(p=29, a=-1%29, b=1) # define eliptic curve parameters
```

### Choose generator point

```python
G_0 = point_in_curve(9, 24, **e1)
G_0
```

### Find subgroup order $ n_{G_0}$

```python
from elliptic.dashboard import subgroup_order
```

```python
help(subgroup_order)
```

```python
n_G0 = subgroup_order(G_0) # should be 37 for {'p': 29, 'a': -1, 'b': 1}
n_G0
```

```python
n_G0 * G_0 # check that n_G0 is truly the subgroup order of G_0
```

### Choose k

```python
k = 3
k
```

### Compute $P=k G_0$

```python
P = k*G_0
P
```

### Find r

```python
r = P.x.num%n_G0
r

assert r != 0 # if r = 0, start over with a new k
```

### create message to sign

```python
message = 'verify me!'
```

### get z for message

```python
from elliptic.dashboard import get_z
```

```python
z = get_z(message)
```

### compute signature $s = k^{-1}(z+rd_A) mod(n_{G_0})$

```python
from elliptic.dashboard import modinv

help(modinv)
```

```python
s = modinv(k, n_G0)*(z + r*)
```

```python

```
