from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import Users

# Create your tests here.


class UsersModelTest(TestCase):

    # Cоздаём объект автора модели
    @classmethod
    def setUpTestData(cls):
        Users.objects.create(
            first_name='John', last_name='Snow', username='White_Wolf'
            )

    # Проверяем значения текстовых меток модели
    def test_fields_label(self):
        # Получение объекта для тестирования
        author = Users.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field1_label = author._meta.get_field('first_name').verbose_name
        field2_label = author._meta.get_field('last_name').verbose_name
        field3_label = author._meta.get_field('username').verbose_name
        field4_label = author._meta.get_field('password').verbose_name
        field5_label = author._meta.get_field('created_at').verbose_name

        self.assertEquals(field1_label, _('Name'))
        self.assertEquals(field2_label, _('Surname'))
        self.assertEquals(field3_label, _('Username'))
        self.assertEquals(field4_label, _('Password'))
        self.assertEquals(field5_label, _('Creation date'))
    
    # Проверяем ожидаемую длину текстовых меток модели
    def test_fields_max_length(self):
        # Получение объекта для тестирования
        author = Users.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        max_length1 = author._meta.get_field('first_name').max_length
        max_length2 = author._meta.get_field('last_name').max_length
        max_length3 = author._meta.get_field('username').max_length
        max_length4 = author._meta.get_field('password').max_length
        # Сравнить значение с ожидаемым результатом
        self.assertEquals(max_length1, 150)
        self.assertEquals(max_length2, 150)
        self.assertEquals(max_length3, 150)
        self.assertEquals(max_length4, 20)

    # Проверяем ожидаемую имена полей созданного объекта автора
    def test_object_name(self):
        # Получение объекта для тестирования
        author = Users.objects.get(id=1)
        # Получение значения поля
        expected_object_name = author.username
        field1_name = author.first_name
        field2_name = author.last_name
        # Сравнить значение с ожидаемым результатом
        self.assertEquals(expected_object_name, str(author))
        self.assertEquals(field1_name, 'John')
        self.assertEquals(field2_name, 'Snow')

    # Проверяем абсолютный URL, возвращаемый методом объекта
    def test_get_absolute_url(self):
        # Получение объекта для тестирования
        author=Users.objects.get(id=1)
        # Сравнить значение с ожидаемым результатом
        self.assertEquals(author.get_absolute_url_update(), '/users/1/update/')
        self.assertEquals(author.get_absolute_url_delete(), '/users/1/delete/')
