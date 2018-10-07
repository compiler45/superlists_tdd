from selenium import webdriver

from functional_tests.base import FunctionalTest


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # Lain is a logged-in user
        self.create_pre_authenticated_session('lain@example.com')
        lain_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(lain_browser))

        # Her friend Edith if also hanging out on the lists site
        edith_browser = webdriver.Chrome()
        self.addCleanup(lambda: quit_if_possible(edith_browser))
        self.browser = edith_browser
        self.create_pre_authenticated_session('edith@example.com')

        # Edith goes to the home page and starts a list
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Get help')

        # She notices a 'Share this list' option
        share_box = self.browser.find_element_by_css_selector(
            'input[name="share"]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

