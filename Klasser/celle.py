import random

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

    def __init__(self, x, y, energi, nabolag) -> None:
        self.pos_x = x
        self.pos_y = y
        self.energi = energi

        self.color = "blue"
        
        self.har_mål = False

        self.vekt_max = 1.0
        self.vekt_min = 0.0
        self.celle_prioritet = random.randrange(self.vekt_min, self.vekt_max)
        # self.mål_vekter = {}
        # for m in self.mål:
        #     self.mål_vekter[m] = random.randrange(self.vekt_min, self.vekt_max)
    
    def tegn(self, canvas, tile_size, rect_size):
        canvas.fill_style = self.color
        canvas.fill_rect(self.pos_x * tile_size, self.pos_y * tile_size, rect_size, rect_size)
    
    def beveg(self):
        # Hvis cellen er på målet trenger den ikke å bevege seg.
        if self.mål_x == self.pos_x and self.mål_y == self.pos_y:
            self.har_mål = False
            return [self.pos_x, self.pos_y]

        # Cellen kan kun bevege seg på en akse om gangen. F.eks. først x, deretter y
        # Hvordan bestemmer cellen hvilken akse den skal bevege seg på?
        # Den kan se på de fire nye mulige posisjonene og velge den som er nermest målet.

        x_direction = 1
        if self.mål_x < self.pos_x:
            x_direction = -1
        
        y_direction = 1
        if self.mål_y < self.pos_y:
            y_direction = -1
        
        new_x_pos = self.pos_x + x_direction
        new_x_distance = ((self.mål_x - new_x_pos)**2 + (self.mål_y - self.pos_y)**2)**0.5

        new_y_pos = self.pos_y + y_direction
        new_y_distance = ((self.mål_x - self.pos_x)**2 + (self.mål_y - new_y_pos)**2)**0.5

        # Beveg funksjonen returnerer den nye posisjonen.
        # En utvendig funksjon bestemmer om denne bevegelsen er mulig.
        if new_x_distance < new_y_distance:
            return [new_x_pos, self.pos_y]
        else:
            return [self.pos_x, new_y_pos]

    def finn_mål(self, nabolag, entities):
        print(self.har_mål, self.mål_x, self.mål_y)
        if self.har_mål:
            # Check if the target is still there.
            if nabolag[self.mål_x][self.mål_y] == None:
                self.har_mål = False
                return


        # Decide what is desired target
        desired = "celle"
        if random.random() < 0.5:
            desired = "busk"

        # Search through vision for valid targets
        closest = 10.0**6 # might cause bugs in massive world
        closest_x = None
        closest_y = None
        x = 0
        y = 0
        found_something = False
        for col in nabolag:
            for tile in col:
                if tile != None and entities[tile] != self:
                    # Decide if target is closest and desired
                    dist = ((x - self.pos_x)**2 + (y - self.pos_y)**2)**0.5
                    selected = entities[tile]
                    if dist < closest and str(type(selected)) == desired:
                        closest = dist
                        closest_x = x
                        closest_y = y
                        found_something = True
                y += 1
            x += 1

        
        if not found_something:
            self.mål_x = random.randint(0, 3)
            self.mål_y = random.randint(0, 3)

        self.mål_x = closest_x
        self.mål_y = closest_y

        self.har_mål = True