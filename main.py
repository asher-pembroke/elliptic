# ---
# jupyter:
#   jupytext:
#     formats: py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
from omegaconf import OmegaConf
from psidash.psidash import load_app, load_conf, load_dash, load_components, get_callbacks, assign_callbacks

conf = load_conf('elliptic.yaml')
app = load_dash(__name__, conf['app'], conf.get('import'))
app.layout = load_components(conf['layout'], conf.get('import'))

if 'callbacks' in conf:
    callbacks = get_callbacks(app, conf['callbacks'])
    assign_callbacks(callbacks, conf['callbacks'])


if __name__ == '__main__':
    app.run_server(**conf['run_server'])