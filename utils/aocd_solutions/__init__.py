from typing import Callable

import aocd.models


class Puzzle(aocd.models.Puzzle):
    _solution_funcs: list[Callable[[str], int]] = [None, None]

    # Set the part 1 solution function
    def solution_a(self, func: Callable[[str], int]):
        self._solution_funcs[0] = func
        return func

    # Set the part 2 solution function
    def solution_b(self, func: Callable[[str], int]):
        self._solution_funcs[1] = func
        return func

    # Check the solution(s) against the listed examples
    def check_examples(self):
        all_pass = True

        for i, example in enumerate(self.examples):
            if self._solution_funcs[0] and example.answer_a:
                s = _check_answer(self._solution_funcs[0], example.input_data, example.answer_a)
                if s != "Pass":
                    all_pass = False
                if s:
                    print(f"Example {i+1}A: {s}")

            if self._solution_funcs[1] and example.answer_b:
                s = _check_answer(self._solution_funcs[1], example.input_data, example.answer_b)
                if s != "Pass":
                    all_pass = False
                if s:
                    print(f"Example {i+1}B: {s}")

            if example.extra:
                print(f"Note: {example.extra}\n")

        return all_pass

    # Submit answers
    def check_solutions(self, submit=True):
        if self._solution_funcs[0]:
            result = self._solution_funcs[0](self.input_data)
            print(f"Part A result: {result}")
            if submit:
                self.answer_a = result

        if self._solution_funcs[1]:
            result = self._solution_funcs[1](self.input_data)
            print(f"Part B result: {result}")
            if submit:
                self.answer_b = result


def _check_answer(f, data, answer):
    try:
        result = str(f(data))
    except Exception as E:
        return str(E)

    if result:
        return "Pass" if result == answer else f"Fail.\nYour answer was {result}. Expected {answer}.\n"
