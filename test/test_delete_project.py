# -*- coding: utf-8 -*-
from random import choice


def test_delete_project(app):
    app.project.ensure_existence_sanity_check()
    app.navigation.go_to_projects()
    old_projects = app.soap.get_project_list()
    project_to_delete = choice(old_projects)
    app.project.delete(project_to_delete)
    old_projects.remove(project_to_delete)
    new_projects = app.soap.get_project_list()
    assert old_projects == new_projects
