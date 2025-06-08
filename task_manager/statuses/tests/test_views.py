from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.forms import StatusForm, StatusUpdateForm
from task_manager.tasks.models import Labels, Statuses, Tasks, Users


# Create your tests here.
class IndexViewTest(TestCase):

    def setUp(self):

        author = Users.objects.create_user(
            first_name='John', last_name='Snow',
            username='White_Wolf',
            password='12345'
            )
        author.save()

    def test_view_url_exists_at_desired_location(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get('/')
        resp2 = self.client.get('/statuses/')

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_view_url_accessible_by_name(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get(reverse('index'))
        resp2 = self.client.get(reverse('statuses:status_index'))

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_view_uses_correct_template(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get(reverse('index'))
        resp2 = self.client.get(reverse('statuses:status_index'))

        # Проверка корректности template
        self.assertTemplateUsed(resp1, 'index.html')
        self.assertTemplateUsed(resp2, 'statuses/index.html')

    def test_redirect_if_not_logged_in(self):
        
        # Не залогиненый пользователь получает response
        resp1 = self.client.get('/statuses/')
        resp2 = self.client.get('/statuses/1/update/')
        resp3 = self.client.get('/statuses/1/delete/', follow=True)
        self.assertRedirects(resp1, '/login/?next=/statuses/')
        self.assertRedirects(resp2, '/login/?next=/statuses/1/update/')
        self.assertRedirects(resp3, '/login/?next=/statuses/1/delete/')

        # Cмотрим текст сообщения и тэг
        messages_list = list(resp3.context['messages'])
        message = messages_list[0]
        self.assertEqual(message.message,
                         _('You are not logged in! Please sign in.'))
        self.assertEqual(message.tags, 'alert alert-danger error')


class StatusCreateViewTest(TestCase):

    def setUp(self):

        self.author = Users.objects.create_user(
            first_name='John', last_name='Snow',
            username='White_Wolf',
            password='12345'
            )
    
    def test_view_url_exists_at_desired_location(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp = self.client.get('/statuses/create/')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp = self.client.get(reverse('statuses:status_create'))
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_form_and_message(self):

        data = {'name': 'Status1'}
        data_exist = {'name': 'Status1'}

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get(reverse('statuses:status_create'))
        resp2 = self.client.post(reverse('statuses:status_create'),
                                 data, follow=True)
        resp3 = self.client.post(reverse('statuses:status_create'),
                                 data_exist, follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'statuses/create.html')
        self.assertRedirects(resp2, '/statuses/')
        self.assertTemplateUsed(resp2, 'statuses/index.html')
        self.assertIn('form', resp1.context)
        self.assertContains(resp1, '<form')
        self.assertIsInstance(resp1.context['form'], StatusForm)

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list = list(resp2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        message = messages_list[0]
        self.assertEqual(message.message, _('Status created successfully'))
        self.assertEqual(message.tags, 'alert alert-success success')

        # Проверяем текст сообщения формы при неудачном обновлении
        form1 = resp3.context['form']
        # Проверяем наличие ошибок в поле
        self.assertIn('name', form1.errors)
        self.assertEqual(form1.errors['name'][0],
                    _('A status with this name already exists.')
                        )
        

class StatusUpdateViewTest(TestCase):

    def setUp(self):

        self.author1 = Users.objects.create_user(
            first_name='John', last_name='Snow',
            username='White_Wolf',
            password='12345'
            )

        self.author2 = Users.objects.create_user(
            first_name='Daenerys', last_name='Targaryen',
            username='Born_of_the_Storm',
            password='12345'
            )

        self.status1 = Statuses.objects.create(
            name='Status1'
            )
        
        self.status2 = Statuses.objects.create(
            name='Status3'
            )

        self.label = Labels.objects.create(
            name='Label1'
            )

        self.task = Tasks.objects.create(
            author='White_Wolf', 
            name='Task1', discription='Discription for Task1',
            status=Statuses.objects.get(id=1),
            executor=Users.objects.get(id=1),
        )
        self.task.label.add(self.label) 
 
    def test_view_url_exists_at_desired_location(self):

        # Логинимся и получаем response
        self.client.login(username='Born_of_the_Storm', password='12345')
        resp = self.client.get('/statuses/1/update/', follow=True)
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_form_and_message(self):

        data = {'name': 'Status2'}
        data_exist = {'name': 'Status3'}
            
        # Логинимся под вторым пользователем, получаем response по id=1,
        # обновляем данные статуса
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get('/statuses/1/update/')
        resp2 = self.client.post('/statuses/1/update/', data, follow=True)
        resp3 = self.client.post('/statuses/1/update/', data_exist, follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'statuses/update.html')
        self.assertRedirects(resp2, '/statuses/')
        self.assertTemplateUsed(resp2, 'statuses/index.html')
        self.assertIn('form', resp1.context)
        self.assertContains(resp1, '<form')
        self.assertIsInstance(resp1.context['form'], StatusUpdateForm)

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list = list(resp2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        message = messages_list[0]
        self.assertEqual(message.message, _('Status changed successfully'))
        self.assertEqual(message.tags, 'alert alert-success success')

        # Проверяем текст сообщения формы при неудачном обновлении
        form1 = resp3.context['form']
        # Проверяем наличие ошибок в поле
        self.assertIn('name', form1.errors)
        self.assertEqual(form1.errors['name'][0],
                    _('A status with this name already exists.')
                        )
        

class StatusDeleteViewTest(TestCase):

    def setUp(self):

        self.author = Users.objects.create_user(
            first_name='John', last_name='Snow',
            username='White_Wolf',
            password='12345'
            )

        self.status = Statuses.objects.create(
            name='Status1'
            )
        
        self.label = Labels.objects.create(
            name='Label1'
            )

        self.task = Tasks.objects.create(
            author='White_Wolf', 
            name='Task1', discription='Discription for Task1',
            status=Statuses.objects.get(id=1),
            executor=Users.objects.get(id=1),
        )
        self.task.label.add(self.label)

    def test_view_url_exists_at_desired_location(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp = self.client.get('/statuses/1/delete/', follow=True)
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_message(self):
        
        # Логинимся и получаем response по id=1 (статус используется)
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get('/statuses/1/delete/')
        resp2 = self.client.post('/statuses/1/delete/', follow=True)

        # Обновляем данные задачи, освобождая поле статуса
        data = {'name': 'Task1', 'discription': 'Discription for Task1',
                 'status': '', 'executor': self.author.pk,
                 'label': self.label.pk}
        self.client.post('/tasks/1/update/', data)

        # Логинимся и получаем response по id=1 (статус освобожден
        # от использования)
        self.client.login(username='White_Wolf', password='12345')
        resp3 = self.client.get('/statuses/1/delete/')
        resp4 = self.client.post('/statuses/1/delete/', follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp4.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'statuses/delete.html')
        self.assertRedirects(resp2, '/statuses/')
        self.assertTemplateUsed(resp2, 'statuses/index.html')
        self.assertTemplateUsed(resp3, 'statuses/delete.html')
        self.assertRedirects(resp4, '/statuses/')
        self.assertTemplateUsed(resp4, 'statuses/index.html')

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list1 = list(resp2.context['messages'])
        self.assertEqual(len(messages_list1), 1)
        message = messages_list1[0]
        self.assertEqual(message.message,
                         _('Cannot delete status because it is in use'))
        self.assertEqual(message.tags, 'alert alert-danger error')        

        messages_list2 = list(resp4.context['messages'])
        self.assertEqual(len(messages_list2), 1)
        message = messages_list2[0]
        self.assertEqual(message.message, _('Status deleted successfully'))
        self.assertEqual(message.tags, 'alert alert-success success')
