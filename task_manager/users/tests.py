from django.test import TestCase

# Create your tests here.
from .models import Users


class UsersModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Users.objects.create(
            first_name='John', last_name='Snow', username='White Wolf'
            )

    def test_first_name_label(self):
        author = Users.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'Name')

    def test_last_name_label(self):
        author = Users.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'Surname')

    def test_username_max_length(self):
        author = Users.objects.get(id=1)
        max_length = author._meta.get_field('username').max_length
        self.assertEquals(max_length, 150)

    def test_password_max_length(self):
        author = Users.objects.get(id=1)
        max_length = author._meta.get_field('password').max_length
        self.assertEquals(max_length, 20)

    def test_object_name(self):
        author = Users.objects.get(id=1)
        expected_object_name = author.username
        field1_name = author.first_name
        field2_name = author.last_name
        self.assertEquals(expected_object_name, str(author))
        self.assertEquals(field1_name, 'John')
        self.assertEquals(field2_name, 'Snow')

    def test_get_absolute_url(self):
        author=Users.objects.get(id=1)
        self.assertEquals(author.get_absolute_url_update(), '/users/1/update/')
        self.assertEquals(author.get_absolute_url_delete(), '/users/1/delete/')
