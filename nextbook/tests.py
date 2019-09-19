from nextbook.models import Posting
from django.db.models import Count
from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class SocialAuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'email' : 'user@secret.com'}
        User = get_user_model()
        user = User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')
        self.assertTrue(login)

    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

class LogInTesting(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')

    def test_login_status_code(self):
            response = self.client.get('/login/', self.credentials, follow=True)
            # Check that the response is 200 OK.
            self.assertEqual(response.status_code, 200)

    def test_logout(self):
        # Attempt to logout
        response = self.client.post('/logout/', self.credentials, follow = True)
        # Check that the user wass able to reach the page
        self.assertEqual(response.status_code, 200)

    def test_logout_no_post(self):
        # Attempt to logout
        self.client.post('/logout/', self.credentials, follow = True)
        response = self.client.get('/posting/')
        # Check that the user wass able to reach the posting page when not logged in
        self.assertEqual(response.status_code, 302)

class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'email' : 'user@secret.com'}
        User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

class ProfileTestViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'email' : 'user@secret.com'}
        User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')

    def test_home_page_status_code(self):
        response = self.client.get('/profile/1/')
        self.assertEquals(response.status_code, 200)

    def test_getProfile_loggedIn_status_code(self):
        # Issue a GET request.
        response = self.client.get('/profile/1/', self.credentials, follow=True)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

class MyBooksTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'email' : 'user@secret.com'}
        User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')
        book_posting = Posting.objects.create(book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=99.99,contact='Ryan@Ryan.com',rent_buy='B')

   # def test_getMyBooks__status_code(self):
        # Issue a GET request.
       # response = self.client.get('/mybooks/1/', self.credentials, follow=True)
        # Check that the response is 200 OK.
       # self.assertEqual(response.status_code, 200)

class EditPostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'email' : 'user@secret.com'}
        User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')

    def editObject(self):
        Posting.objects.create(book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='B')
        self.assertEqual(1,Posting.objects.all().count())



class PasswordResetTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'email' : 'user@secret.com'}
        User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')
        # user = User.objects.create_user(username='pierce', email='pierce@gmail.com', password='pierce')

    def test_password_reset_status_code(self):
        # Issue a GET request.
        response = self.client.post('/password_reset/', self.credentials, follow=True)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    # def test_change_password_page(self):
    #     self.client.get('/signup/', follow_redirects=True)
    #     self.client.post('pierce.faraone@gmail.com', 'P@ssworD', 'P@ssworD')
    #     response = self.client.get('/password_reset/')
    #     self.assertEqual(response.status_code, 200)

    # def test_view_password_reset_by_name(self):
    #     response = self.client.get(reverse('/password_reset/'))
    #     self.assertEqual(response.status_code, 200)


class RegistrationTesting(TestCase):
    def test_added_user(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')
        self.assertNumQueries(1)

class LogInTesting(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')

    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

    def test_getPost_loggedIn_status_code(self):
        # Issue a GET request.
        response = self.client.post('/posting/', self.credentials, follow=True)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_postHome_loggedIn_status_code(self):
        # Issue a GET request.
        response = self.client.post('/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

class LogInTesting(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')

    def test_logout(self):
        # Attempt to logout
        response = self.client.post('/logout/', self.credentials, follow = True)
        # Check that the user wass able to reach the page
        self.assertEqual(response.status_code, 200)

    def test_logout_no_post(self):
        # Attempt to logout
        self.client.post('/logout/', self.credentials, follow = True)
        response = self.client.get('/posting/')
        # Check that the user wass able to reach the posting page when not logged in
        self.assertEqual(response.status_code, 302)

class DisplayBooksTesting(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')

    def test_book_insert_1(self):
        Posting.objects.create(book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='B')
        self.assertEqual(1,Posting.objects.all().count())

    def test_book_insert_10(self):
        for x in range(0,10):
            Posting.objects.create(book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='B')
        self.assertEqual(10,Posting.objects.all().count())

    def test_attribute_content(self):
        Posting.objects.create(book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='B')
        book_posting = Posting.objects.get(id=1)
        expected_object_book_title = book_posting.book_title
        self.assertEquals(expected_object_book_title, 'Algo')

    def test_getHome_status_code(self):
           # Issue a GET request.
          response = self.client.get('/')
          # Check that the response is 200 OK.
          self.assertEqual(response.status_code, 200)

    def test_getPost_status_code(self):
           # Issue a GET request.
          response = self.client.get('/posting/')
          # Check that the response is 302 OK.
          self.assertEqual(response.status_code, 200)

    def test_getLogin_status_code(self):
               # Issue a GET request.
          response = self.client.get('/login/')
              # Check that the response is 200 OK.
          self.assertEqual(response.status_code, 200)

    def test_view_Login_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

class PostingModelTesting(TestCase):
    def setUp(self, book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='B'):
        # Every test needs a client.
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        login = self.client.login(username='testuser', password='secret')

    def create_example_post(self,book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='B'):
        return Posting.objects.create(book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='B')

    def test_valid_input(self):
        book_posting = Posting(book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='B')
        self.assertIs(book_posting.book_title,'Algo')
        self.assertIs(book_posting.class_assoc,'CS 4102')
        self.assertIs(book_posting.iSBN, '123456789')
        self.assertIs(book_posting.price, 100.23)
        self.assertIs(book_posting.contact, 'Ryan@Ryan.com')
        self.assertIs(book_posting.rent_buy, 'B')

    def test_invalid_title(self):
        book_posting = Posting(book_title=123,class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='B')
        with self.assertRaises(AttributeError):
            book_posting.book_title.isalpha()
        self.assertIs(book_posting.class_assoc.replace(' ','').isalnum(), True)
        self.assertIs(book_posting.iSBN.replace(' ','').isalnum(), True)
        self.assertIsInstance(book_posting.price, float)
        self.assertIs(book_posting.contact.replace(' ','').isprintable(), True)
        self.assertIs(book_posting.rent_buy.replace(' ','').isalnum(), True)

    def test_invalid_class_assoc(self):
        book_posting = Posting(book_title='Algo',class_assoc='@@@@', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='B')
        self.assertIs(book_posting.book_title.replace(' ','').isalpha(), True)
        self.assertIs(book_posting.class_assoc.replace(' ','').isalnum(), False)
        self.assertIs(book_posting.iSBN.replace(' ','').isalnum(), True)
        self.assertIsInstance(book_posting.price, float)
        self.assertIs(book_posting.contact.replace(' ','').isprintable(), True)
        self.assertIs(book_posting.rent_buy.replace(' ','').isalnum(), True)

    def test_invalid_iSBN(self):
        book_posting = Posting(book_title='Algo',class_assoc='CS 4102', iSBN ='@@@@', price=100.23,contact='Ryan@Ryan.com',rent_buy='B')
        self.assertIs(book_posting.book_title.replace(' ','').isalpha(), True)
        self.assertIs(book_posting.class_assoc.replace(' ','').isalnum(), True)
        self.assertIs(book_posting.iSBN.replace(' ','').isalnum(), False)
        self.assertIsInstance(book_posting.price, float)
        self.assertIs(book_posting.contact.replace(' ','').isprintable(), True)
        self.assertIs(book_posting.rent_buy.replace(' ','').isalnum(), True)

    def test_invalid_seller_name(self):
        book_posting = Posting(book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='B')
        self.assertIs(book_posting.book_title.replace(' ','').isalpha(), True)
        self.assertIs(book_posting.class_assoc.replace(' ','').isalnum(), True)
        self.assertIs(book_posting.iSBN.replace(' ','').isalnum(), True)
        self.assertIsInstance(book_posting.price, float)
        self.assertIs(book_posting.contact.replace(' ','').isprintable(), True)
        self.assertIs(book_posting.rent_buy.replace(' ','').isalnum(), True)

    def test_invalid_price(self):
        book_posting = Posting(book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price='hi',contact='Ryan@Ryan.com',rent_buy='B')
        self.assertIs(book_posting.book_title.replace(' ','').isalpha(), True)
        self.assertIs(book_posting.class_assoc.replace(' ','').isalnum(), True)
        self.assertIs(book_posting.iSBN.replace(' ','').isalnum(), True)
        with self.assertRaises(AssertionError):
            self.assertIsInstance(book_posting.price, float)
        self.assertIs(book_posting.contact.replace(' ','').isprintable(), True)
        self.assertIs(book_posting.rent_buy.replace(' ','').isalnum(), True)

    def test_invalid_contact(self):
        book_posting = Posting(book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='\n',rent_buy='B')
        self.assertIs(book_posting.book_title.replace(' ','').isalpha(), True)
        self.assertIs(book_posting.class_assoc.replace(' ','').isalnum(), True)
        self.assertIs(book_posting.iSBN.replace(' ','').isalnum(), True)
        self.assertIsInstance(book_posting.price, float)
        self.assertIs(book_posting.contact.replace(' ','').isprintable(), False)
        self.assertIs(book_posting.rent_buy.replace(' ','').isalnum(), True)

    def test_invalid_rent_buy(self):
        book_posting = Posting(book_title='Algo',class_assoc='CS 4102', iSBN ='123456789', price=100.23,contact='Ryan@Ryan.com',rent_buy='@')
        self.assertIs(book_posting.book_title.replace(' ','').isalpha(), True)
        self.assertIs(book_posting.class_assoc.replace(' ','').isalnum(), True)
        self.assertIs(book_posting.iSBN.replace(' ','').isalnum(), True)
        self.assertIsInstance(book_posting.price, float)
        self.assertIs(book_posting.contact.replace(' ','').isprintable(), True)
        self.assertIs(book_posting.rent_buy.replace(' ','').isalnum(), False)

    def test_Posting_creation(self):
        p = self.create_example_post()
        self.assertTrue(isinstance(p, Posting))
        self.assertEqual(p.__str__(), p.book_title)
# Create your tests here.
