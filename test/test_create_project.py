# -*- coding: utf-8 -*-
from model.project import Project


def test_create_project(app, data_project):
    project = data_project
    app.navigation.go_to_projects()
    old_projects = app.soap.get_project_list()
    app.project.create(project)
    old_projects.append(project)
    new_projects = app.soap.get_project_list()
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
