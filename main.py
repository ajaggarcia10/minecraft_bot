import sys
import sqlite3

conn = sqlite3.connect('minecraft.db')
db = conn.cursor()

# TO ADD
# map seed : opens map for seed number
# map add : adds map,
# map open : opens added map


def calculate_nether(overworld_x, overworld_z):
    ''' CALCULATES NETHER PORTAL COORDINATES '''
    try:
        nether_x = round(int(overworld_x)/8)
        nether_z = round(int(overworld_z)/8)
        nether = 'x:' + str(overworld_x) + ', ' + 'z:' + str(overworld_z) + ' in the Nether is: '\
                 + 'x:' + str(nether_x) + ', ' + 'z:' + str(nether_z)
        return nether
    except ValueError:
        print('Coordinates must be numbers!')
    except Exception as e:
        print('Unexpected Error!')
        print(e)


def add_coords(world_name, location_name, x, y, z):
    ''' ADDS A COORDINATE TO DATABASE '''
    try:
        # conn = sqlite3.connect('minecraft.db')
        # db = conn.cursor()
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


def search_coords(world_name, location_name):
    ''' LOOKS UP COORDINATES IN THE DATABASE '''
    try:
        db.execute("""SELECT * FROM worlds WHERE World_Name = '{}' AND Location_Name 
                      = '{}'""".format(world_name, location_name))
        coords = db.fetchall()
        if len(coords) == 0:
            response = 'There are no saved coordinates for {}/{}'.format(world_name, location_name)
            return response
        else:
            all_coords = []
            for item in coords:
                all_coords.append(item)
            return all_coords
    except Exception as e:
        print(e)


def search_world(world_name):
    ''' SEARCHES ENTIRE WORLD FOR COODRDINATES '''
    try:
        db.execute("""SELECT * FROM worlds WHERE World_Name = '{}'""".format(world_name))
        coords = db.fetchall()
        if len(coords) == 0:
            response = 'There are no saved coordinates for {}.'.format(world_name)
            return response
        else:
            all_coords = []
            for item in coords:
                all_coords.append(item)
            return all_coords
    except Exception as e:
        print('failing function')


def select_coordinate(action):
    ''' INPUT TO SELECT A COORDINATE TO USE '''
    selection = ''
    while not selection:
        try:
            selection = int(input('Which entry would you like to {}?: '.format(action)))
        except ValueError:
            print('Selection must be a number!')
        except Exception as e:
            print(e)
    return selection


def update_coord_values():
    ''' INPUT TO SELECT A COORDINATE TO USE '''
    selection = []
    while not selection or len(selection) < 3:
        try:
            x = int(input('New X: '))
            y = int(input('New Y: '))
            z = int(input('New Z: '))
            selection.append(x)
            selection.append(y)
            selection.append(z)
        except ValueError:
            print('Selection must be a number!')
        except Exception as e:
            print(e)
    return selection

def del_coords(world_name, location_name):
    ''' DELETES A COORDINATE FROM DATABASE '''
    all_coords = search_coords(world_name, location_name)
    n = 1
    for item in all_coords:
        coordinates = (world_name + '/' + location_name + ': x:' + str(item[2]).strip('(,)')
                       + ', y:' + str(item[3]).strip('(,)') + ', z:' + str(item[4]).strip(
                           '(,)'))
        print(str(n) + ')', coordinates)
        n += 1
    selection = int(select_coordinate('delete')) - 1
    coords = all_coords[selection]
    db.execute('''DELETE FROM worlds WHERE World_Name = '{}' AND Location_Name = '{}' AND X = '{}' 
                  AND Y = '{}' AND Z = '{}' '''.format(coords[0], coords[1], coords[2], coords[3],
                                                 coords[4]))
    conn.commit()
    deleted = (coords[0] + '/' + coords[1] + ': x:' + str(coords[2]).strip('(,)')
                       + ', y:' + str(coords[3]).strip('(,)') + ', z:' + str(coords[4]).strip(
                           '(,)') + ' has been deleted.')
    return deleted

def update_coords(world_name, location_name):
    ''' UPDATES A COORDINATE '''
    all_coords = search_coords(world_name, location_name)
    n = 1
    for item in all_coords:
        coordinates = (world_name + '/' + location_name + ': x:' + str(item[2]).strip('(,)')
                       + ', y:' + str(item[3]).strip('(,)') + ', z:' + str(item[4]).strip(
                    '(,)'))
        print(str(n) + ')', coordinates)
        n += 1
    selection = int(select_coordinate('update')) - 1
    coords = all_coords[selection]
    original = (coords[0] + '/' + coords[1] + ': x:' + str(coords[2]).strip('(,)')
                       + ', y:' + str(coords[3]).strip('(,)') + ', z:' + str(coords[4]).strip(
                           '(,)'))
    new_coords = update_coord_values()
    print(new_coords)
    new_x = new_coords[0]
    new_y = new_coords[1]
    new_z = new_coords[2]
    db.execute("""UPDATE worlds SET X = '{}' WHERE World_Name = '{}' AND Location_Name = '{}' 
                  AND X = '{}' AND Y = '{}' AND Z = '{}'""".format(new_x, coords[0], coords[1],
                                                                   coords[2], coords[3], coords[4]))
    db.execute("""UPDATE worlds SET Y = '{}' WHERE World_Name = '{}' AND Location_Name = '{}' 
                  AND X = '{}' AND Y = '{}' AND Z = '{}'""".format(new_y, coords[0], coords[1],
                                                                   new_x, coords[3], coords[4]))
    db.execute("""UPDATE worlds SET Z = '{}' WHERE World_Name = '{}' AND Location_Name = '{}' 
                  AND X = '{}' AND Y = '{}' AND Z = '{}'""".format(new_z, coords[0], coords[1],
                                                                   new_x, new_y, coords[4]))
    conn.commit()
    updated = coords[0] + '/' + coords[1] + ': x:' + str(new_x) + ', y:' + str(new_y) + \
              ', z:' + str(new_z)
    response = original + ' has been updated to ' + updated
    return response


def help():
    print('HALP PLS')


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'help':
            help()
        elif sys.argv[1] == 'nether':
            print(calculate_nether(sys.argv[2], sys.argv[3]))
        elif sys.argv[1] == 'search':
            if len(sys.argv) == 4:
                searched = search_coords(sys.argv[2], sys.argv[3])
                for item in searched:
                    print(item[0] + '/' + item[1] + ': x:' + str(item[2]).strip(
                        '(,)') + ', y:' + str(item[3]).strip('(,)') + ', z:' + str(item[4]).strip(
                                '(,)'))
            else:
                searched = search_world(sys.argv[2])
                for item in searched:
                    print(item[0] + '/' + item[1] + ': x:' + str(item[2]).strip(
                        '(,)') + ', y:' + str(item[3]).strip('(,)') + ', z:' + str(item[4]).strip(
                                '(,)'))
        elif sys.argv[1] == 'delete':
            print(del_coords(sys.argv[2], sys.argv[3]))
        elif sys.argv[1] == 'add':
            print(add_coords(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]))
        elif sys.argv[1] == 'update':
            print(update_coords(sys.argv[2], sys.argv[3]))

    except IndexError:
        print('Not enough values or item does not exist.')


