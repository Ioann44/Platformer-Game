class PlaceClass:
    def __init__(self, gab):
        self.level = []
        mini_level = []
        for i in range(gab[0]):
            mini_level.append("-")
        for i in range(gab[1]):
            self.level.append(mini_level[:])

    def change_block(self, loc_mouse, block):
        x = loc_mouse[0] // 30
        y = loc_mouse[1] // 30
        self.level[y][x] = block

    def add_block(self, loc_mouse):
        self.change_block(loc_mouse, "o")

    def del_block(self, loc_mouse):
        self.change_block(loc_mouse, "-")

    def change_spawn(self, loc_mouse):
        for i in self.level:
            if "x" in i:
                i[i.index("x")] = "-"
                break
        self.change_block(loc_mouse, "x")

    def view(self):
        msg = ""
        for i in self.level:
            for j in i:
                msg += j
            msg += "\n"
        print(msg)
