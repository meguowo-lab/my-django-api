from typing import Any

from django.test import Client

from .utils import performing


class ModelTester:
    data: dict[Any, Any]
    path: str

    def __init__(self, client: Client) -> None:
        self.client = client

    @performing
    def post(self):
        self.client.post(self.path, self.data)

    @performing
    def get_all(self):
        self.client.get(self.path)

    @performing
    def get(self):
        self.client.get(f"{self.path}1")

    @performing
    def delete(self):
        self.client.delete(f"{self.path}1")

    @performing
    def put(self):
        self.client.put(f"{self.path}1", data=self.data)

    @performing
    def patch(self):
        self.client.patch(f"{self.path}1", data=self.data)

    def perform_mid_operations(self):
        self.get()
        self.get_all()
        self.put()
        self.patch()

    def perform(self):
        self.post()
        self.perform_mid_operations()
        self.delete()
