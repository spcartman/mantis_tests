class NavigationHelper:

    def __init__(self, app):
        self.app = app

    def home_page(self):
        wd = self.app.wd
        wd.get(self.app.base_url)

    def manage(self):
        wd = self.app.wd
        wd.find_element_by_css_selector("a.manage-menu-link").click()

    def manage_projects(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[@href='/mantis/manage_proj_page.php']").click()

    def go_to_projects(self):
        self.home_page()
        self.manage()
        self.manage_projects()
