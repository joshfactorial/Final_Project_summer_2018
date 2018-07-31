import pandas as pd
import numpy as np
from pandas import DataFrame
import math


class Field(DataFrame):
    """Create a field with sections denote C for crop, F for food, or S for shelter"""

    def __init__(self, *args, **kwargs):
        DataFrame.__init__(self, *args, **kwargs)
        for column in self:
            for row in self:
                if self[column][row] not in (1, 2, 3, 'C', 'F', 'S'):
                    raise ValueError("values must be either 1, 2, 3, C, F, or S")
        try:
            for column in self:
                self[column] = self[column].replace(1, 'C')
                self[column] = self[column].replace(2, 'F')
                self[column] = self[column].replace(3, 'S')

        except ValueError:
            print("values must be either 1, 2, 3, C, F, or S")

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
        # I'll prioritize adding food cells if they elected to have them, or else I'll add shelter cells
        while distro > 0:
            if number_food_cells > 0:
                number_food_cells += 1
            else:
                number_shelter_cells += 1
            distro = area - (number_crop_cells + number_food_cells + number_shelter_cells)
        # If there are any shelter cells, remove those first, then food cells
        while distro < 0:
            if number_shelter_cells > 0:
                number_shelter_cells -= 1
            else:
                number_food_cells -= 1
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
        return Field(random_f)


class Butterfly:
    def __init__(self):
        self.food_level = np.random.randint(0, 100)

    def get_food_level(self):
        return str(self.food_level)

    def __str__(self):
        return 'Monarch butterfly with {}% food'.format(self.food_level)


if __name__ == '__main__':
    f = Field.random_field(5, 5, 85, 14.9, 0.1)
    print(f)

