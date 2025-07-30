import unittest
import asyncio

class AsyncTestCase(unittest.TestCase):
    """Base class for async tests."""
    
    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        
    @classmethod
    def tearDownClass(cls):
        cls.loop.close()
        asyncio.set_event_loop(None)
        
    def async_test(self, coro):
        return self.__class__.loop.run_until_complete(coro)
