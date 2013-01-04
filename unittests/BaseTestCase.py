import sys
import unittest2
import MockBlipTVDepends

MockBlipTVDepends.MockBlipTVDepends().mockXBMC()

sys.path.append('../plugin/')
sys.path.append('../xbmc-mocks/')

class BaseTestCase(unittest2.TestCase): #pragma: no cover
    def setUp(self):
        MockBlipTVDepends.MockBlipTVDepends().mockXBMC()
        MockBlipTVDepends.MockBlipTVDepends().mock()
