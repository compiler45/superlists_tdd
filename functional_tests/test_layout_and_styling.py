from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

MAX_WAIT = 10


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Lain goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input is nicely centered
        input_box = self.get_item_input_box()
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2,
                               512, delta=10)
