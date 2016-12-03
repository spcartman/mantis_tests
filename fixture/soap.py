from suds.client import Client
from suds import WebFault
from model.project import Project


class SOAPHelper:

    def __init__(self, app):
        self.app = app
        self.client = Client(self.app.base_url + "api/soap/mantisconnect.php?wsdl")

    def can_login(self, user, passwd):
        try:
            self.client.service.mc_login(user, passwd)
            return True
        except WebFault:
            return False

    def create(self, project):
        try:
            self.client.service.mc_project_add(self.app.user, self.app.password,
                                               {"name": project.name,
                                                "status": {"name": project.status},
                                                "inherit_global": project.inherit,
                                                "view_state": {"name": project.view},
                                                "description": project.description})
        except WebFault:
            raise WebFault("\nThe system can not create the project.\n")

    def get_project_list(self):
        try:
            return list(map
                        (self.convert_soap_to_model,
                         self.client.service.mc_projects_get_user_accessible(self.app.user, self.app.password)))
        except WebFault:
            raise WebFault("\nThe system can not get contacts for specified user.\n")

    def convert_soap_to_model(self, soap_proj):
        return Project(id=str(soap_proj.id), name=soap_proj.name, status=soap_proj.status.name, enabled=soap_proj.enabled,
                       view=soap_proj.view_state.name, description=soap_proj.description)
