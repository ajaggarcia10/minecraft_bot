import unittest
from unittest.mock import patch
import sqlite3
import main as mc

class MinecraftBotTestCase(unittest.TestCase):
    conn = sqlite3.connect('test_minecraft.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS worlds (World_Name TEXT , Location_Name 
    TEXT, X INTEGER, Y INTEGER, Z INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS maps (World_Name TEXT PRIMARY KEY, Seed_Number 
    INTEGER, Map TEXT)''')

    def test_nether(self):
        expected = 'x:80, z:80 in the Nether is: x:10, z:10'
        self.assertEqual(mc.calculate_nether(80, 80), expected)

    def test_add_coords(self):
        add = mc.add_coords('Testing', 'Test', 550, 45, 45)
        expected_add = 'Testing/Test: 550, 45, 45 was added!'
        self.assertEqual(add, expected_add)

    def test_search_coords_one(self):
        add = mc.add_coords('Test', 'Testing', 69, 69, 69)
        expected = [('Test', 'Testing', 69, 69, 69)]
        test = mc.search_coords('Test', 'Testing')
        self.assertEqual(test, expected)

    def test_del_coords(self):
        delete = mc.del_coords('Testing', 'Test')
        self.assertEqual(delete, 'Testing/Test: x:550, y:45, z:45 has been deleted.')

    def test_search_world(self):
        add = mc.add_coords('Test', 'Testing', 69, 69, 69)
        add = mc.add_coords('Test', 'Testing', 69, 69, 69)
        search = mc.search_world('Test')
        self.assertEqual(len(search), 3)

    def test_update_coords(self):
        update = mc.update_coords('Test', 'Testing')
        expected = 'Test/Testing: x:69, y:69, z:69 has been updated to Test/Testing: ' \
                   'x:1, y:2, z:3'
        self.assertEqual(update, expected)

if __name__ == '__main__':
    unittest.main()
