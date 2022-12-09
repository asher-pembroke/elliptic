## Schnorr signatures

Here we prototype schnorr signatures in tiny fields. Note: most of the setup is the same as ecdsa.

# Steps for signing with Schnorr

```python
from random import randrange
from elliptic.dashboard import subgroup_order, point_in_curve
```

```python
e1 = dict(p=29, a=-1%29, b=1) # define eliptic curve parameters
```

## Step 1 - Generate private/public key pair

```python
d_A = 7 # private key - do not share!
```

```python
d_A
```

```python
P_A = d_A*G_0 # Alice's pub key
P_A
```

## Step 2 - Choose a generator point

```python
G_0 = point_in_curve(9, 24, **e1)
G_0
```

## Step 3 - get subgroup order of generator point

```python
from elliptic.dashboard import subgroup_order
```

```python
n_G0 = subgroup_order(G_0) # should be 37 for {'p': 29, 'a': -1, 'b': 1}
n_G0
```

check that n_G0 is truly the subgroup order of G_0

```python
n_G0 * G_0 # should return point at infinity
```

## Step 4 - Choose (random, unused) value `k`

```python
k = 5
k
```

## Step 5 - compute curve point R

```python
R = k*G_0
R
```

## Step 6 - pick a message to sign

```python
message = 'I love btc++'
```

## Step 7 - hash message with R, P_A (where it starts to differ)

Combine `R`, `p`, and the `message` first

```python
comb = str(R.x.num) + str(R.y.num) + str(P_A.x.num) + str(P_A.x.num) + message
comb
```

hash the result

```python
H = get_z(comb)
H
```

```python
from elliptic.dashboard import get_z
```

s=k+H(R‖P‖m)p mod n_G0

```python
s = (k + (H%n_G0)*(d_A%n_G0))%n_G0
s
```

```python
signature = (R.x.num, R.y.num), s
signature
```

# Steps for verifying Schnorr

Check the following:

sG = R+H(R‖P‖m)P

```python
s*G_0
```

```python
R + H*P_A
```

```python
assert s*G_0 == R + H*P_A # nice!
```
