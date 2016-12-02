# -*- coding: utf-8 -*-
from random import choice


def test_delete_project(app):
    app.project.ensure_existence_sanity_check()
    old_projects = app.project.get_project_list()
    project_to_delete = choice(old_projects)
    app.project.delete(project_to_delete)
    old_projects.remove(project_to_delete)
    new_projects = app.project.get_project_list()
    assert old_projects == new_projects
