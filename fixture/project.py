from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def fill_form(self, project):
        self.app.update_textbox("project-name", project.name)
        self.app.update_dropdown("project-status", project.status)
        self.app.update_checkbox("project-inherit-global", project.inherit)
        self.app.update_dropdown("project-view-state", project.view)
        self.app.update_textbox("project-description", project.description)

    def create(self, project):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_form(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.app.ensure_confirm_page("Operation successful.")
        self.project_cache = None

    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.project_cache = []
            for element in wd.find_elements_by_xpath("(//tbody)[1]/tr"):
                id = element.find_element_by_css_selector("td:nth-child(1) > a").get_attribute("href").split("id=")[1]
                name = element.find_element_by_css_selector("td:nth-child(1) > a").text
                status = element.find_element_by_css_selector("td:nth-child(2)").text
                enabled = self.define_enabled(element.find_element_by_css_selector("td:nth-child(3)").text)
                view = element.find_element_by_css_selector("td:nth-child(4)").text
                description = element.find_element_by_css_selector("td:nth-child(5)").text
                self.project_cache.append(Project(id=id, name=name, status=status, enabled=enabled, view=view,
                                                  description=description))
        return list(self.project_cache)

    def define_enabled(self, table_presentation):
        if table_presentation == 'X':
            return True
        return False
