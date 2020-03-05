from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import random
import json


class Mars2(models.Model):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.grid = None

    def build_chambers(self, level, size_x, size_y, listings):
        # Initialize the grid
        self.width = size_x
        self.height = size_y
        self.grid = [None] * size_y
        for x in range(len(self.grid)):
            self.grid[x] = [None] * size_x

        def is_chamber_present(x_axis, y_axis):
            if self.grid[y_axis][x_axis] is None:
                return False
            else:
                return True

        x: int = 1  # int(size_x / 2)
        y: int = 1  # int(size_y / 2)
        chamber_direction = 'd'
        level_multiplier = 1
        forbidden_directions = 's'
        previous_chamber = None
        for chamber_counter in range(len(listings)):
            chamber = Chamber(chamber_counter, listings[chamber_counter][0], listings[chamber_counter][1], x, y)
            self.grid[y][x] = chamber
            if previous_chamber is not None:
                previous_chamber.connect_chambers(chamber, chamber_direction)
            invalid_direction = True
            while invalid_direction:
                chamber_direction = ['n', 's', 'e', 'w'][random.randint(0, 3)]
                test_x = 0
                test_y = 0
                if chamber_direction == 'n':
                    test_y = 1
                if chamber_direction == 's':
                    test_y = -1
                if chamber_direction == 'e':
                    test_x = 1
                if chamber_direction == 'w':
                    test_x = -1
                if 0 <= y + test_y <= size_y:
                    if 0 <= x + test_x <= size_x:
                        if not is_chamber_present(x + test_x, y + test_y):
                            if chamber_direction not in forbidden_directions:
                                invalid_direction = False
            if (chamber_counter > 0) and (chamber_counter % level) == 0:
                chamber_direction = 'd'
                level_multiplier += 1
                if level_multiplier % 4 == 0:
                    forbidden_directions = 'w'
                elif level_multiplier % 3 == 0:
                    forbidden_directions = 's'
                elif level_multiplier % 2 == 0:
                    forbidden_directions = 'w'
                else:
                    forbidden_directions = 's'
                if not is_chamber_present(x + 1, y + 1):
                    x += 1
                    y += 1
                elif not is_chamber_present(x - 1, y + 1):
                    x -= 1
                    y += 1
                elif not is_chamber_present(x + 1, y - 1):
                    x += 1
                    y -= 1
                elif not is_chamber_present(x - 1, y - 1):
                    x -= 1
                    y -= 1
                else:
                    x = size_x
                    y = size_y
            if chamber_direction == 'n':
                y += 1
            elif chamber_direction == 's':
                y -= 1
            elif chamber_direction == 'e':
                x += 1
            elif chamber_direction == 'w':
                x -= 1
            previous_chamber = chamber


    # @receiver(post_save, sender=User)
    def create_mars_map(sender, instance, created, **kwargs):
        total_chambers = 100
        grid_size = 100
        length_of_each_level = 25
        number_of_levels = 4
        multiplier_of_the_level = 0
        chamber_listings = {
            0: ['Martian Surface', 'The ruddy rocky dusty terrain behind you. The entrance ahead of you, leading downwards.']}
        chamber_levels = ['Dirt', 'Concrete', 'Metal', 'Rock']
        for level in chamber_levels:
            for i in range(1, length_of_each_level + 1):
                chamber_listings[i + multiplier_of_the_level] = [f'Chamber {i + multiplier_of_the_level}: {level}',
                                                                f'You are in a {level} chamber.']
            multiplier_of_the_level += length_of_each_level
        chamber_listings[total_chambers + 1] = ['Martian Lair',
                                                'Deep underground, you have stumbled upon a grisly sight... (to be continued)']
        m = Mars()
        m.build_chambers(level=length_of_each_level, size_x=grid_size, size_y=grid_size, listings=chamber_listings)
        json_list = []
        for i in range(0, grid_size):
            for j in range(0, grid_size):
                val = m.grid[i][j]
                if val is not None:
                    json_list.append(val.convert_to_dict())
                    print(val, end='')
                else:
                    print('-----', end='')
            print()
        json_list_encoded = json.dumps(json_list, indent=4, sort_keys=True)
        with open('./all_chambers.json', 'w') as f:
            json.dump(json_list, f)

