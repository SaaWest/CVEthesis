import unittest
import requestAPI as req
import cpeParser as cpe
import sys
class TestAPIrequest(unittest.TestCase):
    def testPypi_isList(self):
        #sys.argv[1] = "CVE-2026-32711"
        r = req.makeNISTrequest("CVE-2026-32711")
        response = req.makeNISTrequest(r)
        versions = req.get_versions(response)
        verionList = cpe.dockerCPE_versions(versions)
        product = cpe.parse_productAndVersion(versions, versionList=verionList)
        whlFile = req.makePyPi_aptRequest(product)
        pyVer = req.getPythonVersion_Pypi(whlFile, product)
        self.assertIsInstance(pyVer, list)


if __name__=='__main__':
    unittest.main()