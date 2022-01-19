from os import environ


environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # Disables the pygame prompt.


from pygame import KEYDOWN, K_ESCAPE, QUIT, RESIZABLE, Rect, SCALED, Surface, display, event, init, \
    K_0, K_1, K_SPACE, K_TAB, K_r, image


from random import randint, sample, shuffle as rshuffle
from numpy import arange
from time import sleep
from typing import Union
from types import FunctionType


init()
_resolution: tuple[int, int] = display.Info().current_w, display.Info().current_h

_main_canvas: Surface = display.set_mode(_resolution, SCALED)

pause_icon: image = image.load("/Users/yamansirajaldeen/Documents/SortingVisualizer/icons/test.png")

Color = tuple[int, int, int]


def rand_array(begin: int, end: int, size: int, true_rand: bool) -> [int]:
    return [randint(begin, end) for _ in range(size)] if true_rand \
        else sample([int(i) for i in arange(begin, end, 0.5)], size)


def shuffle(viz: any) -> None:
    rshuffle(viz)
