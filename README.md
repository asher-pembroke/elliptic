## About

A hands-on tutorial on elliptic curves

### Lesson 0 - defining elliptic curves

The continuous case uses geogebra. Visit the interactive companion page here:

https://www.geogebra.org/m/baurc6bu

<!-- #region -->
## Setup


### Docker (the easy way)

If you just want to run the dashboard, you'll need to have docker installed on your machine.
https://www.docker.com/products/docker-desktop

Once you have docker, then you can run the following command from the base of this repo:

```
docker compose up
```

This will start two services:

* elliptic curve dashboard server http://localhost:8050
* jupyter notebook server server http://localhost:8888

!!! note: The notebook server uses an access token which will be printed out to the console when the container starts up.
<!-- #endregion -->

<!-- #region -->
## Host install (the slightly harder way)

If you want to run the dashboard on your host machine, you'll need the following requirements

* plotly
* plotly
* dash
* numpy
* dash-bootstrap-components
* dash_daq
* cryptography

You can get any of the above dependencies like this:

```sh
pip3 install <dependency>
```

Also, these are nice to have but not required

* jupyter (if you want to run notebooks)
* jupytext (if you want markdown notebooks)
* jupyter-dash (if you want to prototype a dashboard in a notebook)

You'll also need the `psidash` library I made for rapid prototying of dashboards in yaml

```sh
pip install --user git+https://github.com/predsci/psidash.git
```

Finally, you'll need Jimmy Song's programming bitcoin in a sibling path of this repo

```sh
git clone https://github.com/jimmysong/programmingbitcoin.git /home/programmingbitcoin
```
<!-- #endregion -->


