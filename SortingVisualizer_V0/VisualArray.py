from __future__ import annotations

from prep_visualizer import KEYDOWN, K_ESCAPE, QUIT, Rect, rand_array, \
    sleep, display, event, K_SPACE, K_TAB, Union, K_r, shuffle, Color, \
    _resolution, _main_canvas


class Bar(Rect):
    def __init__(self, value: int, rect_params: list[int], *, bar_color: Color,
                 compare_color: Color, delay: float) -> None:
        """Creates a bar object using the given parameters.
           Bar objects are used as a replacement for ints in the visualizer,
           in order to show the comparisons on screen"""

        super(Bar, self).__init__(*rect_params)

        self.val: int = value

        self.color: Color = bar_color

        self.compare_color: Color = compare_color

        self.delay: float = delay

        _main_canvas.fill(bar_color, rect=self)

    def pre_op(self, other: Bar = None) -> None:
        if other:
            _main_canvas.fill(self.compare_color, rect=self)
            _main_canvas.fill(other.compare_color, rect=other)

            display.update(self)
            display.update(other)
        else:
            _main_canvas.fill(self.compare_color, rect=self)
            display.update(self)

        sleep(self.delay)

    def post_op(self, other: Bar = None) -> None:
        if other:
            _main_canvas.fill(self.color, rect=self)
            _main_canvas.fill(other.color, rect=other)

            # display.update(self)
            # display.update(other)
        else:
            _main_canvas.fill(self.color, rect=self)
            # display.update(self)

    def freeze_select(self, other: Bar = None) -> None:
        self.pre_op(other)

    def unfreeze_select(self, other: Bar = None) -> None:
        self.post_op(other)

    def __call__(self, other: Bar = None) -> Bar:
        self.pre_op(other)
        self.post_op(other)

        return self

    def __eq__(self, other: Union[Bar, int]) -> bool:
        if isinstance(other, Bar):
            return self.val == other.val

        return self.val == other

    def __ne__(self, other: Union[Bar, int]) -> bool:
        if isinstance(other, Bar):
            return self.val != other.val

        return self.val != other

    def __lt__(self, other: Union[Bar, int]) -> bool:
        if isinstance(other, Bar):
            return self.val < other.val

        return self.val < other

    def __gt__(self, other: Union[Bar, int]) -> bool:
        if isinstance(other, Bar):
            return self.val > other.val

        return self.val > other

    def __le__(self, other: Union[Bar, int]) -> bool:
        if isinstance(other, Bar):
            return self.val <= other.val

        return self.val <= other

    def __ge__(self, other: Union[Bar, int]) -> bool:
        if isinstance(other, Bar):
            return self.val >= other.val

        return self.val >= other

    def __add__(self, other: Union[Bar, int]) -> int:
        if isinstance(other, Bar):
            return self.val + other.val

        return self.val + other

    def __radd__(self, other: int) -> int:
        return self + other

    def __sub__(self, other: Union[Bar, int]) -> int:
        if isinstance(other, Bar):
            return self.val - other.val

        return self.val - other

    def __rsub__(self, other: int) -> int:
        return other - self.val

    def __int__(self) -> int:
        return self.val

    def __str__(self) -> str:
        return super().__str__()


class VisualArray:
    """Builtins"""

    def __init__(self, values: list[int] = None, *, only_positive: bool = True, true_random: bool = False,
                 sample_size: int = None, delay: float = 0.0, select_color: Color = (0, 255, 0),
                 bar_color: Color = (255, 255, 255), compare_color: Color = (255, 0, 0), is_separated: bool = True,
                 second_select_color: Color = (255, 0, 0), background_color: Color = (0, 0, 0)) -> None:
        """Assertions"""

        if VisualArray.check_given_values(values):
            sample_size = len(values)

        else:
            VisualArray.check_given_sample_size(sample_size)

        """Color attributes"""

        self.bar_color: Color = bar_color

        self.background_color: Color = background_color

        self.compare_color: Color = compare_color

        self.second_select_color: Color = second_select_color

        self.select_color: Color = select_color

        """Other attributes"""

        self.delay: float = delay

        self.sample_size: int = sample_size

        self.only_positive: bool = only_positive

        self.true_random: bool = true_random

        self.is_separated: bool = is_separated

        self.running: bool = False

        self.width: int = _resolution[0] // sample_size

        if self.width <= 1:
            self.width, self.is_separated = 1, False

        """Container"""

        values = self.rand_values() if not values else values

        self.__bar_objects: list[Bar] = [self.__make_bar(values[i], i) for i in range(len(values))]

    def __str__(self) -> str:
        return str([int(i) for i in self.__bar_objects])

    def __repr__(self) -> str:
        return str([str(i) for i in self.__bar_objects])

    def __len__(self) -> int:
        return len(self.__bar_objects)

    def __getitem__(self, index: Union[int, slice]) -> Union[Bar, list[Bar]]:
        self.check_input()

        if not self.running:
            self.__bar_objects[index].freeze_select()

            while True:
                self.check_input()

                if self.running:
                    self.__bar_objects[index].unfreeze_select()
                    break

        if isinstance(index, slice):
            return self.__bar_objects[index]

        return self.__bar_objects[index]()

    def __setitem__(self, index: Union[int, slice], new_val: Union[list[Bar], Bar, int]) -> None:
        if isinstance(index, slice):
            index = slice(index.start if index.start is not None else 0,
                          index.stop if index.stop is not None else len(self),
                          index.step if index.step is not None else 1)

            j: int = index.start

            for i in range(index.stop - index.start):
                self[j] = new_val[i]
                j += 1
            return

        self.check_input()

        if not self.running:
            self[index].freeze_select(new_val if isinstance(new_val, Bar) else None)

            while True:
                self.check_input()

                if self.running:
                    self[index].unfreeze_select(new_val if isinstance(new_val, Bar) else None)
                    break

        if self.__erase_bar(index):
            self.__bar_objects[index] = self.__make_bar(new_val, index)

        self.update_ind(index)

    def __make_bar(self, value: Union[int, Bar], index: int) -> Bar:
        result: Bar = Bar(int(value),
                          [index * self.width, _resolution[1] - value, self.width - self.is_separated, value + 1],
                          bar_color=self.bar_color,
                          compare_color=self.compare_color,
                          delay=self.delay) \
            if self.only_positive else \
            Bar(int(value),
                [index * self.width, _resolution[1] // 2 - (int(value) if 0 < int(value) else 0),
                 self.width - self.is_separated, abs(int(value) + 1)],
                bar_color=self.bar_color,
                compare_color=self.compare_color,
                delay=self.delay)

        return result

    def __erase_bar(self, index: int) -> bool:
        _main_canvas.fill(self.background_color,
                          rect=Rect([index * self.width, 0, self.width - self.is_separated, _resolution[1]]))
        return True

    @staticmethod
    def check_given_values(values: list[int]) -> bool:
        if not values:
            return False

        assert len(values) <= _resolution[0], f"len(values) larger than resolution width ({_resolution[0]})"
        assert not (_resolution[0] % len(values)), f"resolution width ({_resolution[0]}) not divisible by len(values)"
        return True

    @staticmethod
    def check_given_sample_size(sample_size: int) -> None:
        if sample_size is None:
            return

        assert 0 < sample_size, "sample_size was not given or is negative"
        assert sample_size <= _resolution[0], f"sample size larger than resolution width ({_resolution[0]})"
        assert not (_resolution[0] % sample_size), f"resolution width ({_resolution[0]}) not divisible by sample_size"

    @staticmethod
    def run() -> None:
        display.toggle_fullscreen()
        display.update()

    def rand_values(self) -> list[int]:
        return rand_array(10, _resolution[1], self.sample_size, self.true_random) \
            if self.only_positive else \
            rand_array(-_resolution[1] // 2, _resolution[1] // 2, self.sample_size, self.true_random)

    def independent_run(self) -> None:
        display.toggle_fullscreen()
        display.update()
        self.running = True

        while True:
            self.check_input()

    def check_input(self, function: any = None, is_default: bool = False) -> int:
        for i in event.get():
            if i.type == QUIT:
                return 0

            if i.type == KEYDOWN:
                if i.key == K_ESCAPE:
                    quit()

                if i.key == K_TAB:
                    print(self)
                    return 1

                if i.key == K_SPACE:
                    self.running = not self.running
                    return 2

                if i.key == K_r:
                    shuffle(self)
                    self.running = False

                    if function:
                        return function(self) if not is_default else function()

                    return 3

    def select(self, index: int) -> None:
        _main_canvas.fill(self.select_color, rect=self.__bar_objects[index])
        self.update_ind(index)

    def select_2(self, index: int) -> None:
        _main_canvas.fill(self.second_select_color, rect=self.__bar_objects[index])
        self.update_ind(index)

    def unselect(self, index: int) -> None:
        _main_canvas.fill(self.bar_color, rect=self.__bar_objects[index])
        self.update_ind(index)

    def update_ind(self, *index: int) -> None:
        for i in index:
            display.update(Rect([i * self.width, 0, self.width - self.is_separated, _resolution[1]]))

    def full_unselect(self) -> None:
        for i in range(len(self)):
            _main_canvas.fill(self.bar_color, rect=self.__bar_objects[i])

        display.update()

    def end_sort(self) -> None:
        self.unselect(len(self) - 1)

        for i in range(len(self) - 1):
            sleep(self.delay)
            self.select_2(i + 1)
            self.select(i)

        sleep(1.5)

        self.full_unselect()
