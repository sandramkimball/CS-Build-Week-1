from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import random
import json
import uuid


class Chamber(models.Model):
    def __init__(self, id_num, name, description, x, y):
        """Default constructor for the instance attributes"""
        self.id = id_num
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.u_to = None
        self.d_to = None
        self.x = x
        self.y = y

    def connect_chambers(self, destinationChamber, direction):
        destinationChamberID = destinationChamber.id
        try:
            destinationChamber = Chamber.objects.get(id=destinationChamberID)
        except Chamber.DoesNotExist:
            print("That chamber does not exist")
        else:
            if direction == "n":
                self.n_to = destinationChamberID
            elif direction == "s":
                self.s_to = destinationChamberID
            elif direction == "e":
                self.e_to = destinationChamberID
            elif direction == "w":
                self.w_to = destinationChamberID
            elif direction == "u":
                self.u_to = destinationChamberID
            elif direction == "d":
                self.d_to = destinationChamberID
            else:
                print("Invalid direction")
                return
            self.save()

    def convert_to_dict(self):
        """Returns a dictionary representation of this class including metadata such as the module and class names"""
        #  Populate the dictionary with object meta data
        obj_dict = {"__class__": self.__class__.__name__, "__module__": self.__module__}
        #  Populate the dictionary with object properties
        obj_dict.update(self.__dict__)
        if self.n_to is not None:
            obj_dict['n_to'] = self.n_to.id
        if self.s_to is not None:
            obj_dict['s_to'] = self.s_to.id
        if self.e_to is not None:
            obj_dict['e_to'] = self.e_to.id
        if self.w_to is not None:
            obj_dict['w_to'] = self.w_to.id
        if self.u_to is not None:
            obj_dict['u_to'] = self.u_to.id
        if self.d_to is not None:
            obj_dict['d_to'] = self.d_to.id
        return obj_dict

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentChamber=self.id) if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentChamber=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentChamber = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentChamber == 0:
            self.currentChamber = Chamber.objects.first().id
            self.save()

    def chamber(self):
        try:
            return Chamber.objects.get(id=self.currentChamber)
        except Chamber.DoesNotExist:
            self.initialize()
            return self.chamber()


class Mars(models.Model):
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

    def jsonify(self, grid_size):
        """Method to print an ASCII map to file and all of the chambers to a JSON file"""
        # Get each chamber from the grid coordinates and write the attributes to file
        map_data = open('generated_map.txt', 'w')
        json_list = []
        for y in range(0, grid_size):
            row_to_write = ''
            for x in range(0, grid_size):
                chamber = self.grid[y][x]
                if chamber is not None:
                    json_list.append(chamber.convert_to_dict())
                    row_to_write += repr(chamber)
                else:
                    row_to_write += '-----'
            map_data.write(row_to_write + '\n')
        map_data.close()
        # Save the list of dictionary-converted chambers as a .json file
        with open('../fixtures/all_chambers.json', 'w') as f:
            json.dump(json_list, f)


    # def generate_map(sender, instance, created, **kwargs):
total_chambers = 500
size_of_grid = 150
length_of_each_level = 100
number_of_levels = 5
multiplier_of_the_level = 0
chamber_listings = {
    0: ['Martian Surface', 'The ruddy rocky dusty terrain behind you. The entrance ahead of you, leading downwards.']}
chamber_levels = ['Dirt', 'Concrete', 'Metal', 'Rock', 'Crystal']
for level in chamber_levels:
    for i in range(1, length_of_each_level + 1):
        chamber_listings[i + multiplier_of_the_level] = [f'Chamber {i + multiplier_of_the_level}: {level}',
                                                        f'You are in a {level} chamber.']
    multiplier_of_the_level += length_of_each_level
chamber_listings[total_chambers + 1] = ['Martian Lair',
                                        'Deep underground, you have stumbled upon a grisly sight... (to be continued)']
mars = Mars()
mars.build_chambers(level=length_of_each_level, size_x=size_of_grid, size_y=size_of_grid, listings=chamber_listings)
mars.jsonify(size_of_grid)
    



@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
