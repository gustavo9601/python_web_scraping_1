import unittest
from selenium import webdriver
from Google_page import Google


class GoogleTest(unittest.TestCase):

    @classmethod  # Decoradores para correr en una sola instancia del navegador
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            executable_path=r'C:\xampp\htdocs\python\python_web_scraping_1\driver/chromedriver.exe')

    def test_search(self):
        google = Google(driver=self.driver, url='https://www.google.com', search_locator='q')
        google.open()
        google.search('Python')

        self.assertEqual('Python', google.keyword)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == '__main__':
    unittest.main()
