from livewires import games, color
from random import randint
import threading, string, random, time

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 50
VANISH_TIME_SEC = 5
PLANES_TOTAL_MIN = 1
PLANES_TOTAL_MAX = 4

games.init(screen_width = SCREEN_WIDTH, screen_height = SCREEN_HEIGHT, fps = FPS)

class AirPlane(games.Sprite):
    image = games.load_image("rect.png")
    __text__ = None
    
    def __init__(self, x, y, text):
        super(AirPlane, self).__init__(image = AirPlane.image, x = x, y = y, dy = 0,
                                       dx = 0)
        self.__text__ = text

    def vanish(self):
        self.__text__.destroy()
        self.destroy()    
        
class Controller():

    __vanish_interval_sec__ = 0
    __airplanes_num__ = 0
    __last_modified__ = time.time()
    __visible__ = True
    __airplanes__ = []
    __airline_companies__ = []
    FONT_SIZE = 30
    PLANE_NAME_LETTERS_NUM = 3
    PLANE_NAME_MIN_NUMBERS_NUM = 3
    PLANE_NAME_MAX_NUMBERS_NUM = 4
    MIN_NUMBER = 0
    MAX_NUMBER = 9
    WIDTH_CORRECTION = 30
    LENGTH_CORRECTION = 100
    TEXT_Y_CORRECTION = 8
    TEXT_X_CORRECTION = 40
    AIRLINES_CODES_FILENAME = "companies_codes.txt"

    def __init__(self, airplanes_num_min, airplanes_num_max, vanish_interval_sec):
        self.__airplanes_num_min__ = airplanes_num_min
        self.__airplanes_num_max__ = airplanes_num_max
        self.__vanish_interval_sec__ = vanish_interval_sec
        self.__load_airline_codes__()
        self.__create_airplanes__()

    def __load_airline_codes__(self):
        with open(self.AIRLINES_CODES_FILENAME) as file:
            content = file.readlines()
        new_tuple = []
        for item in content:
            if item != '\r' and item != '\n' and item != '\t':
                new_tuple.append(item)
        self.__airline_companies__ = new_tuple

    def start_practice(self):
        
        if self.__need_update__() == True:
            self.__last_modified__ = time.time()
            if self.__visible__ == True:
                self.__destroy_airplanes__()
                self.__visible__ = False
            else:
                self.__create_airplanes__()
                self.__visible__ = True
        threading.Timer(self.__vanish_interval_sec__, self.start_practice).start()
            
    def __need_update__(self):
        elapsed = int(time.time() - self.__last_modified__)
        if elapsed >= self.__vanish_interval_sec__:
            return True
        return False
    
    def __destroy_airplanes__(self):
        for airplane in self.__airplanes__:
            airplane.vanish()
        self.__airplanes__ = []

    def __generate_random_X_Y_coordinates__(self):
        random_x = randint(self.MIN_NUMBER + self.LENGTH_CORRECTION, SCREEN_WIDTH - self.LENGTH_CORRECTION)
        random_y = randint(self.MIN_NUMBER + self.WIDTH_CORRECTION, SCREEN_HEIGHT - self.WIDTH_CORRECTION)
        return random_x, random_y
        
    def __generate_plane_name__(self):
        letters = ""
        numbers = ""
        airline_companies_num = len(self.__airline_companies__)
        airline_num = randint(self.MIN_NUMBER, airline_companies_num)
        letters = self.__airline_companies__[airline_num]
        letters = letters.replace("\n","")
        print("Letters: ", letters)
        numbers_num = randint(self.PLANE_NAME_MIN_NUMBERS_NUM, self.PLANE_NAME_MAX_NUMBERS_NUM)
        for num in range(numbers_num):
            numbers += str(randint(self.MIN_NUMBER, self.MAX_NUMBER))
        print("Numbers: ", numbers)
        return letters + numbers

    def __create_airplanes__(self):
        planes_num = randint(self.__airplanes_num_min__, self.__airplanes_num_max__)
        for number in range(planes_num):
            random_x, random_y = self.__generate_random_X_Y_coordinates__()
            # add airplane number
            plane_name = self.__generate_plane_name__()
            print("Plane name: ", plane_name)
            airplane_number = games.Text(value = plane_name, size = self.FONT_SIZE, color = color.black,
                                            top = random_y - self.TEXT_Y_CORRECTION, right = random_x + self.TEXT_X_CORRECTION)
            # create the airplane(rectangular)
            air_plane_sprite = AirPlane(random_x, random_y, airplane_number)
            games.screen.add(air_plane_sprite)
            games.screen.add(airplane_number)
            self.__airplanes__.append(air_plane_sprite)

def main():
    
    wall_image = games.load_image("belarus_map.png", transparent = False)
    games.screen.background = wall_image

    # create the desired number of airplanes by passing
    # the number as constructor argument
    
    controller = Controller(PLANES_TOTAL_MIN, PLANES_TOTAL_MAX, VANISH_TIME_SEC)
    controller.start_practice()

    games.screen.mainloop()

main()
