from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
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

    def delete(self, project):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[@href='manage_proj_edit_page.php?project_id=%s']" % project.id).click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        self.ensure_projects_page_opened()
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
                self.project_cache.append(Project(id=str(id), name=name, status=status, enabled=enabled, view=view,
                                                  description=description))
        return list(self.project_cache)

    def define_enabled(self, table_presentation):
        if table_presentation == 'X':
            return True
        return False

    def ensure_existence_sanity_check(self):
        if len(self.app.soap.get_project_list()) == 0:
            self.app.soap.create(Project(name="Sanity project by API"))

    def ensure_projects_page_opened(self):
        try:
            WebDriverWait(self.app.wd, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".row-category")))
        except TimeoutException:
            raise TimeoutException("\nProjects page was not loaded in due time.\n")
