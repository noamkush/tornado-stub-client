# work with python 2.5, doesn't break in newer versions
from __future__ import with_statement
from unittest import TestCase
from tornado.testing import AsyncTestCase

from tornado_stub_client import stub, reset, AsyncHTTPStubClient

class IntegrationTest(AsyncTestCase, TestCase):

    def setUp(self):
        super(IntegrationTest, self).setUp()
        reset()

    def test_stub_and_fetch(self):
        client = AsyncHTTPStubClient()
        stub("/hello").and_return(body=b"world")
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b"world")

    def test_can_fetch_twice(self):
        client = AsyncHTTPStubClient()
        stub("/hello").and_return(body=b"world")
        client.fetch("/hello", self.stop)
        self.wait()
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b"world")

    def test_can_queue_stub_responses(self):
        client = AsyncHTTPStubClient()
        stub("/hello").and_return(body=b"hello")\
                      .and_return(body=b"beautiful")\
                      .and_return(body=b"world")

        # First Response
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b"hello")

        # Second Response
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b"beautiful")

        # Third Response
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b"world")

        # Fourth Response
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b"hello")

    def test_with_syntax(self):
        client = AsyncHTTPStubClient()
        with stub("/hello").and_return(body=b"world"):
            client.fetch("/hello", self.stop)
            response = self.wait()
            self.assertEqual(response.code, 200)
            self.assertEqual(response.body, b"world")
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 404)
