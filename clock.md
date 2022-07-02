```python
from jupyter_dash import JupyterDash
```

```python
import numpy as np
```

```python
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

points = [str(_) for _ in zip([3,4,5,6,6], [2,3,3,4,4])]
app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("JupyterDash Demo"),
    dcc.Graph(figure=go.Figure(
        data=[go.Scatterpolar(
            r = len(points)*[1],
            theta = points,
            mode = 'markers',
            text=points,
        ),
          go.Scatterpolar(
            r = [1],
            theta = [points[3]],
            mode = 'markers',
            marker = dict(symbol='circle'),
            text=[points[3]],
        ),
             ],
        
        layout=dict(#template=None,
                    polar = dict(
                        hole=.75,
                        radialaxis = dict(range=[0, 1.5], showticklabels=False, ticks='', showgrid=False),
                        angularaxis = dict(showgrid=False, ticks='', visible=True),
                    ),
        )
    )),
])

# Run app and display result inline in the notebook
app.run_server(mode='inline', debug=True, port = '8051', host='0.0.0.0')
```

```python

```
