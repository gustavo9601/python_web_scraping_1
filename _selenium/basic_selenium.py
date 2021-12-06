import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver

"""
Descargar driver de:
https://chromedriver.chromium.org/
"""

class HelloWorld(unittest.TestCase):
    # Prepara el entorno de la prueba
    def setUp(self) -> None:
        # Inicializando el driver
        self.driver = webdriver.Chrome(executable_path= r'C:\xampp\htdocs\python\python_web_scraping_1\driver/chromedriver.exe')
        # Esperara el tiempo en s, hasta ejecutar la siguiente accion
        self.driver.implicitly_wait(10)

    def test_hello_world(self):
        self.driver.get('https://platzi.com')

    def test_visirt_wikipedia(self):
        self.driver.get('https://es.wikipedia.org/')

    # Al terminar la prueba se ejecutara
    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output = 'reportes/', report_name='hello_world_report'))