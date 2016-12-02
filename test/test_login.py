# -*- coding: utf-8 -*-


def test_login(app):
    app.session.login("administrator", "admin")
    assert app.session.is_logged_in_as("administrator")
