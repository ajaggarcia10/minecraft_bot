import sys
import sqlite3

def db_connect():
    conn = sqlite3.connect('minecraft.db')
    db = conn.cursor()
    return db


def calculate_nether(overworld_x, overworld_z):
    ''' CALCULATES NETHER PORTAL COORDINATES '''
    try:
        nether_x = round(int(overworld_x)/8)
        nether_z = round(int(overworld_z)/8)
        nether = str(overworld_x) + ', ' + str(overworld_z) + ' in the Nether is: ' + \
                 str(nether_x) + ', ' + str(nether_z)
        return nether
    except ValueError:
        print('Coordinates must be numbers!')
    except Exception as e:
        print('Unexpected Error!')
        print(e)


def search_coords(world_name, location_name):
    try:
        db = db_connect()
        coords = db.execute("""SELECT X, Y, Z FROM worlds WHERE World_Name = '{}' AND Location_Name 
        = '{}'""".format(world_name, location_name))
        for row in coords:
            coordinates = (world_name + '/' + location_name + ': ' + str(row).strip('(,)'))
            return coordinates
    except Exception as e:
        print(e)


def add_coords(world_name, location_name, x, y, z):
    try:
        conn = sqlite3.connect('minecraft.db')
        db = conn.cursor()
        db.execute('''INSERT INTO worlds VALUES ('{}', '{}', {}, {}, {})'''.format(
                    world_name, location_name, x, y, z))
        conn.commit()
        coords = (world_name + '/' + location_name + ': ' + str(x) + ', ' + str(y) + ', ' + str(z)
                  + ' was added!')
        return coords
    except ValueError:
        print('Incorrect Formatting!')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'nether':
            print(calculate_nether(sys.argv[2], sys.argv[3]))
        elif sys.argv[1] == 'coords':
            print(search_coords(sys.argv[2], sys.argv[3]))
        elif sys.argv[1] == 'add':
            print(add_coords(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]))
    except IndexError:
        print('Not Enough Values!')


