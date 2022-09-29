from abc import ABC
from random import randint

class Shape(ABC):
    def __init__(self, color:tuple[int]=[0,0,0]):
        self.color = color

    def get_color(self) ->tuple[int]:
        return tuple(self.color)

class Circle(Shape):
    def __init__(self, color:tuple[int]=(0,0,0),
                       center:list[int]=(0,0),
                       radius:int=0,
                       max_radius:int=10,
                       max_center:list[int]=(10,10)):
        super().__init__(color)
        self.center = center
        self.radius = radius
        self.max_center = max_center
        self.max_radius = max_radius

    def _wiggle_val(self, val, min_val, max_val, wiggle_val):
        val += randint(-wiggle_val,wiggle_val)
        val = max(val,min_val)
        val = min(val,max_val)
        return val

    def get_bbox(self) -> list[tuple[int]]:
        x0 = self.center[0] - self.radius
        x1 = self.center[0] + self.radius
        y0 = self.center[1] - self.radius
        y1 = self.center[1] + self.radius
        return [(x0,y0),(x1,y1)]

    def randomize(self):
        self.color = tuple(randint(0,255) for _ in range(3))
        self.center = tuple(randint(0,self.max_center[i]) for i in range(2))
        self.radius = randint(0,self.max_radius)

    def wiggle(self):
        rand_trait = randint(0,2)
        #color
        if rand_trait == 0:
            self.color = tuple(self._wiggle_val(self.color[i], 0, 255, 10) for i in range(3))
        #center
        elif rand_trait == 1:
            self.center = tuple(self._wiggle_val(self.center[i], 0, self.max_center[i], 40) for i in range(2))
        #radius
        elif rand_trait == 2:
            self.radius = self._wiggle_val(self.radius, 4, self.max_radius, 40)

    def get_area(self):
        return 3.14*self.radius*self.radius