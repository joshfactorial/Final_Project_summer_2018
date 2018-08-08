import numpy as np
import math
import pandas as pd
from pandas import DataFrame
import time


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

    @classmethod
    def random_field(cls, length, width, percent_crops, percent_food, percent_shelter):
        # creates a random field given the dimensions. Picks placement of food and shelter randomly
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
        random_f = np.full((length, width), 1, dtype=int).tolist()
        while number_shelter_cells + number_food_cells > 0:
            if number_shelter_cells > 0:
                temp_length = np.random.randint(0, length-1)
                temp_width = np.random.randint(0, width-1)
                if random_f[temp_length][temp_width] == 1:
                    random_f[temp_length][temp_width] = 3
                    number_shelter_cells -= 1
            if number_food_cells > 0:
                temp_length = np.random.randint(0, length-1)
                temp_width = np.random.randint(0, width-1)
                if random_f[temp_length][temp_width] == 1:
                    random_f[temp_length][temp_width] = 2
                    number_food_cells -= 1
        return cls(random_f)


class Butterfly:
    """
    This class creates the butterfly object. It's main parameters are food level, status, and starting position
    Food level and starting position are random, though starting position is  based on the size of the Field
    and it always enters on an edge.

    """
    def __init__(self, area):
        self.food_level = float(np.random.randint(0, 101))
        self.status = "alive"
        self.length = area.shape[0]
        self.width = area.shape[1]
        self.area = area
        self.sheltered = False
        variable = np.random.choice([0, 1, self.length - 1, self.width - 1])
        # This gives the entry point
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
        # Based on how much food it currently has, the butterfly's chances to die randomly change. If it drops below
        # a near-zero threshold it dies automatically
        roll_die = np.random.random_sample()
        if self.food_level > 50.0:
            if roll_die < 0.001:
                self.status = 'dead'
                return self
            else:
                return self
        elif 25.0 < self.food_level <= 50.0:
            if roll_die <= 0.01:
                self.status = 'dead'
                return self
            else:
                return self
        elif 0.0001 < self.food_level <= 25.0:
            if roll_die < 0.4:
                self.status = 'dead'
                return self
            else:
                return self
        elif 0 <= self.food_level <= 0.0001:
            self.status = 'dead'
            return self
        else:
            raise ValueError('Food level below zero')

    def random_move(self):
        # The Monarch moves randomly
        # One improvement I would like to make is to the food supply. I was having hugely negative food totals,
        # but later realized I was making my fields ten times too long, so the poor butterfly was trying to get
        # 500 km instead of 50. A future improvement will be to refine the food consumption to something that
        # makes more sense. More data and experimentation will also improve these numbers
        coord = np.random.choice((0, 1))
        direction = np.random.choice((-1, 1))
        if coord == 0:
            # Move east-west
            if self.width > self.position[0] + (direction * math.ceil(max(self.area.shape)/4)) >= 0:
                self.position[0] = self.position[0] + (direction * math.ceil(max(self.area.shape)/4))
                self.food_level = self.food_level * 0.3
            elif self.width > self.position[0] + (direction * math.ceil(max(self.area.shape)/10)) >= 0:
                self.position[0] = self.position[0] + (direction * math.ceil(max(self.area.shape)/10))
                self.food_level = self.food_level * 0.5
            elif self.width > self.position[0] + (direction * math.ceil(max(self.area.shape)/100)) >= 0:
                self.position[0] = self.position[0] + (direction * math.ceil(max(self.area.shape)/100))
                self.food_level = self.food_level * 0.9
            elif self.width > self.position[0] + direction >= 0:
                self.position[0] = self.position[0] + direction
                self.food_level = self.food_level * 0.99
            else:
                pass
        else:
            direction = 1
            # move north. I initially allowed it to randomly move south, but it slowed the simulation down to the point
            # where it was taking hours to complete
            if self.width > self.position[1] + (direction * math.ceil(max(self.area.shape)/4)) >= 0:
                self.position[1] = self.position[1] + (direction * math.ceil(max(self.area.shape)/4))
                self.food_level = self.food_level * 0.3
            elif self.width > self.position[1] + (direction * math.ceil(max(self.area.shape)/10)) >= 0:
                self.position[1] = self.position[1] + (direction * math.ceil(max(self.area.shape)/10))
                self.food_level = self.food_level * 0.5
            elif self.width > self.position[1] + (direction * math.ceil(max(self.area.shape)/100)) >= 0:
                self.position[1] = self.position[1] + (direction * math.ceil(max(self.area.shape)/100))
                self.food_level = self.food_level * 0.9
            elif self.width > self.position[1] + direction >= 0:
                self.position[1] = self.position[1] + direction
                self.food_level = self.food_level * 0.99
            else:
                pass
        return self

    def move(self, food, shelter):
        # This is a long bunch of loops and if statements that basically amount to: move north unless you are hungry,
        # in which case move toward food. Every once in awhile move toward shelter (rain simulation)
        while self.status == 'alive':
            while self.sheltered and self.status == 'alive':
                # if it's sheltered it may stay there or move away
                roll_die = np.random.random_sample()
                if self.food_level < 25:
                    self.sheltered = False
                elif roll_die < 0.5:
                    self.sheltered = False
                else:
                    pass
                if self.area[self.position[0]][self.position[1]] != '*':
                    self.sheltered = False
                self.food_level = self.food_level * 0.9
                # I had to add in a lot of death checks because I was having a bunch of zombie butterflies in my sim
                self.check_for_death()
                if self.status != 'alive':
                    return self
            if self.status != 'alive':
                return self
            if self.food_level >= 50.0:
                # if it's belly is full, move with a preference toward North
                roll_die = np.random.random_sample()
                if roll_die <= 0.988:
                    # Northly
                    if self.position[1] > math.ceil(max(self.area.shape)/10):
                        self.position[1] -= math.ceil(max(self.area.shape)/10)
                        self.food_level = self.food_level * 0.3
                    elif self.position[1] > math.ceil(max(self.area.shape)/100):
                        self.position[1] -= math.ceil(max(self.area.shape)/100)
                        self.food_level = self.food_level * 0.5
                    elif self.position[1] > 0:
                        self.position[1] -= 1
                        self.food_level = self.food_level * 0.99
                    elif self.position[1] <= 10:
                        second_die = np.random.random_sample()
                        if second_die > 0.01:
                            self.check_for_death()
                            if self.status == 'dead':
                                return self
                            self.status = "exit"
                            return self
                        else:
                            self.check_for_death()
                            if self.status == 'dead':
                                return self
                            self.food_level -= 2.25
                            pass
                    elif self.position[0] == 0 or self.position[0] == self.width - 1:
                        second_die = np.random.random_sample()
                        if second_die > 0.90:
                            self.check_for_death()
                            if self.status == 'dead':
                                return self
                            self.status = "exit"
                            return self
                    else:
                        raise ValueError("Something's wrong with the northly moving coordinates.")
                elif 0.988 < roll_die <= 0.998:
                    # move randomly
                    self.random_move()
                    self.check_for_death()
                    if self.status == 'dead':
                        return self
                elif 0.998 < roll_die <= 0.999:
                    # look for shelter
                    seek_resource(self, 'shelter', shelter)
                    if self.status != 'alive':
                        return self
                elif roll_die > 0.999:
                    # stay
                    self.check_for_death()
                    if self.status != 'alive':
                        return self
                    self.food_level = self.food_level * 0.9
                    pass
            elif 25.0 <= self.food_level < 50.0:
                roll_die = np.random.random_sample()
                if roll_die <= 0.001:
                    # slight chance of seeking shelter
                    seek_resource(self, 'shelter', shelter)
                    if self.status != 'alive':
                        return self
                else:
                    # usually look for food
                    seek_resource(self, 'food', food)
                    if self.status != 'alive':
                        return self
            else:
                roll_die = np.random.random_sample()
                # slight chance it looks for shelter
                if roll_die <= 0.00001:
                    seek_resource(self, 'shelter', shelter)
                    if self.status != 'alive':
                        return self
                # otherwise look for food
                else:
                    seek_resource(self, 'food', food)
                    if self.status != 'alive':
                        return self
            if self.area[self.position[0]][self.position[1]] == "*":
                # if there are trees in this sector it may look for shelter
                roll_die = np.random.random_sample()
                if roll_die >= .9:
                    self.sheltered = True
            elif self.area[self.position[0]][self.position[1]] == "o":
                # if there's food nearby, might as well eat
                self.food_level = 100
        return self


def create_food_table(field):
    # initialize food table
    # originally, I tried to make this part of the class, but could not figure out how to do that. I wanted it to
    # calculate this table only once, on creation of the Field, but I just couldn't make that work. Creating it on the
    # fly every time was too computationally expensive. If I could figure out how to initialize this table
    # when a field is created, I would do that.
    food_table = {'food_x': [], 'food_y': []}
    if 'o' in field.values:
        # found this trick on stack overflow
        # https://stackoverflow.com/questions/28979794/python-pandas-getting-the-locations-of-a-value-in-dataframe
        locs_food = field[field == "o"].stack().index.tolist()
        for location in locs_food:
            food_table['food_x'].append(location[1])
            food_table['food_y'].append(location[0])
        return pd.DataFrame(food_table)
    else:
        return pd.DataFrame(food_table)


def create_shelter_table(field):
    # initialize shelter table
    # See create_food_table for further comments
    shelter_table = {'shelter_x': [], 'shelter_y': []}
    if 'o' in field.values:
        # found this trick on stack overflow
        # https://stackoverflow.com/questions/28979794/python-pandas-getting-the-locations-of-a-value-in-dataframe
        locs_food = field[field == "o"].stack().index.tolist()
        for location in locs_food:
            shelter_table['shelter_x'].append(location[1])
            shelter_table['shelter_y'].append(location[0])
        return pd.DataFrame(shelter_table)
    else:
        return pd.DataFrame(shelter_table)


def seek_resource(monarch: Butterfly, resource, resource_index) -> Butterfly:
    # Looks for a resource. Again, had to add in death checks so they would stop seeking food if they died
    # probably should have made this function a part of the class. Future improvement
    if monarch.status != 'alive':
        return monarch
    location = monarch.get_position()
    area = monarch.get_area()
    if resource == 'shelter':
        symbol = '*'
        if not resource_index[resource_index['shelter_y'] < location[1]].empty:
            found_scent = max(resource_index[resource_index['shelter_y'] < location[1]].index.tolist())
        else:
            monarch.food_level = monarch.food_level * 0.9
            monarch.random_move()
            return monarch
        chosen_resource = [resource_index['shelter_x'][found_scent], resource_index['shelter_y'][found_scent]]
    elif resource == 'food':
        symbol = 'o'
        if not resource_index[resource_index['food_y'] < location[1]].empty:
            found_scent = max(resource_index[resource_index['food_y'] < location[1]].index.tolist())
        else:
            monarch.food_level = monarch.food_level * 0.9
            monarch.random_move()
            return monarch
        chosen_resource = [resource_index['food_x'][found_scent], resource_index['food_y'][found_scent]]
    else:
        raise ValueError('incorrect resource passed to seek_resource function')
    if area[location[0]][location[1]] == symbol:
        if resource == 'food':
            monarch.food_level = 100
        return monarch
    die_roll = np.random.random_sample()
    if die_roll >= 0.001:
        monarch.position = chosen_resource
        monarch.check_for_death()
        if monarch.status == 'dead':
            return monarch
        monarch.food_level = monarch.food_level * 0.5
        if resource == 'food':
            monarch.food_level = 100
        return monarch
    else:
        monarch.food_level = monarch.food_level * 0.5
        monarch.check_for_death()
        if monarch.status != 'alive':
            return monarch
    if monarch.food_level < 25:
        monarch.check_for_death()
        if monarch.status != 'alive':
            return monarch
    if resource == 'shelter':
        return monarch
    else:
        monarch.food_level = 100
    return monarch


def create_standard_test(iterations: int) -> Field:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
    # create the top rows of the field
    base_field_base_rows = [2] * 100
    base_field_base_rows[0] = 3
    base_field_base_rows[99] = 3
    # create the bottom rows of the field
    base_field_bottom_rows = [3] * 100
    # create the standard middle row
    base_field_middle_rows = [1] * 100
    base_field_middle_rows[0] = 3
    base_field_middle_rows[99] = 3
    # Build up a single standard field
    standard_field = [base_field_base_rows]
    for j in range(98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_bottom_rows)
    # create the standard test site
    construction = []
    for j in range(0, iterations + 1):
        construction += standard_field
    return Field(construction)


def create_food_heavy_test(iterations: int) -> Field:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
    # create the top and bottom rows of the field
    base_field_base_rows = [2] * 100
    # create the standard middle row
    base_field_middle_rows = [1] * 100
    base_field_middle_rows[0] = 2
    base_field_middle_rows[99] = 2
    base_bottom_row = [3] * 100
    # Build up a single standard field
    standard_field = [base_field_base_rows]
    for j in range(0, 98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_bottom_row)
    # create the standard test site
    construction = []
    for j in range(0, iterations + 1):
        construction += standard_field
    return Field(construction)


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
    for j in range(0, 98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    construction = []
    for j in range(0, iterations + 1):
        construction += standard_field
    return Field(construction)


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
    for j in range(0, 98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    construction = []
    for j in range(0, iterations + 1):
        construction += standard_field
    return Field(construction)


def create_middle_shelter_windbreak_test(iterations: int) -> Field:
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
    for j in range(0, 98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    construction = []
    for j in range(0, iterations + 1):
        construction += standard_field
    return Field(construction)


def create_test_food_test(iterations: int) -> Field:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
    # create the top and bottom rows of the field
    base_field_base_rows = [2] * 100
    # Build up a single standard field
    standard_field = [base_field_base_rows]
    for j in range(0, 98):
        standard_field.append(base_field_base_rows)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    construction = []
    for j in range(0, iterations + 1):
        construction += standard_field
    return Field(construction)


def create_middle_shelter_windbreak_test_2(iterations: int) -> Field:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
    # create the top and bottom rows of the field
    base_field_base_rows = [2] * 100
    # create the standard middle row
    base_field_middle_rows = [1] * 100
    base_field_middle_rows[0] = 2
    base_field_middle_rows[99] = 2
    base_field_middle_rows[49] = 3
    base_field_middle_rows_variant = [1] * 100
    base_field_middle_rows_variant[49] = 3
    # Build up a single standard field
    standard_field = [base_field_base_rows]
    for j in range(0, 24):
        standard_field.append(base_field_middle_rows_variant)
        standard_field.append(base_field_middle_rows_variant)
        standard_field.append(base_field_middle_rows)
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_middle_rows_variant)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    construction = []
    for j in range(0, iterations + 1):
        construction += standard_field
    return Field(construction)


def create_middle_shelter_windbreak_test_3(iterations: int) -> Field:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
    # create the top and bottom rows of the field
    base_field_base_rows = [1] * 100
    base_field_base_rows[0] = 2
    base_field_base_rows[99] = 2
    base_field_base_rows[49] = 3
    # create the standard middle row
    base_field_middle_rows = [1] * 100
    base_field_middle_rows[0] = 2
    base_field_middle_rows[99] = 2
    base_field_middle_rows[49] = 2
    standard_field = [base_field_base_rows]
    for j in range(98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    construction = []
    for j in range(0, iterations + 1):
        construction += standard_field
    return Field(construction)


def test_field(dictionary, number):
    # This function takes care of some repetitive code I had written earlier. It's not perfect, but it works for now.
    start_time = time.time()
    if number == 0:
        field_to_test = create_standard_test(33)
    elif number == 1:
        field_to_test = create_food_heavy_test(33)
    elif number == 2:
        field_to_test = create_middle_food_windbreak_test(33)
    elif number == 3:
        field_to_test = create_middle_shelter_windbreak_test(33)
    elif number == 4:
        field_to_test = create_shelter_heavy_test(33)
    elif number == 5:
        field_to_test = Field.random_field(3333, 100, 90, 5, 5)
    elif number == 6:
        field_to_test = Field.random_field(3333, 100, 80, 15, 5)
    elif number == 7:
        field_to_test = Field.random_field(3333, 100, 80, 5, 15)
    else:
        return dictionary
    food_indices = create_food_table(field_to_test)
    shelter_indices = create_shelter_table(field_to_test)
    results = []
    for j in range(1000):
        monarch1 = Butterfly(field_to_test)
        monarch1.move(food_indices, shelter_indices)
        results.append(monarch1.get_status())
    dictionary["test_field_{}".format(number)] = [100 * results.count('exit') / len(results)]
    print("Dead percentage = {:.2f}%".format(100 * results.count('dead') / len(results)))
    print("Exit percentage = {:.2f}%".format(100 * results.count('exit') / len(results)))
    print("--- %s seconds ---" % (time.time() - start_time))
    return dictionary


if __name__ == '__main__':
    # first analysis
    master_results = {}
    for i in range(0, 8):
        test_field(master_results, i)
    index = ['standard', 'food_heavy', 'middle_food', 'middle_shelter', 'shelter_heavy', 'balanced_random', 'food_random',
             'shelter_random']
    master_results = pd.DataFrame(master_results).T
    master_results.index = index
    print("The best-performing field was {}".format(master_results[0].idxmax()))

    # field stats
    field = create_middle_shelter_windbreak_test(33)
    food = len(field[field == 'o'].stack().index.tolist())
    shelter = len(field[field == '*'].stack().index.tolist())
    crops = len(field[field == '='].stack().index.tolist())
    total = food + shelter + crops
    print('Percent food: {:.2f}%'.format(math.ceil(100 * food/total)))
    print("Percent shelter: {:.2f}%".format(math.ceil(100 * shelter/total)))
    print("Percent crops: {:.2f}%".format(math.floor(100 * crops/total)))

    # Testing a higher crop percentage variant of the middle rows
    start_time = time.time()
    field_test = create_middle_shelter_windbreak_test_2(33)
    food_indices = create_food_table(field_test)
    shelter_indices = create_shelter_table(field_test)
    results = []
    for j in range(1000):
        monarch1 = Butterfly(field_test)
        monarch1.move(food_indices, shelter_indices)
        results.append(monarch1.get_status())
    print("Dead percentage = {:.2f}%".format(100 * results.count('dead') / len(results)))
    print("Exit percentage = {:.2f}%".format(100 * results.count('exit') / len(results)))
    print("--- %s seconds ---" % (time.time() - start_time))

    food = len(field_test[field_test == 'o'].stack().index.tolist())
    shelter = len(field_test[field_test == '*'].stack().index.tolist())
    crops = len(field_test[field_test == '='].stack().index.tolist())
    total = food + shelter + crops
    print('Percent food: {:.2f}%'.format(math.ceil(100 * food/total)))
    print("Percent shelter: {:.2f}%".format(math.ceil(100 * shelter/total)))
    print("Percent crops: {:.2f}%".format(math.floor(100 * crops/total)))

    start_time = time.time()
    field_test = create_middle_shelter_windbreak_test_3(33)
    food_indices = create_food_table(field_test)
    shelter_indices = create_shelter_table(field_test)
    results = []
    for j in range(1000):
        if j+1 % 100 == 0 and j != 0:
            print("Test {}".format(j+1))
            print("--- %s seconds ---" % (time.time() - start_time))
        monarch1 = Butterfly(field_test)
        monarch1.move(food_indices, shelter_indices)
        results.append(monarch1.get_status())
    print("Dead percentage = {:.2f}%".format(100 * results.count('dead') / len(results)))
    print("Exit percentage = {:.2f}%".format(100 * results.count('exit') / len(results)))
    print("--- %s seconds ---" % (time.time() - start_time))

    food = len(field_test[field_test == 'o'].stack().index.tolist())
    shelter = len(field_test[field_test == '*'].stack().index.tolist())
    crops = len(field_test[field_test == '='].stack().index.tolist())
    total = food + shelter + crops
    print('Percent food: {:.2f}%'.format(100 * food / total))
    print("Percent shelter: {:.2f}%".format(100 * shelter / total))
    print("Percent crops: {:.2f}%".format(100 * crops / total))

 # try to find an optimal random field
    start_time = time.time()
    score_dictionary = {}
    for i in range(1000):
        field = Field.random_field(333, 100, 95, 4, 1)
        food_indices = create_food_table(field)
        shelter_indices = create_shelter_table(field)
        results = []
        if (i + 1) % 100 == 0 and i != 0:
            print('Test #{}'.format(i + 1))
            print("--- %s seconds ---" % (time.time() - start_time))
        for j in range(200):
            monarch1 = Butterfly(field)
            monarch1.move(food_indices, shelter_indices)
            results.append(monarch1.get_status())
        score_dictionary["test_field_{}".format(i)] = [(100 * (results.count('exit') / len(results))), field]
    print("--- %s seconds ---" % (time.time() - start_time))
    df = pd.DataFrame(score_dictionary).T
    max = 0
    for row in df[0]:
        if row > max:
            max = row
    print(df[df[0] == max].values.tolist()[0][0])
    print(df[df[0] == max].values.tolist()[0][1])