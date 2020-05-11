import unittest
import sqlite3
import main as mc


class MinecraftBotTestCase(unittest.TestCase):
    conn = sqlite3.connect('test_minecraft.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS worlds (World_Name TEXT, Location_Name TEXT, 
    X INTEGER, Y INTEGER, Z INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS maps (World_Name TEXT PRIMARY KEY, Seed_Number 
    INTEGER, Map TEXT)''')
    c.execute('''INSERT INTO worlds VALUES ('Solo_Queue', 'Base', 1500, 70, 150)''')
    conn.commit()

    def test_nether(self):
        expected = '80, 80 in the Nether is: 10, 10'
        self.assertEqual(mc.calculate_nether(80, 80), expected)

    def test_search_coords(self):
        expected = 'Solo_Queue/Base: 1500, 70, 150'
        test = mc.search_coords('Solo_Queue', 'Base')
        self.assertEqual(test, expected)

    def test_add_coords(self):
        add = mc.add_coords('Test', 'Test', 150, 150, 150)
        test = mc.search_coords('Test', 'Test')
        expected = 'Test/Test: 150, 150, 150'
        self.assertEqual(test, expected)



if __name__ == '__main__':
    unittest.main()
