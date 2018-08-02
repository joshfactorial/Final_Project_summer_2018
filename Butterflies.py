import pandas as pd
import numpy as np
from pandas import DataFrame
import math


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
    >>> rf = Field.random_field(10, 10, 85, 10, 5)
    1    85
    2    10
    3     5
    dtype: int64
    """

    def __init__(self, *args, **kwargs):
        DataFrame.__init__(self, *args, **kwargs)
        for column in self:
            for row in self:
                if self[column][row] not in (1, 2, 3):
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
        random_f = pd.DataFrame(np.full((length, width), 1, dtype=int))
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
        # reality check
        print(random_f.stack().value_counts())
        return cls(random_f)


class Butterfly:
    """
    This class creates the butterfly object. It's main parameters are food level, status, and starting position
    Food level and starting position are random, though starting position is  based on the size of the Field
    and it always enters on an edge

    """
    def __init__(self, length, width):
        self.food_level = float(np.random.randint(0, 101))
        self.status = "alive"
        self.length = length
        self.width = width
        variable = np.random.choice([0, 1, length-1, width-1])
        if variable == 1:
            self.position = (0, np.random.randint(0, length))
        elif variable == 0:
            self.position = (np.random.randint(0, width), 0)
        elif variable == length-1:
            self.position = (np.random.randint(0, width), variable)
        else:
            self.position = (variable, np.random.randint(0, length))

    def get_status(self):
        return self.status

    def get_food_level(self):
        return str(self.food_level)

    def get_position(self):
        return list(self.position)

    def __str__(self):
        return 'Monarch butterfly with {}% food'.format(self.food_level)

    def move(self):
        if self.food_level > 50.0:
            # if it's belly is full, move with a preference toward North
            roll_die = np.random.random_sample()
            if roll_die <= 0.75:
                # Northly
                if self.position[1] - 1 > 0:
                    second_die = np.random.random_sample()
                    if second_die > 0.05:
                        self.position = (self.position[0], self.position[1] - 1)
                    else:
                        self.status = 'dead'
                else:
                    second_die = np.random.random_sample()
                    if second_die > 0.05:
                        self.status = "exit"
                    elif 0.05 >= second_die >0.01:
                        self.status = "dead"
                    else:
                        pass
            elif 0.75 < roll_die <=0.83:
                # Easterly
                second_die = np.random.random_sample()
                if second_die >= 0.01:
                    self.position = (self.position[0] + 1, self.position[1])
                else:
                    self.status = "dead"
            elif 0.83 < roll_die <= 0.91:
                # Southerly
                second_die = np.random.random_sample()
                if second_die >= 0.01:
                    self.position = (self.position[0], self.position[1] + 1)
                else:
                    self.status = "dead"
            elif 0.91 < roll_die <= 0.99:
                # Westerly
                second_die = np.random.random_sample()
                if second_die >= 0.01:
                    self.position = (self.position[0] - 1, self.position[1])
                else:
                    self.status = 'dead'
            else:
                # stay
                second_die = np.random.random_sample()
                if second_die >= 0.10:
                    pass
                else:
                    self.status = 'dead'
        elif 25.0 < self.food_level <= 50.0:
            roll_die = np.random.random_sample()
            if roll_die <= 0.05:
                self.status = 'dead'
            else:
                seek_food(self)
        else:
            roll_die = np.random.random_sample()
            if roll_die < 0.1:
                self.status = 'dead'
            else:
                seek_food(self)
        self.food_level -= 0.0225


def nearest_food(area:Field) -> pd.Dataframe:
    key = []
    for column in area:
        temp_column = []
        for row in area:
            if area[column][row] == 'o':
                temp_column.append((column, row))
            else:


def seek_food(monarch: Butterfly, area: Field) -> Butterfly:
    location = monarch.get_position()

    return location
    # TODO figure out a way to find the nearest food source and have the monarch move there with high probability


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
    for i in range(0, iterations+1):
        test_site += standard_field
    return Field(pd.DataFrame(test_site))


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
    for i in range(0, iterations+1):
        test_site += standard_field
    return Field(pd.DataFrame(test_site))


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
    for i in range(0, iterations+1):
        test_site += standard_field
    return Field(pd.DataFrame(test_site))


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
    for i in range(0, iterations+1):
        test_site += standard_field
    return Field(pd.DataFrame(test_site))


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
    for i in range(0, iterations+1):
        test_site += standard_field
    return Field(pd.DataFrame(test_site))


if __name__ == '__main__':
    b1 = Butterfly(100, 100)
    print(b1)
