from unittest import TestCase

import importlib
hello = importlib.import_module("honeycomb-opentelemetry-python.hello")
# funky import needed because dashes are weird in python modules

class UnitTestHello(TestCase):
    def test_hello(self):
        self.assertEqual(
            "Hello World", hello.hello_world()
        )
