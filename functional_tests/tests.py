from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest,time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NewVisitorTest(StaticLiveServerTestCase):
    #setup 和tearDowm是特殊的方法，分别在测试的前后运行，这两个方法与try/except相似
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)                          #隐式等待 3秒

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_item(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):         #名字以test开头的函数都是测试方法
        self.browser.get(self.live_server_url)
        #网页头部和标题是否含有To-Do这个词
        self.assertIn('To-Do',self.browser.title)

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
        edith_list_url = self.browser.current_url

        self.check_for_row_in_item('1: Buy peacock feathers')
        self.check_for_row_in_item('2: Use peacock feathers to make a fly')
        #回车后,页面是否更新
        # self.assertTrue(
        #     any(row.text == '1: Buy peacock feathers' for row in rows),'New to-do item didnot appear in table\
        #  it was %s'%table.text)

        #使用一个新的浏览器会话
        self.browser.quit()
        self.browser = webdriver.Chrome()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
       # self.assertNotIn('Buy peacock feathers',page_text)
        #self.assertNotIn('make a fly',page_text)

        #新建待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        #获取唯一url
        personal_url = self.browser.current_url
        self.assertRegex(personal_url,'/lists/.+')
        #self.assertNotEqual(personal_url,edith_list_url)

        #没有羽毛。只有牛奶
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)


        self.fail('Finish the test!')

    def test_layout_and_styling(self):
        #首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        #显示居中
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
                               512,
                               delta=10)
        #新建清单也居中
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
                               512,
                               delta=10)

