from abc import ABC


class Shape(ABC):
    def __init__(self, color:list[int]=[0,0,0]):
        self.color = color

    def get_color(self) ->tuple[int]:
        return tuple(self.color)

class Circle(Shape):
    def __init__(self, color:list[int]=[0,0,0], center:list[int]=[0,0], radius:int=0):
        super().__init__(color)
        self.center = center
        self.radius = radius

    def get_bbox(self) -> list[tuple[int]]:
        x0 = self.center[0] - self.radius
        x1 = self.center[0] + self.radius
        y0 = self.center[1] - self.radius
        y1 = self.center[1] + self.radius
        return [(x0,y0),(x1,y1)]
