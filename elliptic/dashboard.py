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
    return (((yy**2)%p - ((xx**3)%p+(a*xx)%p+b)%p) == 0)*1.0

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
        return "F_{" + str(p) + "}: y^2 = x^3" + sign_str(b)
    else:
        return "F_{" + str(p) + "}: y^2 = x^3" + sign_str(a, False) + "x " + sign_str(b)


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


def get_pnt_annotation(x, y, text):
    return dict(x = x, y=y, text=text,
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8)

def point_str(x, y):
    return "({},{})".format(x,y)

def multiply_graph(p_i, a, b, n, points):
    """multiply points by n"""
    p = primes_[p_i]
    curve = elliptic(p, a, b)

    fig = go.Figure(
            data=go.Heatmap(z=curve,
                showscale=False,
                colorscale='gray',
                hoverinfo = 'text',
                text = array_to_str(curve),
                ),
            )

    title_str = get_eqn_str(p, a, b)

    if points is not None:
        curve_key = str((p,a,b))
        if curve_key in points:
            pts = points[curve_key]
            if len(pts) > 0:
                x_0, y_0 = pts[0]
                base_point = go.Scatter(x=[x_0], y=[y_0],
                    text=[],
                    marker_symbol='square',
                    marker=dict(size=get_p_size(p_i)),
                    hoverinfo='skip',
                    mode='markers',
                    showlegend=False,)
                fig.add_trace(base_point)

                title_str += '\qquad {} \cdot {}'.format(str(n), str((x_0, y_0)))
                if n == 0:
                    title_str += ' = \infty'

            if len(pts) == 2: # get second point
                x_n, y_n = pts[1]
                n_point = go.Scatter(x=[x_n], y=[y_n],
                    text=[],
                    marker_symbol='square',
                    marker=dict(size=get_p_size(p_i)),
                    hoverinfo='skip',
                    mode='markers',
                    showlegend=False)
                fig.add_trace(n_point)

                if n == 0:
                    pass
                elif x_n == -1:
                    title_str += ' = \infty'
                else:
                    title_str += ' = {}'.format(str((x_n, y_n)))

            if len(pts) > 0:
                order_ = order(p, a, b)
                subgroup_order_ = subgroup_order(point_in_curve(x_0, y_0, p, a, b))
                title_str += f"\\newline \quad N:{order_}"
                title_str += "\quad N_{" + point_str(x_0, y_0) + "}" + f":{subgroup_order_}"

            for p_ in pts:
                x_, y_ = p_
                fig.add_annotation(**get_pnt_annotation(x_, y_, str((x_, y_))))

    fig.update_layout(dict(width=700, height=700,
                xaxis=dict(range=[0,p-1]),
                yaxis=dict(range=[0,p-1]),
                title="$ {} $".format(title_str)))
    return fig

def add_graph(p_i, a, b, points):
    """add points on click"""
    p = primes_[p_i]

    curve = elliptic(p, a, b)

    fig = go.Figure(
            data=go.Heatmap(z=curve,
                showscale=False,
                colorscale='gray',
                hoverinfo = 'text',
                text = array_to_str(curve),
                ),
            )

    title_str = get_eqn_str(p, a, b)

    if points is not None:
        curve_key = str((p,a,b))
        if curve_key in points:
            pts = points[curve_key]
            x_ = [p_[0] for p_ in pts]
            y_ = [p_[1] for p_ in pts]
            scatter_points = go.Scatter(x=x_, y=y_,
                text=[],
                marker_symbol='square',
                marker=dict(size=get_p_size(p_i)),
                hoverinfo='skip',
                mode='markers',
                showlegend=False,)
            fig.add_trace(scatter_points)
            for p_ in pts:
                x_, y_ = p_
                fig.add_annotation(**get_pnt_annotation(x_, y_, str((x_, y_))))

            title_str +=  "\qquad" + '+'.join([str(tuple(p_)) for p_ in pts])

            if len(pts) == 2:
                P = point_in_curve(pts[0][0], pts[0][1], p, a, b)
                Q = point_in_curve(pts[1][0], pts[1][1], p, a, b)
                R = P+Q
                if R.x is not None:
                    R_str = str((R.x.num, R.y.num))
                    title_str += ' = {}'.format(R_str)
                    R_trace = go.Scatter(x = [R.x.num], y = [R.y.num],
                        text = [R_str],
                        marker_symbol = 'square',
                        marker=dict(size=get_p_size(p_i)),
                        hoverinfo='text',
                        mode='markers',
                        showlegend=False,
                        )
                    fig.add_trace(R_trace)
                else:
                    title_str += ' = \infty'
        else:
            # print(curve_key, 'not in point store')
            pass

    
    fig.update_layout(dict(width=700, height=700,
                xaxis=dict(range=[0,p-1]),
                yaxis=dict(range=[0,p-1]),
                title="$ {} $".format(title_str)))
    return fig

def update_multiply_points(p_i, a, b, n, clickData, store):
    p = primes_[p_i]
    curve_key = str((p, a, b))

    if store is not None:
        if curve_key in store:
            points = [tuple(v) for v in store[curve_key]]
        else:
            points = []
    else:
        points = []
        store = {curve_key: points}

    if clickData is not None:
        # replace the first point
        p_0 = clickData['points'][0]
        x_0, y_0 = p_0['x'], p_0['y']
        try:
            G_0 = point_in_curve(x_0, y_0, p, a, b)
            points = [(x_0, y_0)]
        except ValueError:
            raise PreventUpdate
        p_n = n*G_0
        if p_n.x is not None:
            points.append((p_n.x.num, p_n.y.num))
        else:
            points.append((-1, -1))
        
    store[curve_key] = points
    return store

def update_add_points(p_i, a, b, clickData, store):
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
            else:
                # add point to itself
                point_in_curve(p_[0], p_[1], p, a, b)
                points.append(p_)
                
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


order_dict = {} # cache results

def order(p, a, b):
    """calculate the order of the field including the point at infinity"""
    if (p,a,b) not in order_dict:
        order_ = int(elliptic(p, a, b).sum()+1) # brute force
        order_dict[(p,a,b)] = order_
    else:
        order_ = order_dict[(p,a,b)]
    return order_

def divisors(n):
    for i in range(1, int(n / 2) + 1):
        if n % i == 0:
            yield i
    yield n

def subgroup_order(P):
    p = P.x.prime
    a = P.a.num
    b = P.b.num

    N = order(p, a, b)
    
    for _ in divisors(N):
        P_ = _*P
        if P_.x is None:
            break
    return _

