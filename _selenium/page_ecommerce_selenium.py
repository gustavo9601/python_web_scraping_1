import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver
# By nos permite el uso de 2 métodos privados find_elements(selector, 'value') y find_element(By.ID, "search")
from selenium.webdriver.common.by import By

"""
Descargar driver de:
https://chromedriver.chromium.org/
"""


class HomePageTests(unittest.TestCase):
    # Prepara el entorno de la prueba
    def setUp(self) -> None:
        # Inicializando el driver
        self.driver = webdriver.Chrome(
            executable_path=r'C:\xampp\htdocs\python\python_web_scraping_1\driver/chromedriver.exe')
        # De esta forma para que use una sola instancia del navegador y no abra una por cada prueba
        driver = self.driver
        driver.get('http://demo-store.seleniumacademy.com/')
        driver.maximize_window()
        # Esperara el tiempo en s, hasta ejecutar la siguiente accion
        driver.implicitly_wait(5)

    def test_search_text_field(self):
        # search_field = self.driver.find_element_by_id('search')
        search_field = self.driver.find_element(By.ID, "search")

    def test_search_by_name(self):
        search_field = self.driver.find_element(By.NAME, "q")

    def test_search_by_class(self):
        search_field = self.driver.find_element(By.CLASS_NAME, "input-text")

    def test_search_button(self):
        search_button = self.driver.find_element(By.CLASS_NAME, "search-button")

    def test_search_banner_img(self):
        banner_list = self.driver.find_element(By.CLASS_NAME, "promos")
        banner = banner_list.find_elements(By.TAG_NAME, "img")
        self.assertEqual(3, len(banner))

    def test_icon_cart(self):
        icon_cart = self.driver.find_element(By.CSS_SELECTOR, "div.header-minicart span.icon")

    def test_vip_promo(self):
        # Usando los selectores de XPATH
        vip_promo = self.driver.find_element(By.XPATH,
                                             "//*[@id='top']/body/div/div[2]/div[2]/div/div/div[2]/div/ul/li[4]/a/img")

    # Al terminar la prueba se ejecutara
    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes/', report_name='home_page_reports'))
