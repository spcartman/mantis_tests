# -*- coding: utf-8 -*-
from model.project import Project


def test_create_project(app, data_project):
    project = data_project
    app.navigation.go_to_projects()
    old_projects = app.project.get_project_list()
    app.project.create(project)
    old_projects.append(project)
    app.navigation.go_to_projects()
    new_projects = app.project.get_project_list()
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
