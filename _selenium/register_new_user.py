import unittest

from pyunitreport import HTMLTestRunner
from selenium.webdriver.common.by import By
from selenium import webdriver


class RegisterNewUser(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            executable_path=r'C:\xampp\htdocs\python\python_web_scraping_1\driver/chromedriver.exe')
        driver = self.driver
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get("http://demo.onestepcheckout.com/")

    def test_new_user(self):
        driver = self.driver
        # le decimos al driver que encuentre la opción de cuenta por su Xpath y le haga click para desplegar el menu
        driver.find_element(By.XPATH, '/html/body/div/div[2]/header/div/div[2]/div/a/span[2]').click()
        # el driver va a buscar el enlace por su texto y haga click
        driver.find_element(By.LINK_TEXT, 'Log In').click()
        # creo una variable asociada al botón de crear cuenta
        create_account_button = driver.find_element(By.XPATH,
                                                    '/html/body/div/div[2]/div[2]/div/div/div[2]/form/div/div[1]/div[2]/a/span/span')

        # validamos que el botón esté visible y habilitado
        self.assertTrue(create_account_button.is_displayed() and create_account_button.is_enabled())
        create_account_button.click()

        # comprueba que estamos en el sitio de crear cuenta
        self.assertEqual('Create New Customer Account', driver.title)

        # creación de variables con el nombre del selector correspondiente
        first_name = driver.find_element(By.ID, 'firstname')
        last_name = driver.find_element(By.ID, 'lastname')
        email_address = driver.find_element(By.ID, 'email_address')
        password = driver.find_element(By.ID, 'password')
        confirm_password = driver.find_element(By.ID, 'confirmation')
        news_letter_subscription = driver.find_element(By.ID, 'is_subscribed')
        submit_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div/div[2]/form/div[2]/button')

        # verificamos si los elementos están habilitados
        self.assertTrue(first_name.is_enabled()
                        and last_name.is_enabled()
                        and email_address.is_enabled()
                        and password.is_enabled()
                        and confirm_password.is_enabled()
                        and news_letter_subscription.is_enabled()
                        and submit_button.is_enabled())

        # mandamos los datos al formulario
        first_name.send_keys('Test')
        last_name.send_keys('Test')
        email_address.send_keys('arqcftlothxuknlsxkt@awdrt.com')  # sacado de 10-minute mail
        password.send_keys('Test')
        confirm_password.send_keys('Test')
        submit_button.click()


    def test_create_new_user_directly_path(self):
        url = 'http://demo.onestepcheckout.com/customer/account/create/'
        driver = self.driver
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get(url)

        # creación de variables con el nombre del selector correspondiente
        first_name = driver.find_element(By.ID, 'firstname')
        last_name = driver.find_element(By.ID, 'lastname')
        email_address = driver.find_element(By.ID, 'email_address')
        password = driver.find_element(By.ID, 'password')
        confirm_password = driver.find_element(By.ID, 'confirmation')
        news_letter_subscription = driver.find_element(By.ID, 'is_subscribed')
        submit_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div/div[2]/form/div[2]/button')

        # verificamos si los elementos están habilitados
        self.assertTrue(first_name.is_enabled()
                        and last_name.is_enabled()
                        and email_address.is_enabled()
                        and password.is_enabled()
                        and confirm_password.is_enabled()
                        and news_letter_subscription.is_enabled()
                        and submit_button.is_enabled())

        # mandamos los datos al formulario
        first_name.send_keys('Gus')
        last_name.send_keys('Mar')
        email_address.send_keys('gusmar@awdrt.com')  # sacado de 10-minute mail
        password.send_keys('gus123456')
        confirm_password.send_keys('gus123456')
        submit_button.click()

    def tearDown(self):
        self.driver.implicitly_wait(3)
        self.driver.close()


if __name__ == "__main__":
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes/', report_name='register_new_reports'))
