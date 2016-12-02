# -*- coding: utf-8 -*-


def test_login(app):
    app.session.ensure_logout()
    app.session.login("administrator", "admin")
    assert app.session.is_logged_in_as("administrator")
