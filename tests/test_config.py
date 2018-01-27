# -*- coding: utf-8 -*-
"""Test configs."""
from vimcar.app import create_app
from vimcar.settings import DevConfig, ProdConfig


def test_production_config(api):
    """Production config."""
    app = create_app(ProdConfig, api)
    assert app.config['ENV'] == 'prod'
    assert app.config['DEBUG'] is False
    assert app.config['DEBUG_TB_ENABLED'] is False


def test_dev_config(api):
    """Development config."""
    app = create_app(DevConfig, api)
    assert app.config['ENV'] == 'dev'
    assert app.config['DEBUG'] is True
