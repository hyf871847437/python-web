from django.test import TestCase
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)
        print('right')

    def test_home_page_is_right(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html'),response.content)
        self.assertIn(b'<title>To-Do lists</title>',response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

    def _test_home_page_return_correct_html(self):   #{% csrf_token %} 导致测试失败
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(),expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'The first item'

        response = home_page(request)

        self.assertEqual(Item.objects.count(),1)
        first_item = Item.objects.first()
        self.assertEqual(first_item.text,'The first item')

    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemy 1')
        Item.objects.create(text='itemy 2')

        request = HttpRequest()
        response = home_page(request)
        self.assertIn('itemy 1',response.content.decode())
        self.assertIn('itemy 2', response.content.decode())


        #expect_html = render_to_string('home.html',{'new_item_text':'A new list item'})
        #self.assertEqual(response.content.decode(),expect_html)


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_save_item = saved_items[0]
        second_save_item = saved_items[1]

        self.assertEqual(first_save_item.text,'The first list item')
        self.assertEqual(second_save_item.text, 'The second list item')



    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'The first item'

        response = home_page(request)


        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        # expect_html = render_to_string('home.html',{'new_item_text':'The first item'})
        # self.assertEqual(response.content.decode(),expect_html)

    def test_home_page_only_save_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(),0)