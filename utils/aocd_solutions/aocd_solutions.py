import itertools
import os
from cProfile import Profile
from time import time
from typing import Callable

import aocd.models
import certifi
from urllib3 import PoolManager, ProxyManager

# Dumb hack to inject CA certs into aocd if desired.
# This is done by injecting a custom PoolManager into aocd's singleton http wrapper.
# This will break if aocd ever changes that behavior.
if ca_cert := os.environ.get('AOCD_CA_CERT', 0):
    if ca_cert.lower() == 'certifi':
        ca_cert = certifi.where()
    http = aocd.utils.http
    proxy = isinstance(aocd.utils.http.pool_manager, ProxyManager)
    headers = http.pool_manager.headers
    proxy_url = os.environ.get("http_proxy") or os.environ.get("https_proxy")

    if proxy_url:
        http.pool_manager = ProxyManager(proxy_url, headers=headers, ca_certs=ca_cert)
    else:
        http.pool_manager = PoolManager(headers=headers, ca_certs=ca_cert)


class FuncWrapper:

    def __init__(self, func, *args, **kwargs):
        """Wraps a function such that extra arguments will be added.
        Positional args will be placed at the front."""
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.func(*(self.args + args), **(self.kwargs | kwargs))


class Puzzle(aocd.models.Puzzle):
    _solution_funcs: list[Callable[[str], int | str]] = [None, None]
    profile = False

    # Set the part 1 solution function
    def solution_a(self, *args, **kwargs):
        return self._set_solution(0, args, kwargs)

    # Set the part 2 solution function
    def solution_b(self, *args, **kwargs):
        return self._set_solution(1, args, kwargs)

    def _set_solution(self, idx, args, kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], Callable):
            self._solution_funcs[idx] = args[0]
            return args[0]


        def wrapper(func):
            w = FuncWrapper(func, *args, **kwargs)
            self._solution_funcs[idx] = w
            return func

        return wrapper

    # Check the solution(s) against the listed examples
    def check_examples(self, *args, **kwargs):

        for i, example in enumerate(self.examples):
            for p, f, a in zip('AB', self._solution_funcs, (example.answer_a, example.answer_b)):
                result, s = self._get_result(f, example.input_data, args, kwargs, f"example{p}")
                success = "Pass." if str(result) == a else f"Fail. Result: {result} (expected {a}.)"
                print(_format_output(f"Example {i+1}{p} {success}", s))

            if example.extra:
                print(f"Note: {example.extra}\n")

    # Submit answers
    def check_solutions(self, *args, **kwargs):
        for p, f in zip("AB", self._solution_funcs):
            if f:
                result, s = self._get_result(f, self.input_data, args, kwargs, f"solution_{p}")
                print(_format_output(f"Part {p} result: {result}", s))
                if p == 'A':
                    self.answer_a = result
                else:
                    self.answer_b = result


    def _get_result(self, f, data, args, kwargs, context):
        wrapped = FuncWrapper(f, *args, **kwargs)
        if self.profile:
            pr = Profile()
            pr.enable()
        else:
            pr = None
        t_start = time()
        result = wrapped(data)
        t_end = time()
        if pr:
            pr.disable()
            pr.dump_stats(f"{context}.prof")

        return result, f"(t={t_end - t_start}s)"

def _format_output(r, t):
    return f"{r:<60}{t:>20}"