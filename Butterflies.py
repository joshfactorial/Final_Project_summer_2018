import numpy as np
import math
import pandas as pd
from pandas import DataFrame
import time
from multiprocessing import Pool


class Field(DataFrame):
    """
    Create a field with sections denote C for crop, F for food, or S for shelter

    >>> f = Field([[1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1]])
    >>> print(f)
       0  1  2  3
    0  =  o  o  =
    1  =  o  o  =
    2  =  o  o  =
    3  =  o  o  =
    4  =  o  o  =
    >>> f2 = Field([[1, 1, 1, 2], [1, 1, 1, 2], [1, 1, 1, 2], [1, 1, 1, 4]])
    Traceback (most recent call last):
      File "C:/Users/Joshua/PycharmProjects/Final_Project/Butterflies.py", line 117, in <module>
        f = Field([[1, 1, 1, 2], [1, 1, 1, 2], [1, 1, 1, 2], [1, 1, 1, 4]])
      File "C:/Users/Joshua/PycharmProjects/Final_Project/Butterflies.py", line 30, in __init__
        raise ValueError("values must be either 1 (crop), 2 (food), or 3 (shelter)")
    ValueError: values must be either 1 (crop), 2 (food), or 3 (shelter)
    """

    def __init__(self, *args, **kwargs):
        DataFrame.__init__(self, *args, **kwargs)
        for column in self:
            for row in self[column]:
                if row not in (1, 2, 3):
                    raise ValueError("values must be either 1 (crop), 2 (food), or 3 (shelter)")
        try:
            for column in self:
                self[column] = self[column].replace(1, '=')
                self[column] = self[column].replace(2, 'o')
                self[column] = self[column].replace(3, '*')

        except ValueError:
            print("values must be either 1 (crop), 2 (food), or 3 (shelter)")

    def get_food_table(self):
        # found this trick on stack overflow
        # https://stackoverflow.com/questions/28979794/python-pandas-getting-the-locations-of-a-value-in-dataframe
        locs_food = self[self == "o"].stack().index.tolist()
        food_table = {'food_x': [], 'food_y': []}
        for location in locs_food:
            food_table['food_x'].append(location[1])
            food_table['food_y'].append(location[0])
        return pd.DataFrame(food_table)

    def get_shelter_table(self):
        # found this trick on stack overflow
        # https://stackoverflow.com/questions/28979794/python-pandas-getting-the-locations-of-a-value-in-dataframe
        locs_shelter = self[self == "*"].stack().index.tolist()
        shelter_table = {'shelter_x': [], 'shelter_y': []}
        for location in locs_shelter:
            shelter_table['shelter_x'].append(location[1])
            shelter_table['shelter_y'].append(location[0])
        return pd.DataFrame(shelter_table)

    @classmethod
    def random_field(cls, length, width, percent_crops, percent_food, percent_shelter):
        if percent_crops + percent_food + percent_shelter != 100:
            raise ValueError("The percentages do not add up to 100")
        area = length * width
        # find the number of squares for each type of cell
        number_crop_cells = math.ceil(percent_crops / 100 * area)
        number_food_cells = math.ceil(percent_food / 100 * area)
        number_shelter_cells = math.floor(percent_shelter / 100 * area)
        # if the calculations produced more or less of the squares needed, this should clean it up.
        # there shouldn't be more than three cells difference because of how I rounded it, so this shouldn't
        # affect the final result much
        distro = area - (number_crop_cells + number_food_cells + number_shelter_cells)
        # I'll prioritize adding shelter cells if they elected to have them, or else I'll add food cells
        # I feel like most farmers would prioritize wind breaks over feeding butterflies
        while distro > 0:
            if number_shelter_cells > 0:
                number_shelter_cells += 1
            else:
                number_food_cells += 1
            distro = area - (number_crop_cells + number_food_cells + number_shelter_cells)
        # If there are any food cells, remove those first, then shelter cells
        while distro < 0:
            if number_food_cells > 0:
                number_food_cells -= 1
            else:
                number_shelter_cells -= 1
            distro = area - (number_crop_cells + number_food_cells + number_shelter_cells)
        try:
            distro == 0
        except ValueError:
            print('something went wrong in the cell calculations')
        random_f = list(np.full((length, width), 1, dtype=int))
        while number_shelter_cells + number_food_cells > 0:
            if number_shelter_cells > 0:
                temp_length = np.random.randint(0, length)
                temp_width = np.random.randint(0, width)
                if random_f[temp_width][temp_length] == 1:
                    random_f[temp_width][temp_length] = 3
                    number_shelter_cells -= 1
            if number_food_cells > 0:
                temp_length = np.random.randint(0, length)
                temp_width = np.random.randint(0, width)
                if random_f[temp_width][temp_length] == 1:
                    random_f[temp_width][temp_length] = 2
                    number_food_cells -= 1
        return cls(random_f)


class Butterfly:
    """
    This class creates the butterfly object. It's main parameters are food level, status, and starting position
    Food level and starting position are random, though starting position is  based on the size of the Field
    and it always enters on an edge

    """

    def __init__(self, area):
        self.food_level = float(np.random.randint(0, 101))
        self.status = "alive"
        self.length = area.shape[0]
        self.width = area.shape[1]
        self.area = area
        self.sheltered = False
        variable = np.random.choice([0, 1, self.length - 1, self.width - 1])
        if variable == 1:
            self.position = [0, np.random.randint(0, self.length)]
        elif variable == 0:
            self.position = [np.random.randint(0, self.width), 0]
        elif variable == self.length - 1:
            self.position = [np.random.randint(0, self.width), variable]
        else:
            self.position = [variable, np.random.randint(0, self.length)]

    def get_area(self):
        return self.area

    def get_status(self):
        return self.status

    def get_food_level(self):
        return self.food_level

    def get_position(self):
        return self.position

    def __str__(self):
        return 'Monarch butterfly with {}% food at {}'.format(self.food_level, self.position)

    def __repr__(self):
        return 'Monarch butterfly with {}% food at {}'.format(self.food_level, self.position)

    def check_for_death(self):
        roll_die = np.random.random_sample()
        if self.food_level > 50.0:
            # if it's belly is full, move with a preference toward North
            if roll_die < 0.000001:
                self.status = 'dead'
        elif 25.0 < self.food_level <= 50.0:
            if roll_die <= 0.00005:
                self.status = 'dead'
        elif 0 < self.food_level <= 25.0:
            if roll_die < 0.0001:
                self.status = 'dead'
        else:
            self.status = 'dead'
        return self

    def random_move(self):
        coord = np.random.choice((0, 1))
        direction = np.random.choice((-1, 1))
        if coord == 0:
            if self.width > self.position[coord] + direction >= 0:
                self.position[coord] = self.position[coord] + direction
            else:
                pass
        else:
            if self.length > self.position[coord] + direction >= 0:
                self.position[coord] = self.position[coord] + direction
            else:
                pass
        return self

    def move(self):
        while self.status == 'alive':
            while self.sheltered and self.status == 'alive':
                roll_die = np.random.random_sample()
                self.check_for_death()
                print(self.position)
                if self.food_level < 25:
                    seek_resource(self, 'food')
                elif roll_die < 0.5:
                    print('move randomly')
                    self.random_move()
                else:
                    print('stay sheltered')
                    pass
                if self.area[self.position[0]][self.position[1]] != '*':
                    print('moved out of shelter')
                    self.sheltered = False
                self.food_level -= 0.0112
            if self.food_level >= 50.0:
                # if it's belly is full, move with a preference toward North
                roll_die = np.random.random_sample()
                if roll_die <= 0.85:
                    # Northly
                    print('moving north')
                    if self.position[1] > 0:
                        self.position[1] -= 1
                    elif self.position[1] == 0:
                        second_die = np.random.random_sample()
                        if second_die > 0.05:
                            self.status = "exit"
                            self.check_for_death()
                        else:
                            self.check_for_death()
                            pass
                    else:
                        raise ValueError("Something's wrong with the northly moving coordinates.")
                elif 0.85 < roll_die <= 0.855:
                    # move randomly
                    print('Moving randomly')
                    self.random_move()
                    self.check_for_death()
                elif 0.855 < roll_die <= 0.856:
                    # look for shelter
                    print('seeking shelter')
                    seek_resource(self, 'shelter')
                elif roll_die > 0.856:
                    # stay
                    print("not moving")
                    self.check_for_death()
                    pass
            elif 25.0 <= self.food_level < 50.0:
                roll_die = np.random.random_sample()
                if 0 > roll_die >= 0.001:
                    # slight chance of seeking shelter
                    print('seeking shelter')
                    seek_resource(self, 'shelter')
                else:
                    # usually look for food
                    print('looking for food')
                    seek_resource(self, 'food')
            else:
                roll_die = np.random.random_sample()
                # slight chance it looks for shelter
                if roll_die > 0.0001:
                    print("seeking shelter")
                    seek_resource(self, 'shelter')
                # otherwise look for foot
                else:
                    print("looking for food")
                    seek_resource(self, 'food')
            if self.area[self.position[0]][self.position[1]] == "*":
                # if there are trees in this sector it may look for shelter
                roll_die = np.random.random_sample()
                if roll_die >= .5:
                    self.sheltered = True
                    print('found shelter')
            self.food_level -= 0.0225


def seek_resource(monarch: Butterfly, resource) -> Butterfly:
    location = monarch.get_position()
    area = monarch.get_area()
    if resource == 'shelter':
        symbol = '*'
        resource_table = area.get_shelter_table()
        options = resource_table[resource_table['shelter_y'] < location[1]].index.tolist()
        if options:
            found_scent = np.random.choice(options)
            print(found_scent)
        else:
            monarch.food_level -= 0.0225
            return None
        chosen_resource = resource_table['shelter_x'][found_scent], resource_table['shelter_y'][found_scent]
    elif resource == 'food':
        symbol = 'o'
        resource_table = area.get_food_table()
        options = resource_table[resource_table['food_y'] < location[1]].index.tolist()
        if options:
            found_scent = np.random.choice(options)
            print(found_scent)
        else:
            monarch.food_level -= 0.225
            return None
        chosen_resource = resource_table['food_x'][found_scent], resource_table['food_y'][found_scent]
    else:
        raise ValueError('incorrect resource passed to seek_resource function')
    while (location[0] != chosen_resource[0] or location[1] != chosen_resource[1]) and monarch.status == 'alive':
        die_roll = np.random.random_sample()
        print("Moving toward {}".format(resource))
        if die_roll >= 0.05:
            if location[0] > chosen_resource[0]:
                location[0] -= 1
            elif location[0] < chosen_resource[0]:
                location[0] += 1
            elif location[1] > chosen_resource[1]:
                location[1] -= 1
            elif location[1] < chosen_resource[1]:
                location[1] += 1
            else:
                monarch.random_move()
            print(location)
            monarch.position = location
        elif .04 < die_roll < 0.05:
            print("Hanging out intead of looking for {}".format(resource))
            pass
        else:
            print("moving randomly")
            monarch.random_move()
        monarch.food_level -= 0.0225
        if monarch.food_level < 25:
            monarch.check_for_death()
            if resource == 'shelter':
                seek_resource(monarch, 'food')
    if monarch.status == 'dead':
        print("Butterfly died looking for {}".format(resource))
    else:
        print("Butterfly found {}".format(resource))
    if resource == 'food':
        monarch.food_level = 100
    return None


def create_standard_test(iterations: int) -> Field:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
    # create the top and bottom rows of the field
    base_field_base_rows = [2] * 100
    base_field_base_rows[0] = 3
    base_field_base_rows[99] = 3
    # create the standard middle row
    base_field_middle_rows = [1] * 100
    base_field_middle_rows[0] = 3
    base_field_middle_rows[99] = 3
    # Build up a single standard field
    standard_field = [base_field_base_rows]
    for i in range(0, 98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    test_site = []
    for i in range(0, iterations + 1):
        test_site += standard_field
    return Field(test_site)


def create_food_heavy_test(iterations: int) -> Field:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
    # create the top and bottom rows of the field
    base_field_base_rows = [2] * 100
    # create the standard middle row
    base_field_middle_rows = [1] * 100
    base_field_middle_rows[0] = 2
    base_field_middle_rows[99] = 2
    # Build up a single standard field
    standard_field = [base_field_base_rows]
    for i in range(0, 98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    test_site = []
    for i in range(0, iterations + 1):
        test_site += standard_field
    return Field(test_site)


def create_shelter_heavy_test(iterations: int) -> Field:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
    # create the top and bottom rows of the field
    base_field_base_rows = [3] * 100
    base_field_base_rows[0] = 3
    base_field_base_rows[99] = 3
    # create the standard middle row
    base_field_middle_rows = [1] * 100
    base_field_middle_rows[0] = 2
    base_field_middle_rows[99] = 2
    # Build up a single standard field
    standard_field = [base_field_base_rows]
    for i in range(0, 98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    test_site = []
    for i in range(0, iterations + 1):
        test_site += standard_field
    return Field(test_site)


def create_middle_food_windbreak_test(iterations: int) -> Field:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
    # create the top and bottom rows of the field
    base_field_base_rows = [3] * 100
    # create the standard middle row
    base_field_middle_rows = [1] * 100
    base_field_middle_rows[0] = 3
    base_field_middle_rows[99] = 3
    base_field_middle_rows[49] = 2
    # Build up a single standard field
    standard_field = [base_field_base_rows]
    for i in range(0, 98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    test_site = []
    for i in range(0, iterations + 1):
        test_site += standard_field
    return Field(test_site)


def create_food_middle_windbreak_test(iterations: int) -> Field:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
    # create the top and bottom rows of the field
    base_field_base_rows = [2] * 100
    # create the standard middle row
    base_field_middle_rows = [1] * 100
    base_field_middle_rows[0] = 2
    base_field_middle_rows[99] = 2
    base_field_middle_rows[49] = 3
    # Build up a single standard field
    standard_field = [base_field_base_rows]
    for i in range(0, 98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    test_site = []
    for i in range(0, iterations + 1):
        test_site += standard_field
    return Field(test_site)


def move_butterfly(monarch: Butterfly):
    monarch.move()


if __name__ == '__main__':
    pass
    # start_time = time.time()
    # test2 = create_standard_test(3334)
    # print("--- %s seconds ---" % (time.time() - start_time))
    # results = []
    #

    #     with Pool(processes=20) as p:
    #         p.map(move_butterfly, swarm)
    #     for butterfly in swarm:
    #         print(butterfly.get_position())
    #         print(butterfly.get_status())
    #         results.append(butterfly.get_status())
    # print("{} butterflies processed".format(len(results)))
    # print("Dead percentage = {:.2f}%".format(100 * results.count('dead')/len(results)))
    #
    # print("--- %s seconds ---" % (time.time() - start_time))



