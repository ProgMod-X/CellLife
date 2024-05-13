import random

class Celle:
    pos_x: int = None
    pos_y: int = None
    energi: int = None
    vision = None

    mål_x: int = None
    mål_y: int = None
    har_mål: bool = None

    mål: list = None

    mål_vekter: dict = None
    vekt_min: float = None
    vekt_max: float = None

    def __init__(self, x, y, energi, nabolag) -> None:
        self.pos_x = x
        self.pos_y = y
        self.energi = energi

        self.har_mål = False

        self.vekt_max = 1.0
        self.vekt_min = 0.0
        self.celle_prioritet = random.randrange(self.vekt_min, self.vekt_max)
        # self.mål_vekter = {}
        # for m in self.mål:
        #     self.mål_vekter[m] = random.randrange(self.vekt_min, self.vekt_max)
    
    def tegn(self, canvas, tile_size, rect_size):
        canvas.fill_style = "blue"
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
        if self.har_mål:
            # Check if the target is still there.
            local_x = self.mål_x - self.pos_x + 2 # 2 is temp for vision range
            local_y = self.mål_y - self.pos_y + 2
            if nabolag[local_x][local_y] != None:
                return 

        valid_targets = []
        for row in nabolag:
            for tile in row:
                content = entities[tile]
                if content != None and content != self:
                    valid_targets.append(content)
        
        if len(valid_targets) == 0:
            self.mål_x = random.randint(-2, 2) + self.pos_x
            self.mål_y = random.randint(-2, 2) + self.pos_y

        # Choose target
        choice = random.random()
        target = None
        if choice > self.celle_prioritet:
            for potential_target in valid_targets:
                if type(potential_target) == Celle:
                    target = potential_target
        else:
            for potential_target in valid_targets:
                if type(potential_target) != Celle and potential_target:
                    target = potential_target

        if target:
            self.mål_x = target.pos_x
            self.mål_y = target.pos_y
        else:
            self.mål_x = random.randint(-2, 2) + self.pos_x
            self.mål_y = random.randint(-2, 2) + self.pos_y
        self.har_mål = True