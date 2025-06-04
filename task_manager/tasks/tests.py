# Create your tests here.
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.forms import TaskForm
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
        resp2 = self.client.get('/tasks/')

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_view_url_accessible_by_name(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get(reverse('index'))
        resp2 = self.client.get(reverse('tasks:task_index'))

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_view_uses_correct_template(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get(reverse('index'))
        resp2 = self.client.get(reverse('tasks:task_index'))

        # Проверка корректности template
        self.assertTemplateUsed(resp1, 'index.html')
        self.assertTemplateUsed(resp2, 'tasks/index.html')

    def test_redirect_if_not_logged_in(self):
        
        # Не залогиненый пользователь получает response
        resp1 = self.client.get('/tasks/')
        resp2 = self.client.get('/tasks/1/update/')
        resp3 = self.client.get('/tasks/1/delete/', follow=True)
        self.assertRedirects(resp1, '/login/?next=/tasks/')
        self.assertRedirects(resp2, '/login/?next=/tasks/1/update/')
        self.assertRedirects(resp3, '/login/?next=/tasks/1/delete/')

        # Cмотрим текст сообщения и тэг
        messages_list = list(resp3.context['messages'])
        message = messages_list[0]
        self.assertEqual(message.message,
                         _('You are not logged in! Please sign in.'))
        self.assertEqual(message.tags, 'alert alert-danger error')


class TaskCreateViewTest(TestCase):

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
            name='Label2'
            )
    
    def test_view_url_exists_at_desired_location(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp = self.client.get('/tasks/create/')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp = self.client.get(reverse('tasks:task_create'))
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_form_and_message(self):

        data = {'name': 'Task1', 'discription': 'Discription for Task1',
                 'status': self.status.pk, 'executor': self.author2.pk,
                 'label': [self.label1.pk, self.label2.pk]}

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get(reverse('tasks:task_create'))
        resp2 = self.client.post(reverse('tasks:task_create'),
                                 data, follow=True)
        
        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'tasks/create.html')
        self.assertRedirects(resp2, '/tasks/')
        self.assertTemplateUsed(resp2, 'tasks/index.html')
        self.assertIn('form', resp1.context)
        self.assertContains(resp1, '<form')
        self.assertIsInstance(resp1.context['form'], TaskForm)

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list1 = list(resp2.context['messages'])
        self.assertEqual(len(messages_list1), 1)
        message = messages_list1[0]
        self.assertEqual(message.message, _('Task created successfully'))
        self.assertEqual(message.tags, 'alert alert-success success')
        

class TaskUpdateViewTest(TestCase):

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
            name='Status2'
            )

        self.label1 = Labels.objects.create(
            name='Label1'
            )

        self.label2 = Labels.objects.create(
            name='Label2'
            )

        self.task = Tasks.objects.create(
            author='White_Wolf', 
            name='Task1', discription='Discription for Task1',
            status=Statuses.objects.get(id=1),
            executor=Users.objects.get(id=1),
        )
        self.task.label.add(self.label1)      

    
    def test_view_url_exists_at_desired_location(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp = self.client.get('/tasks/1/update/', follow=True)
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_form_and_message(self):

        data1 = {'name': 'Task2', 'discription': 'Discription for Task2',
                 'status': self.status2.pk, 'executor': self.author2.pk,
                 'label': self.label2.pk}
        data2 = {'name': 'Task3', 'discription': 'Discription for Task3',
                 'status': self.status1.pk, 'executor': self.author2.pk,
                 'label': [self.label1.pk, self.label2.pk]}
            
        # Логинимся под первым пользователем, получаем response по id=1,
        # обновляем данные задачи
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get('/tasks/1/update/')
        resp2 = self.client.post('/tasks/1/update/', data1, follow=True)
        # Логинимся под вторым пользователем, получаем response по id=1,
        # обновляем данные задачи
        self.client.login(username='Born_of_the_Storm', password='12345')
        resp3 = self.client.get('/tasks/1/update/')
        resp4 = self.client.post('/tasks/1/update/', data2, follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp4.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'tasks/update.html')
        self.assertRedirects(resp2, '/tasks/')
        self.assertTemplateUsed(resp2, 'tasks/index.html')
        self.assertTemplateUsed(resp3, 'tasks/update.html')
        self.assertRedirects(resp4, '/tasks/')
        self.assertTemplateUsed(resp4, 'tasks/index.html')
        self.assertIn('form', resp1.context)
        self.assertContains(resp1, '<form')
        self.assertIsInstance(resp1.context['form'], TaskForm)

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list1 = list(resp2.context['messages'])
        self.assertEqual(len(messages_list1), 1)
        message = messages_list1[0]
        self.assertEqual(message.message, _('The task was successfully modified'))
        self.assertEqual(message.tags, 'alert alert-success success')
        

class TaskDeleteViewTest(TestCase):

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
            name='Status'
            )

        self.label = Labels.objects.create(
            name='Label'
            )

        self.task1 = Tasks.objects.create(
            author='White_Wolf', 
            name='Task1', discription='Discription for Task1',
            status=Statuses.objects.get(id=1),
            executor=Users.objects.get(id=1),
        )
        self.task1.label.add(self.label)

        self.task2 = Tasks.objects.create(
            author='White_Wolf', 
            name='Task2', discription='Discription for Task2',
            status=Statuses.objects.get(id=1),
            executor=Users.objects.get(id=1),
        )
        self.task1.label.add(self.label)   

    def test_view_url_exists_at_desired_location(self):

        # Логинимся и получаем response
        self.client.login(username='White_Wolf', password='12345')
        resp = self.client.get('/tasks/1/delete/', follow=True)
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_message(self):
        
        # Логинимся под первым пользователем до и после удаления
        # и получаем response по id=1
        self.client.login(username='White_Wolf', password='12345')
        resp1 = self.client.get('/tasks/1/delete/')
        resp2 = self.client.post('/tasks/1/delete/', follow=True)
        # Логинимся под вторым пользователем
        # и получаем response по id=2 (автор - первый пользователь)
        self.client.login(username='Born_of_the_Storm', password='12345')
        resp3 = self.client.get('/tasks/2/delete/', follow=True)

        # Проверка ответа на запрос
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)

        # Проверка корректности template и формы
        self.assertTemplateUsed(resp1, 'tasks/delete.html')
        self.assertRedirects(resp2, '/tasks/')
        self.assertTemplateUsed(resp2, 'tasks/index.html')
        self.assertRedirects(resp3, '/tasks/')
        self.assertTemplateUsed(resp3, 'tasks/index.html')

        # Должно быть хотябы одно сообщение, смотрим текст сообщения и тэг
        messages_list1 = list(resp2.context['messages'])
        self.assertEqual(len(messages_list1), 1)
        message = messages_list1[0]
        self.assertEqual(message.message, _('Task deleted successfully'))
        self.assertEqual(message.tags, 'alert alert-success success')

        messages_list2 = list(resp3.context['messages'])
        self.assertEqual(len(messages_list2), 1)
        message = messages_list2[0]
        self.assertEqual(message.message,
                         _('A task can only be deleted by its author'))
        self.assertEqual(message.tags, 'alert alert-danger error')

