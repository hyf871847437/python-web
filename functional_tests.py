from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest,time

class NewVisitorTest(unittest.TestCase):
    #setup 和tearDowm是特殊的方法，分别在测试的前后运行，这两个方法与try/except相似
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)                          #隐式等待 3秒

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_item(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):         #名字以test开头的函数都是测试方法
        self.browser.get('http://localhost:8000')
        #网页头部和标题是否含有To-Do这个词
        self.assertIn('To-Do',self.browser.title)
        header_text = self.browser.find_element_by_id('id_new_item').text
        #self.assertIn('To-Do', header_text)    #不知道为什么，错误
        #待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')   #获取属性placeholder的值
        #发送第一个
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_item('1: Buy peacock feathers')
        #第二个
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_item('1: Buy peacock feathers')
        self.check_for_row_in_item('2: Use peacock feathers to make a fly')
        #回车后,页面是否更新
        # self.assertTrue(
        #     any(row.text == '1: Buy peacock feathers' for row in rows),'New to-do item didnot appear in table\
        #  it was %s'%table.text)

        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')                               #warnings='ignore'为禁止抛出resourceWarning异常

