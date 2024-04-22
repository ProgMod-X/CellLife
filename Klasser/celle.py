class Celle:
    pos_x: int = None
    pos_y: int = None
    energi: int = None
    nabolag: list = None

    def __init__(self, x, y, energi, nabolag) -> None:
        self.pos_x = x
        self.pos_y = y
        self.energi = energi
        self.nabolag = nabolag
    
    def tegn(self, canvas, tile_size, rect_size):
        canvas.fill_style = "blue"
        canvas.fill_rect(self.pos_x * tile_size, self.pos_y * tile_size, rect_size, rect_size)