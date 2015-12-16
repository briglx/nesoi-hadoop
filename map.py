import pymongo
from pymongo import MongoClient
import unittest

class SetBoundsMapper():

    def __init__(self):
        # self.client = MongoClient()
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.nesoi
        self.terrain = self.db.terrain
    
    def migrate(self):



        for cell in self.terrain.find():
            mX, mY, idx = self.map(cell["x"], cell["y"])
            result = self.terrain.update_one(
                {"x": cell["x"], "y": cell["y"]},
                {"$set": {"mX": mX, "mY": mY, "idx": idx}}
            )
            print (cell["x"], cell["y"], mX, mY, idx, result.modified_count)

        

    def map(self, x, y):

        minX, minY = self.mapToMinor(x, y)
        idx = self.coordToIndex(minX, minY)

        return minX, minY, idx

        # minx = 0;
        # miny = 0;
        # for cell in terrain.find():
        #     x = cell["x"]
        #     y = cell["y"]
        #     if x < minx:
        #         minx = x
        #     if y < miny:
        #         miny = y

        # return minx, miny

    def mapToMinor(self, x, y):
        boundsMaxX = 15 + 1
        boundsMaxY = 10 + 1

        minX = x % boundsMaxX
        minY = y % boundsMaxY
        return (minX, minY)

    def coordToIndex(self, x, y):

        boundsMaxX = 15 
        boundsMaxY = 10 

        idx = ((boundsMaxX + 1) * y) + x  ;
        return idx

class TestStringMethods(unittest.TestCase):


    def setUp(self):
        self.mapper = SetBoundsMapper();

    def test_0_0(self):
        
        x, y = self.mapper.mapToMinor(0,0);

        self.assertEqual(x, 0)
        self.assertEqual(y, 0)

    def test_0_1(self):
        
        x, y = self.mapper.mapToMinor(0,1);

        self.assertEqual(x, 0)
        self.assertEqual(y, 1)

    def test_15_0(self):
        
        x, y = self.mapper.mapToMinor(15,0);

        self.assertEqual(x, 15)
        self.assertEqual(y, 0)

    def test_15_10(self):
        
        x, y = self.mapper.mapToMinor(15,10);

        self.assertEqual(x, 15)
        self.assertEqual(y, 10)

    def test_Page2_0_0(self):
        
        x, y = self.mapper.mapToMinor(16,0);

        self.assertEqual(x, 0)
        self.assertEqual(y, 0)

    def test_Page2_15_0(self):
        
        x, y = self.mapper.mapToMinor(31,0);

        self.assertEqual(x, 15)
        self.assertEqual(y, 0)

    def test_Page2_15_10(self):
        
        x, y = self.mapper.mapToMinor(31,10);

        self.assertEqual(x, 15)
        self.assertEqual(y, 10)

    def test_Page3_0_0(self):
        
        x, y = self.mapper.mapToMinor(32,0);

        self.assertEqual(x, 0)
        self.assertEqual(y, 0)

    def test_PageN1_15_0(self):
        
        x, y = self.mapper.mapToMinor(-1,0);

        self.assertEqual(x, 15)
        self.assertEqual(y, 0)

    def test_PageN1_0_0(self):
        
        x, y = self.mapper.mapToMinor(-16,0);

        self.assertEqual(x, 0)
        self.assertEqual(y, 0)

    def test_PageN2_15_0(self):
        
        x, y = self.mapper.mapToMinor(-17,0);

        self.assertEqual(x, 15)
        self.assertEqual(y, 0)

    def test_PageD1_0_0(self):
        
        x, y = self.mapper.mapToMinor(0,11);

        self.assertEqual(x, 0)
        self.assertEqual(y, 0)

    def test_PageUN1_0_0(self):
        
        x, y = self.mapper.mapToMinor(-16,-11);

        self.assertEqual(x, 0)
        self.assertEqual(y, 0)

    def test_PageUN1_15_10(self):
        
        x, y = self.mapper.mapToMinor(-1,-1);

        self.assertEqual(x, 15)
        self.assertEqual(y, 10)

    def test_PageD_7_15(self):
        
        x, y = self.mapper.mapToMinor(7,15);

        self.assertEqual(x, 7)
        self.assertEqual(y, 4)
      
    def testConvertCellToIndex(self):
        idx = self.mapper.coordToIndex(0,0)
        self.assertEqual(idx, 0)

    def testConvertCellToIndexTopRight(self):
        idx = self.mapper.coordToIndex(15,0)
        self.assertEqual(idx, 15)

    def testConvertCellToIndexBottomLeft(self):
        idx = self.mapper.coordToIndex(0,10)
        self.assertEqual(idx, 160)

    def testConvertCellToIndexBottomRight(self):
        idx = self.mapper.coordToIndex(15,10)
        self.assertEqual(idx, 175)

    def testConvertCellToIndex5_6(self):
        idx = self.mapper.coordToIndex(5,6)
        self.assertEqual(idx, 101)

    def testConvertCellToIndex15_3(self):
        idx = self.mapper.coordToIndex(15,3)
        self.assertEqual(idx, 63)

    

    def testTripleMap00(self):
        x, y, idx = self.mapper.map(0,0)
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(idx, 0)

    def testTripleMapN1_0(self):
        x, y, idx = self.mapper.map(-1,0)
        self.assertEqual(x, 15)
        self.assertEqual(y, 0)
        self.assertEqual(idx, 15)

    def testTripleMap0_n1(self):
        x, y, idx = self.mapper.map(0,-1)
        self.assertEqual(x, 0)
        self.assertEqual(y, 10)
        self.assertEqual(idx, 160)

    def testTripleMapn1_n1(self):
        x, y, idx = self.mapper.map(-1,-1)
        self.assertEqual(x, 15)
        self.assertEqual(y, 10)
        self.assertEqual(idx, 175)

    

    def testTripleMap15_0(self):
        x, y, idx = self.mapper.map(15,0)
        self.assertEqual(x, 15)
        self.assertEqual(y, 0)
        self.assertEqual(idx, 15)

    def testTripleMap15_n1(self):
        x, y, idx = self.mapper.map(15,-1)
        self.assertEqual(x, 15)
        self.assertEqual(y, 10)
        self.assertEqual(idx, 175)

    def testTripleMap16_n1(self):
        x, y, idx = self.mapper.map(16,-1)
        self.assertEqual(x, 0)
        self.assertEqual(y, 10)
        self.assertEqual(idx, 160)

    def testTripleMap16_0(self):
        x, y, idx = self.mapper.map(16,0)
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(idx, 0)

    def testTripleMap16_1(self):
        x, y, idx = self.mapper.map(16,1)
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)
        self.assertEqual(idx, 16)

    def testTripleMap15_10(self):
        x, y, idx = self.mapper.map(15,10)
        self.assertEqual(x, 15)
        self.assertEqual(y, 10)
        self.assertEqual(idx, 175)

    def testTripleMap16_10(self):
        x, y, idx = self.mapper.map(16,10)
        self.assertEqual(x, 0)
        self.assertEqual(y, 10)
        self.assertEqual(idx, 160)

    def testTripleMap16_11(self):
        x, y, idx = self.mapper.map(16,11)
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(idx, 0)

    def testTripleMap15_11(self):
        x, y, idx = self.mapper.map(15,11)
        self.assertEqual(x, 15)
        self.assertEqual(y, 0)
        self.assertEqual(idx, 15)

    def testTripleMap0_10(self):
        x, y, idx = self.mapper.map(0,10)
        self.assertEqual(x, 0)
        self.assertEqual(y, 10)
        self.assertEqual(idx, 160)

    def testTripleMap0_11(self):
        x, y, idx = self.mapper.map(0,11)
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(idx, 0)

    def testTripleMapN1_11(self):
        x, y, idx = self.mapper.map(-1,11)
        self.assertEqual(x, 15)
        self.assertEqual(y, 0)
        self.assertEqual(idx, 15)

    def testTripleMapN1_10(self):
        x, y, idx = self.mapper.map(-1,10)
        self.assertEqual(x, 15)
        self.assertEqual(y, 10)
        self.assertEqual(idx, 175)


    def testTripleMap3_3(self):
        x, y, idx = self.mapper.map(3,3)
        self.assertEqual(x, 3)
        self.assertEqual(y, 3)
        self.assertEqual(idx, 51)

    def testTripleMap13_7(self):
        x, y, idx = self.mapper.map(13,7)
        self.assertEqual(x, 13)
        self.assertEqual(y, 7)
        self.assertEqual(idx, 125)

  # def test_isupper(self):
  #     self.assertTrue('FOO'.isupper())
  #     self.assertFalse('Foo'.isupper())

  # def test_split(self):
  #     s = 'hello world'
  #     self.assertEqual(s.split(), ['hello', 'world'])
  #     # check that s.split fails when the separator is not a string
  #     with self.assertRaises(TypeError):
  #         s.split(2)

def migrateCode():
    mapper = SetBoundsMapper();
    mapper.migrate();

if __name__ == '__main__':
    # unittest.main()
    migrateCode()

