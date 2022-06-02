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
from psidash.psidash import load_app

app = load_app(__name__, 'elliptic.yaml')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',
                   port=8050,
                   mode='external',
                   extra_files=["elliptic.yaml", "elliptic/dashboard.py"],
                   debug=True)
