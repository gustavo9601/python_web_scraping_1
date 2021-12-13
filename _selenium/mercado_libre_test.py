import unittest
from selenium import webdriver
from time import sleep


class TestingMercadoLibre(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            executable_path=r'C:\xampp\htdocs\python\python_web_scraping_1\driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        driver.get('https://www.mercadolibre.com')

    def test_search_PS4(self):
        driver = self.driver

        country = driver.find_element_by_id("CO")
        country.click()

        search_field = driver.find_element_by_name("as_word")
        search_field.click()
        search_field.clear()
        search_field.send_keys('playstation 4')
        search_field.submit()
        sleep(3)

        location = driver.find_element_by_xpath("//div/div/aside/section[2]/dl[9]/dd[1]/a")
        driver.execute_script("arguments[0].click();", location)
        sleep(3)

        condition = driver.find_element_by_xpath("//div/div/aside/section[3]/dl[6]/dd[1]/a")
        driver.execute_script("arguments[0].click();", condition)
        sleep(3)

        order_menu = driver.find_element_by_class_name("andes-dropdown__trigger")
        order_menu.click()

        higher_price = driver.find_element_by_xpath("//div/div/aside/section[2]/div[2]/div[1]/div/div/div/ul/li[3]/a")
        driver.execute_script("arguments[0].click();", higher_price)
        sleep(3)

        articles = []
        prices = []

        for i in range(5):
            article_name = driver.find_element_by_xpath(
                f'/html/body/main/div/div/section/ol/li[{i + 1}]/div/div/div[2]/div[1]/a').text
            articles.append(article_name)
            article_price = driver.find_element_by_xpath(
                f'/html/body/main/div/div/section/ol/li[{i + 1}]/div/div/div[2]/div[2]/div[1]/div[1]/div/div/span[1]/span[2]').text
            prices.append(article_price)

        print(articles, prices)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
