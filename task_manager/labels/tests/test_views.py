from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.forms import LabelForm, LabelUpdateForm
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
        resp2 = self.client.get('/labels/')

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_view_url_accessible_by_name(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get(reverse('index'))
        resp2 = self.client.get(reverse('labels:label_index'))

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_view_uses_correct_template(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get(reverse('index'))
        resp2 = self.client.get(reverse('labels:label_index'))

        # Проверка корректности template
        self.assertTemplateUsed(resp1, 'index.html')
        self.assertTemplateUsed(resp2, 'labels/index.html')

    def test_redirect_if_not_logged_in(self):
        
        # Не залогиненый пользователь получает response
        resp1 = self.client.get('/labels/')
        resp2 = self.client.get('/labels/1/update/')
        resp3 = self.client.get('/labels/1/delete/', follow=True)
        self.assertRedirects(resp1, '/login/?next=/labels/')
        self.assertRedirects(resp2, '/login/?next=/labels/1/update/')
        self.assertRedirects(resp3, '/login/?next=/labels/1/delete/')

        # Cмотрим текст сообщения и тэг
        messages_list = list(resp3.context['messages'])
        message = messages_list[0]
        self.assertEqual(message.message,
                         _('You are not logged in! Please sign in.'))
        self.assertEqual(message.tags, 'alert alert-danger error')


class LabelCreateViewTest(TestCase):

    def setUp(self):

        self.author = Users.objects.create_user(
            first_name='John', last_name='Snow',
            username='White_Wolf',
            password='12345'
            )
    
    def test_view_url_exists_at_desired_location(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp = self.client.get('/labels/create/')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp = self.client.get(reverse('labels:label_create'))
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_form_and_message(self):

        data = {'name': 'Label1'}
        data_exist = {'name': 'Label1'}

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get(reverse('labels:label_create'))
        resp2 = self.client.post(reverse('labels:label_create'),
                                 data, follow=True)
        resp3 = self.client.post(reverse('labels:label_create'),
                                 data_exist, follow=True)
        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'labels/create.html')
        self.assertRedirects(resp2, '/labels/')
        self.assertTemplateUsed(resp2, 'labels/index.html')
        self.assertIn('form', resp1.context)
        self.assertContains(resp1, '<form')
        self.assertIsInstance(resp1.context['form'], LabelForm)

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list = list(resp2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        message = messages_list[0]
        self.assertEqual(message.message, _('Label created successfully'))
        self.assertEqual(message.tags, 'alert alert-success success')

        # Проверяем текст сообщения формы при неудачном обновлении
        form1 = resp3.context['form']
        # Проверяем наличие ошибок в поле
        self.assertIn('name', form1.errors)
        self.assertEqual(form1.errors['name'][0],
                    _('A label with this name already exists.')
                        )
        

class LabelUpdateViewTest(TestCase):

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

        self.status = Statuses.objects.create(
            name='Status1'
            )

        self.label1 = Labels.objects.create(
            name='Label1'
            )

        self.label2 = Labels.objects.create(
            name='Label3'
            )
        
        self.task = Tasks.objects.create(
            author='White_Wolf', 
            name='Task1', discription='Discription for Task1',
            status=Statuses.objects.get(id=1),
            executor=Users.objects.get(id=1),
        )
        self.task.labels.add(self.label1)      
 
    def test_view_url_exists_at_desired_location(self):

        # Логинимся и получаем response
        self.client.login(username='Born_of_the_Storm', password='12345')
        resp = self.client.get('/labels/1/update/', follow=True)
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_form_and_message(self):

        data = {'name': 'Label2'}
        data_exist = {'name': 'Label3'}
            
        # Логинимся под вторым пользователем, получаем response по id=1,
        # обновляем данные статуса
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get('/labels/1/update/')
        resp2 = self.client.post('/labels/1/update/', data, follow=True)
        resp3 = self.client.post('/labels/1/update/', data_exist, follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'labels/update.html')
        self.assertRedirects(resp2, '/labels/')
        self.assertTemplateUsed(resp2, 'labels/index.html')
        self.assertIn('form', resp1.context)
        self.assertContains(resp1, '<form')
        self.assertIsInstance(resp1.context['form'], LabelUpdateForm)

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list = list(resp2.context['messages'])
        self.assertEqual(len(messages_list), 1)
        message = messages_list[0]
        self.assertEqual(message.message, _(
            'The label has been changed successfully'))
        self.assertEqual(message.tags, 'alert alert-success success')

        # Проверяем текст сообщения формы при неудачном обновлении
        form1 = resp3.context['form']
        # Проверяем наличие ошибок в поле
        self.assertIn('name', form1.errors)
        self.assertEqual(form1.errors['name'][0],
                    _('A label with this name already exists.')
                        )
        

class LabelDeleteViewTest(TestCase):

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
        self.task.labels.add(self.label)

    def test_view_url_exists_at_desired_location(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp = self.client.get('/labels/1/delete/', follow=True)
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_message(self):
        
        # Логинимся и получаем response по id=1 (метка используется)
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get('/labels/1/delete/')
        resp2 = self.client.post('/labels/1/delete/', follow=True)

        # Обновляем данные задачи, освобождая поле метки
        data = {'name': 'Task1', 'discription': 'Discription for Task1',
                 'status': self.status.pk, 'executor': self.author.pk}
        self.task.labels.clear()
        self.client.post('/tasks/1/update/', data)

        # Логинимся и получаем response по id=1 (метка освобождена
        # от использования)
        self.client.login(username='White_Wolf', password='12345')
        resp3 = self.client.get('/labels/1/delete/')
        resp4 = self.client.post('/labels/1/delete/', follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp4.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'labels/delete.html')
        self.assertRedirects(resp2, '/labels/')
        self.assertTemplateUsed(resp2, 'labels/index.html')
        self.assertTemplateUsed(resp3, 'labels/delete.html')
        self.assertRedirects(resp4, '/labels/')
        self.assertTemplateUsed(resp4, 'labels/index.html')

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list1 = list(resp2.context['messages'])
        self.assertEqual(len(messages_list1), 1)
        message = messages_list1[0]
        self.assertEqual(message.message,
                         _('Cannot delete label because it is in use'))
        self.assertEqual(message.tags, 'alert alert-danger error')        

        messages_list2 = list(resp4.context['messages'])
        self.assertEqual(len(messages_list2), 1)
        message = messages_list2[0]
        self.assertEqual(message.message, _('Label successfully removed'))
        self.assertEqual(message.tags, 'alert alert-success success')
