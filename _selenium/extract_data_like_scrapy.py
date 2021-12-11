import unittest
from selenium import webdriver


class Typos(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            executable_path=r'C:\xampp\htdocs\python\python_web_scraping_1\driver/chromedriver.exe')
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/')
        driver.find_element_by_link_text('Sortable Data Tables').click()

    def test_sort_tables(self):
        driver = self.driver

        table_data = [[] for i in range(5)]
        print(table_data)

        for i in range(5):
            header = driver.find_element_by_xpath(f'//*[@id="table1"]/thead/tr/th[{i + 1}]/span')
            table_data[i].append(header.text)

            for j in range(4):
                row_data = driver.find_element_by_xpath(f'//*[@id="table1"]/tbody/tr[{j + 1}]/td[{i + 1}]')
                table_data[i].append(row_data.text)

        print(table_data)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
