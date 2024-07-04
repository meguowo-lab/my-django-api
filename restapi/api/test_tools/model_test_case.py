from django.test import TestCase

from .model_tester import ModelTester
from .utils import create_superuser


class ModelTestCase(TestCase):
    model_tester_type: type[ModelTester]
    use_anon_user = True
    use_admin_user = True

    def test(self):
        if type(self) is ModelTestCase:
            return
        tester = self.model_tester_type(client=self.client)
        if self.use_anon_user:
            print("beginning tests with anon user...")
            tester.perform()
        if self.use_admin_user:
            password = "12345"
            user = create_superuser(password=password)
            self.client.login(username=user.username, password=password)
            print("beginning tests with admin user...")
            tester.perform()
