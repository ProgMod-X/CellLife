import random
from Klasser.busk import *
from math import floor

class Celle:
    pos_x: int = None
    pos_y: int = None
    energi: int = None

    mål_x: int = None
    mål_y: int = None
    har_mål: bool = None

    gen_mål_ønske: float = None # Float frå 0 til 1, der om den r 1 vil cella helst til busk, mens om 0 vil cella helst til celle.
    gen_syn_og_energi_effektivitet: float = None #Float frå 0 til 1. 1 er godt syn, 0 er meir energi frå busk.
    gen_energi_overføring: float = None #Kor stor del av energien som vli bli overført til ungane. Ved 1 overførast alt, 0 ingenting og 0,5 halvparten.

    def __init__(self, x, y, energi, world_x, world_y, gen_mål_ønske, gen_syn_og_energi_effektivitet, gen_energi_overføring, skap_celle) -> None:
        self.pos_x = x
        self.pos_y = y
        self.energi = energi

        self.skap_celle = skap_celle

        self.world_x = world_x
        self.world_y = world_y

        self.color = "blue"
        
        self.har_mål = False

        self.gen_mål_ønske = gen_mål_ønske
        self.gen_syn_og_energi_effektivitet = gen_syn_og_energi_effektivitet
        self.gen_energi_overføring = gen_energi_overføring

        self.sight_range = int(3*gen_syn_og_energi_effektivitet + 1)
        self.energi_frå_busk = int(-5*gen_syn_og_energi_effektivitet + 10)
        # self.mål_vekter = {}
        # for m in self.mål:
        #     self.mål_vekter[m] = random.randrange(self.vekt_min, self.vekt_max)
    
    def tegn(self, canvas, tile_size, rect_size):
        # Draw target pos
        #canvas.fill_style = "tomato"
        #canvas.fill_rect(((self.pos_x + self.mål_x - self.sight_range) % self.world_x) * tile_size, ((self.pos_y + self.mål_y - self.sight_range) % self.world_x) * tile_size, rect_size, rect_size)
        # Draw self
        gen_1_color = str(floor(self.gen_energi_overføring * 255))
        gen_2_color = str(floor(self.gen_mål_ønske * 255))
        gen_3_color = str(floor(self.gen_syn_og_energi_effektivitet * 255))
        canvas.fill_style = f"rgb({gen_1_color}, {gen_2_color}, {gen_3_color})"
        canvas.fill_rect(self.pos_x * tile_size, self.pos_y * tile_size, rect_size, rect_size)
    
    def beveg(self):
        # Hvis cellen er på målet trenger den ikke å bevege seg.
        if (self.mål_x - self.sight_range)**2 + (self.mål_y - self.sight_range)**2 == 1:
            #self.har_mål = False
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
        self.energi -= 1

    def spis(self, busk: Busk):
        if busk.spis():
            print("bær", busk.bær)
            self.energi += self.energi_frå_busk
            print("energi", self.energi)
            return True

    def finn_mål(self, nabolag, entities):
        if self.har_mål and (self.sight_range - self.mål_x)**2 + (self.sight_range - self.mål_y)**2 == 1:
            # Når cellen er ved målet bør den gjøre noe
            if nabolag[self.mål_y][self.mål_x] != None:
                mål_entity = entities[nabolag[self.mål_y][self.mål_x]]
                if type(mål_entity) == Busk:
                    self.spis(mål_entity)
                else:
                    self.skap_celle(self, mål_entity)

            self.har_mål = False
        if self.har_mål:
            return

        # Decide what is desired target
        desired = Celle
        if random.random() < self.gen_mål_ønske:
            desired = Busk

        # Search through vision for valid targets
        closest_desired = 10.0**6 # might cause bugs in massive world
        closest_desired_x = None
        closest_desired_y = None
        closest_not_desired = 10.0**6 # might cause bugs in massive world
        closest_not_desired_x = None
        closest_not_desired_y = None
        x = 0
        y = 0
        found_desired = False
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
                    if dist < closest_desired and type(selected) == desired and (type(selected) == Celle or selected.bær > 0):
                        closest_desired = dist
                        closest_desired_x = x
                        closest_desired_y = y
                        found_desired = True
                    elif dist < closest_not_desired and (type(selected) == Celle or selected.bær > 0):
                        closest_not_desired = dist
                        closest_not_desired_x = x
                        closest_not_desired_y = y
                        found_something = True
                x += 1
            y += 1
        if found_desired:
            self.mål_x = closest_desired_x
            self.mål_y = closest_desired_y
        elif found_something:
            self.mål_x = closest_not_desired_x
            self.mål_y = closest_not_desired_y
        else:
            self.mål_x = random.randint(0, self.sight_range * 2)
            self.mål_y = random.randint(0, self.sight_range * 2)

        self.har_mål = True