import plotly.graph_objects as go
import numpy as np

from dash.exceptions import PreventUpdate

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




def show_graph(p_i, a, b, clickData):
    p = primes_[p_i]

    fig = go.Figure(
            data=go.Heatmap(z=elliptic(p, a, b),
                showscale=False,
                colorscale='gray'),
            layout=dict(width=700, height=700, title=get_eqn_str(p, a, b)))

    if clickData is not None:
        points = clickData['points']
        x_ = [p['x'] for p in points]
        y_ = [p['y'] for p in points]
        scatter_points = go.Scatter(x=x_, y=y_, mode='markers')
        fig.add_trace(scatter_points)
        
    return fig

def update_point(clickData):
    if clickData is None:
        raise PreventUpdate

    # print(clickData)

    x_ = clickData['points'][0]['x']
    y_ = clickData['points'][0]['y']
    return "({},{})".format(x_, y_)

