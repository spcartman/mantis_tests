from suds.client import Client
from model.project import Project


client = Client("http://localhost/mantis/api/soap/mantisconnect.php?wsdl")


def convert_soap_to_model(soap_proj):
    return Project(id=soap_proj.id, name=soap_proj.name, status=soap_proj.status.name, enabled=soap_proj.enabled,
                   view=soap_proj.view_state.name, description=soap_proj.description)

# p = list(map(convert_soap_to_model, client.service.mc_projects_get_user_accessible("administrator", "admin")))
# print(p)

client.service.mc_project_add("administrator", "admin",
                              {"name": "Another API project 01",
                               "status": {"name": "release"},
                               "inherit_global": False,
                               "view_state": {"name": "private"},
                               "description": "Some random text"})
