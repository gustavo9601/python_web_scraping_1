import unittest

from pyunitreport import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.support.ui import Select  # Modulo para poder seleccionar del dropdown


class LanguageOptions(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            executable_path=r'C:\xampp\htdocs\python\python_web_scraping_1\driver/chromedriver.exe')
        driver = self.driver
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get('http://demo-store.seleniumacademy.com/')

    def test_select_language(self):
        exp_options = ['English', 'French', 'German']
        act_options = []

        # Clase para interactuar con los input type Select
        select_language = Select(self.driver.find_element_by_id('select-language'))

        self.assertEqual(3, len(select_language.options))

        for option in select_language.options:
            act_options.append(option.text)

        # Verifico que las lsiatas sean iguales
        self.assertListEqual(act_options, exp_options)
        # Verifico que idionma esta seleciionado
        self.assertEqual('English', select_language.first_selected_option.text)
        # Seleccionar el idioma German
        select_language.select_by_visible_text('German')
        # verifico que en la url diga store=german
        self.assertTrue('store=german' in self.driver.current_url)
        # selecciono por indice me devuelvo a Ingles
        select_language = Select(self.driver.find_element_by_id('select-language'))
        select_language.select_by_index(0)

    def tearDown(self):
        self.driver.implicitly_wait(5)
        self.driver.close()


if __name__ == '__main__':
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes/', report_name='select_and_list_report'))

