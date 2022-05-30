import plotly.graph_objects as go
import numpy as np

from dash.exceptions import PreventUpdate

import sys

sys.path.append('../programmingbitcoin/code-ch03/')

from ecc import Point, FieldElement

def prime(i, primes):
    for prime in primes:
        if not (i == prime or i % prime):
            return False
    primes.add(i)
    return i

def get_primes(n):
    primes = set([2])
    i, p = 2, 0
    while True:
        if prime(i, primes):
            p += 1
            if p == n:
                return primes
        i += 1

primes_ = list(get_primes(100))

def update_p_slider_label(p_i):
    return str(primes_[p_i])

def elliptic(p, a, b):
    x = y = np.arange(p)
    xx, yy = np.meshgrid(x,y)
    return (np.mod(yy**2, p) - np.mod(xx**3+a*xx+b, p) == 0)*1.0

def sign_str(a, unity=True):
    if a > 0:
        if unity:
            return f'+ {a}'
        else:
            if a == 1:
                return f'+ ' # + x
            else:
                return f'+ {a}'
    elif a < 0:
        if unity:
            return f'- {abs(a)}'
        else:
            if a == -1:
                return f'- '
            else:
                return f'- {abs(a)}'
    else:
        return ''

def get_eqn_str(p, a, b):
    """F_p: y^2 = x^3 + ax + b"""
    if a == 0:
        return "$ F_{" + str(p) + "}: y^2 = x^3" + sign_str(b) + "$"
    else:
        return "$ F_{" + str(p) + "}: y^2 = x^3" + sign_str(a, False) + "x " + sign_str(b) + "$"


def array_to_str(arr):
    result = []
    for i, row in enumerate(arr):
        for j, col in enumerate(row):
            if col > 0:
                result.append('({},{})'.format(j,i))
            else:
                result.append('')
    return np.array(result).reshape(arr.shape)

def get_p_size(p_i, size_min = 1, size_max = 30):
    """scale to 15 when p_i = 14"""
    return int(np.interp(p_i, [3, 14, 100], [size_max, 15, size_min]))

def show_graph(p_i, a, b, points):
    p = primes_[p_i]

    curve = elliptic(p, a, b)
    fig = go.Figure(
            data=go.Heatmap(z=curve,
                showscale=False,
                colorscale='gray',
                hoverinfo = 'text',
                text = array_to_str(curve),
                ),
            layout=dict(width=700, height=700, title=get_eqn_str(p, a, b)))

    if points is not None:
        curve_key = str((p,a,b))
        if curve_key in points:
            x_ = [p_[0] for p_ in points[curve_key]]
            y_ = [p_[1] for p_ in points[curve_key]]
            scatter_points = go.Scatter(x=x_, y=y_,
                text=[],
                marker_symbol='square',
                marker=dict(size=get_p_size(p_i)),
                hoverinfo='text',
                mode='markers')
            fig.add_trace(scatter_points)
        else:
            print(curve_key, 'not in point store')

    return fig

def update_points(p_i, a, b, clickData, store):
    p = primes_[p_i]


    curve_key = str((p,a,b))

    if store is not None:
        if curve_key in store:
            points = [tuple(v) for v in store[curve_key]]
        else:
            points = []
    else:
        points = []
        store = {curve_key: points}
    
    if clickData is not None:
        new_points = [(p_['x'], p_['y']) for p_ in clickData['points']]
        for p_ in new_points:
            if p_ not in points:
                try:
                    point_in_curve(p_[0], p_[1], p, a, b)
                    points.append(p_)
                except ValueError:
                    raise PreventUpdate
                
    store[curve_key] = points[-2:] # keep the last two points

    return store

def render_points(p_i, a, b, points):
    p = primes_[p_i]
    if points is not None:
        curve_key = str((p,a,b))
        if curve_key in points:
            points_str = ""
            for  i, p_ in enumerate(points[curve_key]):
                points_str += "$ P_{" + str(i) + "}: " f"{p_[0],p_[1]} $ \n"

            return points_str

def point_in_curve(x, y, p, a, b):
    return Point(FieldElement(x, p),
                FieldElement(y, p),
                FieldElement(a, p),
                FieldElement(b, p),)



