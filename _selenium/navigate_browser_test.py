import unittest
from selenium import webdriver
from time import sleep


class CompareProducts(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            executable_path=r'C:\xampp\htdocs\python\python_web_scraping_1\driver/chromedriver.exe')
        driver = self.driver
        driver.implicitly_wait(30)
        driver.maximize_window()
        driver.get("https://www.google.com/")

    def test_browser_navigation(self):
        driver = self.driver

        search_field = driver.find_element_by_name('q')
        search_field.clear()
        search_field.send_keys('Gustavo Marquez Prieto')
        search_field.submit()

        driver.back()  # retroceder navegador
        sleep(3)  # espera 3 segundos
        driver.forward()  # avanzar
        sleep(3)
        driver.refresh()  # actualizar página
        sleep(3)

    def tearDown(self):
        self.driver.implicitly_wait(3)
        self.driver.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
