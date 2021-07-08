""" User unit test """

from utilities.user import user


class TestUser:
    def setup_method(self):
        self.name = "John Doe"
        self.email = "john@doe.cc"
        self.password = "johndoe123"
        self.user_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    def test_registration_with_unique_email(self):
        unique = user.register(self.name, self.email, self.password)
        assert unique == (3, 'John Doe')

    def test_registration_with_non_unique_email(self):
        non_unique = user.register(self.name, self.email, self.password)
        assert non_unique is None

    def test_is_email_exists_with_unique_email(self):
        exist = user.is_email_exists(self.email)
        assert exist == (3, 'John Doe')

    def test_is_email_exists_with_non_unique_email(self):
        doesnt_exist = user.is_email_exists("jane@doe.cc")
        assert doesnt_exist is None

    def test_login_corect_email_correct_password(self):
        result = user.login(self.email, self.password)
        assert result == (3, 'John Doe')

    def test_login_corect_email_inccorrect_password(self):
        result = user.login(self.email, "janedoe124")
        assert result is None

    def test_login_incorect_email_correct_password(self):
        result = user.login("jane@doe.cc", self.password)
        assert result is None

    def test_login_inccorect_email_incorrect_password(self):
        result = user.login("jane@doe.cc", "janedoe124")
        assert result is None

    def test_login_data(self):
        user_data = user.login(self.email, self.password)
        assert list(user_data)[-1] == self.name
