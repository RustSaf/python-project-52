from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.users.forms import LoginUserForm, UserForm, UserUpdateForm
from task_manager.users.models import Users


# Create your tests here.
class IndexViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):

        resp1 = self.client.get('/')
        resp2 = self.client.get('/users/')

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_view_url_accessible_by_name(self):

        resp1 = self.client.get(reverse('index'))
        resp2 = self.client.get(reverse('users:user_index'))

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_view_uses_correct_template(self):

        resp1 = self.client.get(reverse('index'))
        resp2 = self.client.get(reverse('users:user_index'))

        # Проверка корректности template
        self.assertTemplateUsed(resp1, 'index.html')
        self.assertTemplateUsed(resp2, 'users/index.html')

    def test_redirect_if_not_logged_in(self):

        resp1 = self.client.get('/users/1/update/')
        resp2 = self.client.get('/users/1/delete/', follow=True)
        self.assertRedirects(resp1, '/login/?next=/users/1/update/')
        self.assertRedirects(resp2, '/login/?next=/users/1/delete/')

        # Должно быть два сообщения, смотрим текст сообщения и тэг
        messages_list = list(resp2.context['messages'])
        self.assertEqual(len(messages_list), 2)
        message = messages_list[0]
        self.assertEqual(message.message,
                         _('You are not logged in! Please sign in.'))
        self.assertEqual(message.tags, 'alert alert-danger error')


class LoginUserViewTest(TestCase):

    def setUp(self):
        author = Users.objects.create_user(
            first_name='John', last_name='Snow', username='White_Wolf',
            password='12345'
            )
        author.save()
  
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/login/')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('login'))
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)
    
    def test_logged_in_uses_correct_template_and_form_and_message(self):

        data_good = {'username': 'White_Wolf', 'password': '12345'}
        data_bad = {'username': 'White_Wolf2', 'password': '123456'}
        resp1 = self.client.get(reverse('login'))
        resp2 = self.client.post(reverse('login'), data_good, follow=True)
        resp3 = self.client.post(reverse('login'), data_bad, follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)

        # Проверка корректности template
        self.assertTemplateUsed(resp1, 'login.html')

        # Проверка корректности формы
        self.assertIsInstance(resp1.context['form'], LoginUserForm)

        # Проверка что пользователь залогинился/незалогинился и 
        # выдается нужный tamplate
        self.assertEqual(str(resp2.context['user'].username), 'White_Wolf')
        self.assertRedirects(resp2, '/')
        self.assertTemplateUsed(resp2, 'index.html')
        self.assertTemplateUsed(resp3, 'login.html')

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list1 = list(resp2.context['messages'])
        self.assertEqual(len(messages_list1), 1)
        message = messages_list1[0]
        self.assertEqual(message.message, _('You are logged in'))
        self.assertEqual(message.tags, 'alert alert-success success')

        # Проверяем текст сообщения при неудачном входе из вывода формы
        form = resp3.context['form']
        # Проверяем наличие ошибок в поле
        self.assertIn('__all__', form.errors)
        self.assertEqual(form.errors['__all__'][0],
        _("""Please enter a correct Username and password. Note that both fields may be case-sensitive.""")  # noqa: E501
                        )


class LogoutUserViewTest(TestCase):

    def setUp(self):
        author = Users.objects.create_user(
            first_name='John', last_name='Snow', username='White_Wolf',
            password='12345'
            )
        author.save()

    def test_view_uses_correct_template_and_message(self):

        # Логинимся и разлогиниваемся
        self.client.login(username='White_Wolf', password='12345')
        self.client.logout()
        resp = self.client.get(reverse('logout'), follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

        # Проверка корректности template
        self.assertRedirects(resp, '/')
        self.assertTemplateUsed(resp, 'index.html')

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list1 = list(resp.context['messages'])
        self.assertEqual(len(messages_list1), 1)
        message = messages_list1[0]
        self.assertEqual(message.message, _('You are logged out'))
        self.assertEqual(message.tags, 'alert alert-primary success')


class UserCreateViewTest(TestCase):
    
    def test_view_url_exists_at_desired_location(self):

        resp = self.client.get('/users/create/')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):

        resp = self.client.get(reverse('users:user_create'))
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_form_and_message(self):

        data_good = {'first_name': 'John', 'last_name': 'Snow',
                 'username': 'White_Wolf', 'password1': '12345',
                 'password2': '12345'}
        data_bad1 = {'first_name': 'John', 'last_name': 'Snow',
                 'username': 'White_Wolf~!', 'password1': '12345',
                 'password2': '12345'}
        data_bad2 = {'first_name': 'John', 'last_name': 'Snow',
                 'username': 'Aegon_Targaryen', 'password1': '12',
                 'password2': '12'}
        data_bad3 = {'first_name': 'John', 'last_name': 'Snow',
                 'username': 'Aegon_Targaryen', 'password1': '123',
                 'password2': ''}
        resp1 = self.client.get(reverse('users:user_create'))
        resp2 = self.client.post(reverse('users:user_create'),
                                 data_good, follow=True)
        resp3 = self.client.post(reverse('users:user_create'),
                                 data_bad1, follow=True)
        resp4 = self.client.post(reverse('users:user_create'),
                                 data_good, follow=True)
        resp5 = self.client.post(reverse('users:user_create'),
                                 data_bad2, follow=True)
        resp6 = self.client.post(reverse('users:user_create'),
                                 data_bad3, follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp4.status_code, 200)
        self.assertEqual(resp5.status_code, 200)
        self.assertEqual(resp6.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'users/create.html')
        self.assertRedirects(resp2, '/login/')
        self.assertTemplateUsed(resp2, 'login.html')
        self.assertIn('form', resp1.context)
        self.assertContains(resp1, '<form')
        self.assertIsInstance(resp1.context['form'], UserForm)

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list1 = list(resp2.context['messages'])
        self.assertEqual(len(messages_list1), 1)
        message = messages_list1[0]
        self.assertEqual(message.message, _('User successfully registered'))
        self.assertEqual(message.tags, 'alert alert-success success')

        # Проверяем текст сообщения формы при неудачной регистрации
        form1 = resp3.context['form']
        form2 = resp4.context['form']
        form3 = resp5.context['form']
        form4 = resp6.context['form']
        # Проверяем наличие ошибок в поле
        self.assertIn('username', form1.errors)
        self.assertEqual(form1.errors['username'][0],
                    _("""Please enter a valid username.
                    It can only contain letters,
                    numbers and @/./+/-/_ signs.""")
                        )
        self.assertIn('username', form2.errors)
        self.assertEqual(form2.errors['username'][0],
                    _("""A user with this name already exists.""")
                        )
        self.assertIn('password1', form3.errors)
        self.assertEqual(form3.errors['password1'][0],
                    _("""The password you entered is too short.
                    It must support at least 3 characters.""")
                        )
        self.assertIn('password2', form4.errors)
        self.assertEqual(form4.errors['password2'][0],
                    _("Required field.")
                        )
        

class UserUpdateViewTest(TestCase):

    def setUp(self):

        author1 = Users.objects.create_user(
            first_name='John', last_name='Snow',
            username='White_Wolf',
            password='12345'
            )
        author1.save()

        author2 = Users.objects.create_user(
            first_name='Daenerys', last_name='Targaryen',
            username='Born_of_the_Storm',
            password='12345'
            )
        author2.save()
    
    def test_view_url_exists_at_desired_location(self):

        resp = self.client.get('/users/1/update/', follow=True)
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_form_and_message(self):

        data = {'first_name': 'John1', 'last_name': 'Snow1',
                'username': 'White_Wolf', 'password1': '12345',
                'password2': '12345'}
        
        # Логинимся под первым пользователем, получаем response по id=1
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get('/users/1/update/')
        resp2 = self.client.post('/users/1/update/', data, follow=True)
        # Логинимся снова под первым пользователем, получаем response 
        # на get-запрос по id=2
        self.client.login(username='White_Wolf', password='12345')
        resp3 = self.client.get('/users/2/update/', follow=True)
        # Логинимся под вторым пользователем, получаем response 
        # на post-запрос по id=2 и подставляем данные с username 
        # первого пользователя
        self.client.login(username='Born_of_the_Storm', password='12345')
        resp4 = self.client.post('/users/2/update/', data, follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp4.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'users/update.html')
        self.assertRedirects(resp2, '/users/')
        self.assertTemplateUsed(resp2, 'users/index.html')
        self.assertRedirects(resp3, '/users/')
        self.assertTemplateUsed(resp3, 'users/index.html')
        self.assertIn('form', resp1.context)
        self.assertContains(resp1, '<form')
        self.assertIsInstance(resp1.context['form'], UserUpdateForm)

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list1 = list(resp2.context['messages'])
        self.assertEqual(len(messages_list1), 1)
        message = messages_list1[0]
        self.assertEqual(message.message, _('User successfully changed'))
        self.assertEqual(message.tags, 'alert alert-success success')

        messages_list2 = list(resp3.context['messages'])
        self.assertEqual(len(messages_list2), 1)
        message = messages_list2[0]
        self.assertEqual(message.message,
                         _('You do not have permission to modify another user'))
        self.assertEqual(message.tags, 'alert alert-danger error')

        # Проверяем текст сообщения формы при неудачном обновлении
        form1 = resp4.context['form']
        # Проверяем наличие ошибок в поле
        self.assertIn('username', form1.errors)
        self.assertEqual(form1.errors['username'][0],
                    _('A user with this name already exists.')
                        )
        

class UserDeleteViewTest(TestCase):

    def setUp(self):

        author1 = Users.objects.create_user(
            first_name='John', last_name='Snow',
            username='White_Wolf',
            password='12345'
            )
        author1.save()

        author2 = Users.objects.create_user(
            first_name='Daenerys', last_name='Targaryen',
            username='Born_of_the_Storm',
            password='12345'
        )
        author2.save()

    def test_view_url_exists_at_desired_location(self):

        resp = self.client.get('/users/1/delete/', follow=True)
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_message(self):
        
        # Логинимся под первым пользователем до и после удаления
        # и получаем response по id=1
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get('/users/1/delete/')
        resp2 = self.client.post('/users/1/delete/', follow=True)
        resp3 = self.client.login(username='White_Wolf', password='12345')
        # Логинимся под вторым пользователем, получаем response 
        # на get-запрос по id=1
        self.client.login(username='Born_of_the_Storm', password='12345')
        resp4 = self.client.get('/users/1/delete/', follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertFalse(resp3)  # Проверка отсутствия удаленного пользователя
        self.assertEqual(resp4.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'users/delete.html')
        self.assertRedirects(resp2, '/users/')
        self.assertTemplateUsed(resp2, 'users/index.html')
        self.assertRedirects(resp4, '/users/')
        self.assertTemplateUsed(resp4, 'users/index.html')

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list1 = list(resp2.context['messages'])
        self.assertEqual(len(messages_list1), 1)
        message = messages_list1[0]
        self.assertEqual(message.message, _('User deleted successfully'))
        self.assertEqual(message.tags, 'alert alert-success success')

        messages_list2 = list(resp4.context['messages'])
        self.assertEqual(len(messages_list2), 1)
        message = messages_list2[0]
        self.assertEqual(message.message,
                         _('You do not have permission to modify another user'))
        self.assertEqual(message.tags, 'alert alert-danger error')
