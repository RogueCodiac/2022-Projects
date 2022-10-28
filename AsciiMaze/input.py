import config
from config import *
from pygame.locals import *
from pygame.event import Event, wait
from pygame.display import set_caption
from typing import Union


# Current function index.
current_function_index: int = 0

# Currently selected character
selected_char: str = possible_chars[0]

# Current mouse action id; 0 do nothing, 1 draw, -1 erase
mouse_action_id: int = 0


def __get_keyboard_input(event: Event) -> int:
    """
    Either returns the index of the character to be drawn.
    Returns -1 if no input is given, or a change in the algorithm selection is made.
    :return:
    """

    if event.type == KEYDOWN:
        if event.key is K_1:
            return bool(config.CHOSEN_START) + (bool(config.CHOSEN_END) if config.CHOSEN_START else 0)

        elif event.key is K_2:
            return 2

        elif event.key is K_3:
            return 3

        elif event.key is K_q:
            return 4

        elif event.key is K_e:
            return 5

        elif event.key is K_r:
            return -101

        elif event.key is K_t:
            return -102

        elif event.key is K_SPACE:
            return -103

        elif event.key is K_y:
            return -104

    return -1


def __get_mouse_input(event: Event) -> MOUSE_T:
    """
    Returns an integer that is either -1, 0, or 1 along with the mouse position.
    -1 indicates that the char at the current position is to be deleted.
    0 indicates that no drawing action to be taken.
    1 indicates that the currently selected char is to be drawn at mouse position.
    :return:
    """
    global mouse_action_id

    coords: tuple[int, int] = (-1, -1)

    if event.type == MOUSEBUTTONUP:  # When we lift our hold from left or right click, hover mode is restored
        mouse_action_id = 0

    elif event.type == MOUSEBUTTONDOWN:
        coords = event.pos  # Get the coordinates of the cursor

        if event.button == 1:  # Left click
            mouse_action_id = 1

        elif event.button == 3:  # Right click
            mouse_action_id = -1

    elif event.type == MOUSEMOTION:  # Get cursor motion when left click or right click are pressed
        if mouse_action_id:
            coords = event.pos  # Get the coordinates of the cursor

            return mouse_action_id, coords

    return mouse_action_id, coords


def __is_quit(event: Event) -> bool:
    """
    Returns True iff the event is of type QUIT or the escape button has been pressed.
    :param event:
    :return:
    """

    return event.type == QUIT and event or event.type == KEYDOWN and event.key == K_ESCAPE


def __process_keyboard_input(code: int) -> tuple[str, int]:
    """
    Processes the input from the keyboard.
    0 -> 3: Possible character choices
    4, 5:   Changes the algorithm
    :param code:
    :return:
    """

    global selected_char, current_function_index

    if code < 0:
        if code == -101:
            return CLEAR

        elif code == -102:
            return RESET

        elif code == -103:
            return START

        elif code == -104:
            return BACK_SEARCH

    elif code < 4:
        selected_char = possible_chars[code]

    elif code == 4:
        current_function_index = config.algo_count - 1 if not current_function_index else current_function_index - 1

    elif code == 5:
        current_function_index = (current_function_index + 1) % config.algo_count

    set_caption(f"{config.algo_names[current_function_index]:}  |  {selected_char:}".center(25))

    return selected_char, current_function_index


def __process_mouse_input(code: MOUSE_T) -> Union[tuple[str, COORDS], INPUT_T]:
    """
    Processes the input from the mouse.
    :param code:
    :return:
    """

    if not code[0]:
        return IDLE

    elif code[0] == -1:
        return possible_chars[-1], code[1]

    return selected_char, code[1]


def __get_input() -> INPUT_T:
    """
    Returns the input of keyboard and mouse (in this order) as a tuple.
    :return:
    """

    # Wait for an event, given timeout value
    event: Event = wait(IN_TIMEOUT)

    if not event:
        return IDLE

    if __is_quit(event):
        return QUIT_INPUT

    return __get_keyboard_input(event), __get_mouse_input(event)


def __terminate() -> None:
    """
    Terminates the program.
    :return:
    """

    quit(0)
    exit(0)


def process_input() -> tuple[tuple[str, int], Union[tuple[str, tuple[int, int]], tuple[int, tuple[int, tuple[int, int]]]]]:
    """
    Takes the input from mouse and keyboard, and processes them.
    Returns selected char & function_index in one tuple and the result of mouse processing.
    :return:
    """

    input_codes: INPUT_T = __get_input()

    if input_codes == QUIT_INPUT:
        __terminate()

    return __process_keyboard_input(input_codes[0]), __process_mouse_input(input_codes[1])
