from django.core import mail

from .email import email_sent_event
from .test_tools import ModelTestCase, ModelTester
from .test_tools.utils import performing


class NewsTester(ModelTester):
    data = {"title": "test", "body": "test"}
    path = "/api/v1/news/"


class CommentTester(ModelTester):
    data = {"body": "test", "news_id": 1}
    path = "/api/v1/comments/"


class UserTester(ModelTester):
    data = {
        "username": "test_rat",
        "password": "tadsa123ko",
        "email": "test@testmail.test",
    }
    path = "/api/v1/users/"

    def post(self):
        super().post()
        self.client.login(
            username=self.data["username"], password=self.data["password"]
        )

    @performing
    def email_verification(self):
        self.client.post("/email-verify/")
        email_sent_event.wait()
        self.client.post(mail.outbox[0].body)

    def perform_mid_operations(self):
        self.email_verification()
        return super().perform_mid_operations()

    def delete(self):
        super().delete()


class NewsTestCase(ModelTestCase):
    model_tester_type = NewsTester


class CommentTestCase(ModelTestCase):
    model_tester_type = CommentTester


class UserTestCase(ModelTestCase):
    model_tester_type = UserTester
    use_admin_user = False

    def test(self):
        with self.settings(
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
            EMAIL_TEMPLATE="",
        ):
            super().test()
