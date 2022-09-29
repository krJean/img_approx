from signal import SIG_DFL
from shapes import Circle
from PIL import Image, ImageDraw, ImageChops, ImageStat
import copy
import signal
import sys
from random import randint
import cv2
import numpy as np

def generate_shapes(num_shapes:int, canvas_size:tuple[int]) -> list[Circle]:
    shape_list = [None]*num_shapes
    for i in range(num_shapes):
        shape_list[i] = Circle(max_radius=min(canvas_size)//20, max_center=canvas_size)
        shape_list[i].randomize()
    return shape_list

def get_score(img1, img2):
    diff = ImageChops.difference(img1, img2)
    stat = ImageStat.Stat(diff)
    return stat.mean

def is_better(old_score, new_score):
    r = old_score[0]-new_score[0]
    g = old_score[1]-new_score[1]
    b = old_score[2]-new_score[2]
    return (r+b+g) > 0

def draw_shapes(draw_context, shape_list):
    for s in shape_list:
        draw_context.ellipse(xy=s.get_bbox(), fill=tuple(s.color))

def wiggle_shapes(shape_list):
    for s in shape_list:
        s.wiggle()

def clear_canvas(draw_context, canvas_size):
    draw_context.rectangle([(0,0),canvas_size],fill=(0,0,0))

def main():
    # Initialize the canvases
    target = Image.open(fp='starry-night-big.jpg').convert(mode='RGB')
    canvas_size = target.size
    canvas = Image.new(mode='RGB', size=canvas_size, color=(0,0,0))
    draw = ImageDraw.Draw(canvas)

    # Create initial list of shapes
    shape_list = generate_shapes(300, canvas_size)

    # Track number of improvements
    improvement_count = 0

    # First round of randomization
    wiggle_shapes(shape_list)
    draw_shapes(draw,shape_list)

    # Keep score
    old_score = get_score(canvas, target)
    old_shapes = copy.deepcopy(shape_list)
    print("Old score: ", old_score)
    new_score = copy.copy(old_score)

    # Handle an early exit
    def signal_handler(sig, frame):
        clear_canvas(draw, canvas_size)
        draw_shapes(draw, old_shapes)
        canvas.show()
        target.show()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # Do the thing
    while improvement_count < 10000:
        while(not is_better(old_score, new_score)):
            clear_canvas(draw, canvas_size)
            new_shapes = copy.deepcopy(old_shapes)
            new_shapes[randint(0,len(new_shapes)-1)].wiggle()
            new_shapes.sort(key=lambda x: x.get_area(), reverse=True)
            draw_shapes(draw, new_shapes)
            new_score = get_score(canvas, target)
        if improvement_count % 10 == 0:
            print(str(improvement_count)+": "+str(new_score))
            cv2.imshow('approx', cv2.cvtColor(np.array(canvas).copy(), cv2.COLOR_RGB2BGR))
            cv2.waitKey(1)
        improvement_count += 1
        old_score = copy.copy(new_score)
        old_shapes = copy.deepcopy(new_shapes)

    canvas.show()
    target.show()

if __name__ == '__main__':
    main()