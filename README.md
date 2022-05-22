## About

A hands-on tutorial on elliptic curves

### Lesson 0 - defining elliptic curves

Continuous case uses geogebra


```python
import plotly
```

```python
import numpy as np
```

```python
def elliptic(p, a, b):
    x = y = np.arange(p)
    xx, yy = np.meshgrid(x,y)
    return (np.mod(yy**2, p) - np.mod(xx**3+a*xx+b, p) == 0)*1.0
```

## Finite elliptic curves

```python
import plotly.graph_objects as go

fig = go.Figure(data=go.Heatmap(z=elliptic(37, a=0, b=7), colorscale='gray'), layout=dict(width=700, height=700))
fig
```

Note symmetry about $p/2$


## Algebraic sum

Given
$$P=(x_p, y_p)$$
$$Q=(x_q, y_q)$$
What is $P + Q = -R$?

We want the (modulus) line passing through $P, Q$. The slope $m$ of that line is given by

$$m = (y_p-y_q)(x_p-x_q)^{-1} mod(p)  \quad P!=Q$$
$$ (3x_P^2+a) (2y_P)^{-1} mod(p) \quad P = Q, $$
$$a = 7 \quad \text{for bitcoin}$$

With $m$ we can obtain the $R$:
$$ x_R = (m^2 - x_P - x_Q) mod(p) $$
$$ y_r = (y_p + m(x_R-x_P)) mod(p) $$

```python
# taken from https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception(f'modular inverse does not exist {m}')
    else:
        return x % m
```

```python
def add_mod(P, Q, p, a=7):
    x_p, y_p = P
    x_q, y_q = Q
    if (x_p == x_q)&(y_p == y_q):
        m = ((3*x_p**2+a)*modinv(2*y_p, p))%p
    else:
        m = ((y_p - y_q)*modinv(x_p-x_q, p))%p
    x_r = (m**2 - x_p - x_q)%p
    y_r = (y_p + m*(x_r-x_p))%p
    return x_r, y_r
    

add_mod((22, 6), (22, 6), p)
```

```python
def multiply_mod(P, n, p, a=7, b=None):
    P_ = P + ()
    for _ in range(1, n+1):
        P_ = add_mod(P_, P_, p, a)
        if P_ == P:
            break
    return P_

multiply_mod((3, 6), 10, p=97, a=2)
```

How many points are in the subgroup generated by P?

1. count all points on the curve N (see [Schoof's Algorithm](https://en.wikipedia.org/wiki/Schoof%27s_algorithm))
1. find all divisors of N
1. for every divisor of N, see if $nP=0$

```python
def order(field):
    """calculate the order of the field including the point at infinity"""
    return int(field.sum()+1)

order(elliptic(37, a=-1, b=3))
```

```python
def divisors(n):
    for i in range(1, int(n / 2) + 1):
        if n % i == 0:
            yield i
    yield n
```

```python
def subgroup_order(P, p, a, b):
    N = order(elliptic(p, a, b))
    for _ in divisors(N):
#         print(_)
        if multiply_mod(P, _, p=p, a=a) == P:
            break
    if _ == N:
        return N # already contains the point at infinity
    else:
        return _+1

subgroup_order((2,3), p=37, a=-1, b=3)
```

```python
order(elliptic(p=29, a=-1, b=1)) # is prime!
```

```python
subgroup_order((9,24), p=29, a=-1, b=1) # should be 37 instead of 38
```

```python
fig = go.Figure(data=go.Heatmap(z=elliptic(p=29, a=-1, b=1), colorscale='gray'),
                layout=dict(width=700, height=700))
fig
```

# choosing generator point P

Trick is 
1. given N choose the subgroup order n to be a prime divisor of N
1. compute cofactor h = N/n
1. choose random point P -- this could be fun!
1. compute G=hP
1. if G != 0, then n(hP)=0 and G is a generator of the whole curve
1. if G = 0, go back to (3)

```python
def is_prime(n):
    prime_flag = 0
      
    if(n > 1):
        for i in range(2, int(np.sqrt(n)) + 1):
            if (n % i == 0):
                prime_flag = 1
                break
        if (prime_flag == 0):
            return True
    return False
```

```python
def prime_divisor(n):
    """find the largest prime divisor of n"""
    for _ in list(divisors(n))[::-1]:
        if is_prime(_):
            return _

def cofactor(order, n):
    return int(order/n)

prime_divisor(42)
```

```python
order(elliptic(**e1))
```

```python
prime_divisor(37)
```

```python
cofactor(37, 37)
```

```python
e1 = dict(p=29, a=-1, b=1)
N_ = order(elliptic(**e1))
N_
```

```python
H__ = (12, 8)

G__ = multiply_mod(H__, 37, **e1)
G__
```

```python
for _ in range(1, 38):
    print(multiply_mod(G__, _, **e1))
```

## Secret sharing

Since $H=dG$ is uninvertable, we can define a public/private key pairs as ($d_{priv}, H_{pub}$)

Suppose alice has public $H_a$ and private key $d_a$ and similarly for Bob $H_b$ and $d_b$. Alice and Bob may compute a shared secret $S = d_aH_b = d_bH_a = d_ad_bG$. This shared secret can be used by either party to encrypt blobs of data without fear of eavesdropping.

```python
d_a = 5
H_a = multiply_mod(G__, d_a, **e1)

d_b = 9
H_b = multiply_mod(G__, d_b, **e1)

S_b = multiply_mod(H_a, d_b, **e1) # Bob generates secret key using Alice's pub key
S_a = multiply_mod(H_b, d_a, **e1) # Alice generates secret key using Bob's pub key
assert S_a == S_b # check that Alice and Bob get the same result
S_a
```

## ECDSA

1. choose $k \in [1, n]$ for subgroup order $n$
1. calculate $P=kG$

```python
G_ = (9,24)
n_ = subgroup_order(G_, **e1) # should be 37 instead of 38

multiply_mod(G_, d_b, **e1)
```

```python
from random import randrange
```
