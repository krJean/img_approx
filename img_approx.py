from shapes import Circle
from PIL import Image, ImageDraw

def main():
    my_shape = Circle(color=[46, 176, 100], center=[50,50], radius=10)
    canvas = Image.new(mode='RGB', size=(100,100), color=(255,255,255))
    draw = ImageDraw.Draw(canvas)
    draw.ellipse(xy=my_shape.get_bbox(), fill=tuple(my_shape.color))
    canvas.show()

if __name__ == '__main__':
    main()