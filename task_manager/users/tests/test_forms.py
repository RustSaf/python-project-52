from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from task_manager.users.forms import LoginUserForm, UserForm, UserUpdateForm
from task_manager.users.models import Users

# Create your tests here.


class UserFormTest(TestCase):

    # Cоздаём объект автора модели
    @classmethod
    def setUpTestData(cls):
        Users.objects.create(
            first_name='John', last_name='Snow', username='White_Wolf'
            )

    # Проверяем текст который должен содержать поле label
    def test_userform_fields_label(self):
        # Создаем экземпляр формы
        form = UserForm()
        # Сравнить значение с ожидаемым результатом
        self.assertTrue(form.fields['first_name'].label is None or form.fields[
            'first_name'].label == _('First name'))
        self.assertTrue(form.fields['last_name'].label is None or form.fields[
            'last_name'].label == _('Last name'))
        self.assertTrue(form.fields['username'].label is None or form.fields[
            'username'].label == _('Username'))
        self.assertTrue(form.fields['password'].label is None or form.fields[
            'password'].label == _('Password'))
        self.assertTrue(form.fields[
            'password_confirm'].label is None or form.fields[
                'password_confirm'].label == _('Password confirm'))

    # Проверяем текст который должен содержать поле help_text
    def test_userform_fields_help_text(self):
        # Создаем экземпляр формы
        form = UserForm()
        # Сравнить значение с ожидаемым результатом
        self.assertEqual(form.fields['username'].help_text, _(
            """Required field. No more than 150 characters.
            Letters, numbers and symbols only @/./+/-/_."""
            ))
        self.assertEqual(form.fields['password'].help_text, _(
            "Your password must be at least 3 characters long"
            ))
        self.assertEqual(form.fields['password_confirm'].help_text, _(
            "To confirm, please enter the password again"
            ))

    # Проверка правильности работы валидации формы по имени
    def test_userform_username_is_valid(self):

        # Создаем данные формы
        username_bad = 'Qw1!~#'
        username_good = 'Qw1_@,+-'
        username_exist = 'White_Wolf'

        form_data1 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': username_bad,
                      'password': 'pass',
                      'password_confirm': 'pass'}
        form_data2 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': username_good,
                      'password': 'pass',
                      'password_confirm': 'pass'}
        form_data3 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': username_exist,
                      'password': 'pass',
                      'password_confirm': 'pass'}
        # Передаем данные в форму
        form1 = UserForm(data=form_data1)
        form2 = UserForm(data=form_data2)
        form3 = UserForm(data=form_data3)
        # Сравнить значение с ожидаемым результатом
        self.assertFalse(form1.is_valid())
        self.assertTrue(form2.is_valid())
        self.assertFalse(form3.is_valid())

    # Проверка правильности работы валидации формы по паролю
    def test_userform_password_is_valid(self):
        # Создаем данные формы
        password_small = 'Q1'
        password_good = 'Qw1'
        password_confirm_matches = 'Qw1'
        password_confirm_unmatches = 'Qw12'

        form_data1 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': 'Aegon_Targaryen',
                      'password': password_small, 
                      'password_confirm': password_small}
        form_data2 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': 'Aegon_Targaryen',
                      'password': password_good,
                      'password_confirm': password_confirm_matches}
        form_data3 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': 'Aegon_Targaryen',
                      'password': password_good,
                      'password_confirm': password_confirm_unmatches}
        # Передаем данные в форму
        form1 = UserForm(data=form_data1)
        form2 = UserForm(data=form_data2)
        form3 = UserForm(data=form_data3)
        # Сравнить значение с ожидаемым результатом
        self.assertFalse(form1.is_valid())
        self.assertTrue(form2.is_valid())
        self.assertFalse(form3.is_valid())


class UserUpdateFormTest(TestCase):

    # Cоздаём объект автора модели
    @classmethod
    def setUpTestData(cls):
        Users.objects.create(
            first_name='John', last_name='Snow', username='White_Wolf'
            )
    
    # Проверка правильности работы валидации формы по имени
    def test_userform_username_is_valid(self):

        # Создаем данные формы
        username_bad = 'Qw1!~#'
        username_good = 'Qw1_@,+-'
        username_exist = 'White_Wolf'

        form_data1 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': username_bad,
                      'password': 'pass',
                      'password_confirm': 'pass'}
        form_data2 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': username_good,
                      'password': 'pass',
                      'password_confirm': 'pass'}
        form_data3 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': username_exist,
                      'password': 'pass',
                      'password_confirm': 'pass'}
        # Передаем данные в форму
        form1 = UserUpdateForm(data=form_data1)
        form2 = UserUpdateForm(data=form_data2)
        form3 = UserUpdateForm(data=form_data3)
        # Сравнить значение с ожидаемым результатом
        self.assertFalse(form1.is_valid())
        self.assertTrue(form2.is_valid())
        self.assertFalse(form3.is_valid())

    # Проверка правильности работы валидации формы по паролю
    def test_userform_password_is_valid(self):
        # Создаем данные формы
        password_small = 'Q1'
        password_good = 'Qw1'
        password_confirm_matches = 'Qw1'
        password_confirm_unmatches = 'Qw12'

        form_data1 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': 'Aegon_Targaryen',
                      'password': password_small, 
                      'password_confirm': password_small}
        form_data2 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': 'Aegon_Targaryen',
                      'password': password_good,
                      'password_confirm': password_confirm_matches}
        form_data3 = {'first_name': 'John',
                      'last_name': 'Snow',
                      'username': 'Aegon_Targaryen',
                      'password': password_good,
                      'password_confirm': password_confirm_unmatches}
        # Передаем данные в форму
        form1 = UserUpdateForm(data=form_data1)
        form2 = UserUpdateForm(data=form_data2)
        form3 = UserUpdateForm(data=form_data3)
        # Сравнить значение с ожидаемым результатом
        self.assertFalse(form1.is_valid())
        self.assertTrue(form2.is_valid())
        self.assertFalse(form3.is_valid())


class LoginUserFormTest(TestCase):

    # Проверяем текст который должен содержать поле label
    def test_userform_fields_label(self):
        # Создаем экземпляр формы
        form = LoginUserForm()
        # Сравнить значение с ожидаемым результатом
        self.assertTrue(form.fields['username'].label is None or form.fields[
            'username'].label == _('Username'))
        self.assertTrue(form.fields['password'].label is None or form.fields[
            'password'].label == _('Password'))
