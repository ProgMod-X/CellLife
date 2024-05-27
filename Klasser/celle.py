import random
from Klasser.busk import *

class Celle:
    pos_x: int = None
    pos_y: int = None
    energi: int = None
    vision = None

    mål_x: int = None
    mål_y: int = None
    har_mål: bool = None

    vekt_min: float = None
    vekt_max: float = None

    def __init__(self, x, y, energi, sight_range, world_x, world_y) -> None:
        self.pos_x = x
        self.pos_y = y
        self.energi = energi

        self.world_x = world_x
        self.world_y = world_y

        self.sight_range = sight_range
        self.color = "blue"
        
        self.har_mål = False

        self.vekt_max = 1.0
        self.vekt_min = 0.0
        self.celle_prioritet = random.randrange(self.vekt_min, self.vekt_max)
        # self.mål_vekter = {}
        # for m in self.mål:
        #     self.mål_vekter[m] = random.randrange(self.vekt_min, self.vekt_max)
    
    def tegn(self, canvas, tile_size, rect_size):
        # Draw target pos
        canvas.fill_style = "tomato"
        canvas.fill_rect(((self.pos_x + self.mål_x - self.sight_range) % self.world_x) * tile_size, ((self.pos_y + self.mål_y - self.sight_range) % self.world_x) * tile_size, rect_size, rect_size)
        # Draw self
        canvas.fill_style = self.color
        canvas.fill_rect(self.pos_x * tile_size, self.pos_y * tile_size, rect_size, rect_size)
    
    def beveg(self):
        # Hvis cellen er på målet trenger den ikke å bevege seg.
        if self.mål_x - self.sight_range == 0 and self.mål_y - self.sight_range == 0:
            self.har_mål = False
            return [self.pos_x, self.pos_y, 0, 0]

        # Cellen kan kun bevege seg på en akse om gangen. F.eks. først x, deretter y
        # Hvordan bestemmer cellen hvilken akse den skal bevege seg på?
        # Den kan se på de fire nye mulige posisjonene og velge den som er nermest målet.
        pos_x = self.sight_range
        pos_y = self.sight_range

        x_direction = 1
        if self.mål_x < pos_x:
            x_direction = -1
        
        y_direction = 1
        if self.mål_y < pos_y:
            y_direction = -1
        
        new_x_pos = pos_x + x_direction
        new_x_distance = ((self.mål_x - new_x_pos)**2 + (self.mål_y - pos_y)**2)**0.5

        new_y_pos = pos_y + y_direction
        new_y_distance = ((self.mål_x - pos_x)**2 + (self.mål_y - new_y_pos)**2)**0.5

        # Beveg funksjonen returnerer den nye posisjonen.
        # En utvendig funksjon bestemmer om denne bevegelsen er mulig.
        if new_x_distance < new_y_distance:
            return [self.pos_x + x_direction, self.pos_y, x_direction, 0]
        else:
            return [self.pos_x, self.pos_y + y_direction, 0, y_direction]

    def update_pos(self, new_x, new_y, dir_x, dir_y):
        self.pos_x = new_x
        self.pos_y = new_y
        self.mål_x -= dir_x
        self.mål_y -= dir_y

    def spis(self, busk: Busk):
        if busk.bær > 0:
            ate_berry = busk.spis()
            print(busk.bær)
            if ate_berry:
                self.energi += 1
            print(self.energi)
            return ate_berry

    def finn_mål(self, nabolag, entities):
        if self.har_mål and (self.sight_range - self.mål_x)**2 + (self.sight_range - self.mål_y)**2 == 1:
            # Når cellen er ved målet bør den gjøre noe

            if nabolag[self.mål_x][self.mål_y] != None:
                mål_entity = entities[nabolag[self.mål_x][self.mål_y]]
                self.har_mål = self.spis(mål_entity)
            else:
                self.har_mål = False
        if self.har_mål:
            return

        # Decide what is desired target
        desired = Celle
        if random.random() < 0.5:
            desired = Busk

        # Search through vision for valid targets
        closest = 10.0**6 # might cause bugs in massive world
        closest_x = None
        closest_y = None
        x = 0
        y = 0
        found_something = False
        for col in nabolag:
            x = 0
            for tile in col:
                if tile != None and entities[tile] != self:
                    # Decide if target is closest and desired
                    dist = ((x - self.pos_x)**2 + (y - self.pos_y)**2)**0.5
                    selected = entities[tile]
                    #print(dist, closest)
                    #print(dist < closest, type(selected).__name__ == desired)
                    if dist < closest:# and type(selected) == desired:
                        if type(selected) == Busk and selected.bær > 0:
                            closest = dist
                            closest_x = x
                            closest_y = y
                            found_something = True
                        if type(selected) == Celle:
                            closest = dist
                            closest_x = x
                            closest_y = y
                            found_something = True
                x += 1
            y += 1
        if found_something:
            self.mål_x = closest_x
            self.mål_y = closest_y
        else:
            self.mål_x = random.randint(0, self.sight_range * 2)
            self.mål_y = random.randint(0, self.sight_range * 2)

        self.har_mål = True