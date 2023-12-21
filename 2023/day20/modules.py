from __future__ import annotations

import re
from enum import Enum
from sys import stdin


class Signal(Enum):
    LOW = False
    HIGH = True


# The main module map
modules: dict[str: Module] = {}

# Pulses are processed in the order they are sent.
# When a pulse is received, it gets added to the queue.
processing_queue: list[tuple[Module, str, Signal]] = []


class Module:
    id: str
    subscribers: list[str]
    counter: dict[Signal: int]

    def __init__(self, name: str):
        self.id = name
        if name in modules:
            raise ValueError(f"Duplicate module: {name}")
        modules[name] = self
        self.subscribers = []
        self.reset_counter()

    def reset_counter(self):
        self.counter = {Signal.LOW: 0, Signal.HIGH: 0}

    def process(self, sender, signal):
        # Receives a signal, processes internal state (including count), and sends any outgoing signals.
        pass

    def send(self, signal):
        # Sends signals to all subscribers by adding them to the processing queue.
        for module in self.subscribers:
            self.counter[signal] += 1
            processing_queue.append((modules[module], self.id, signal))
            if verbose:
                print(f"{self.id} -{'high' if signal == Signal.HIGH else 'low'}-> {module}")

    def count(self):
        # Returns the number of low and high pulses sent by this module
        return self.counter[Signal.LOW], self.counter[Signal.HIGH]


class Button(Module):
    # Always has the id "button"
    def __init__(self, name: str):
        super().__init__(name)
        self.subscribers.append("broadcaster")

    def process(self, sender=None, signal=None):
        self.send(Signal.LOW)


class Broadcaster(Module):
    # Always has the id "broadcaster"
    def process(self, sender, signal):
        self.send(signal)


class FlipFlop(Module):
    # False = off, True = on.
    state: bool

    def __init__(self, name: str):
        super().__init__(name)
        self.state = False

    def process(self, sender, signal):
        # Ignore high pulses
        if signal == Signal.HIGH:
            return

        # Flip state and send a high pulse if it was off, or a low pulse if it was on.
        self.send(Signal.LOW if self.state else Signal.HIGH)
        self.state = not self.state


class Conjunction(Module):
    # Remembers the most recent pulse received from each connected input
    # Defaults to low for each connection.
    state: dict[str: Signal]

    def __init__(self, name: str):
        super().__init__(name)
        self.state = {}

    def process(self, sender, signal):
        # Update memory
        self.state[sender] = signal

        # If it remembers high pulses for all inputs, it sends low, else sends high.
        out = True  # True if all inputs are high
        for s in self.state.values():
            out = out and (True if s == Signal.HIGH else False)

        self.send(Signal.LOW if out else Signal.HIGH)


class Dummy(Module):
    # Does nothing, but remembers its inputs.

    inc_counter: dict[Signal: int]

    def __init__(self, name: str):
        super().__init__(name)
        self.reset_counter()

    def process(self, sender, signal):
        self.inc_counter[signal] += 1

    def reset_counter(self):
        self.inc_counter = {Signal.LOW: 0, Signal.HIGH: 0}


pattern = r"^(?P<type>[\%\&]|broadcaster)(?P<id>\w*)\s*->\s*(?P<output>(?:\w*(?:,\s+|$))*)"


def create_module(index, line):
    # Regex magic
    m: re.Match[str] = re.match(pattern, line)
    if m is None:
        raise ValueError(f"Syntax error in line {index}: {line}")

    # Create the module
    module: Module
    match m["type"]:
        case "broadcaster":
            module = Broadcaster("broadcaster")
        case "%":
            module = FlipFlop(m["id"])
        case "&":
            module = Conjunction(m["id"])
        case _:
            raise ValueError(f"Invalid type in line {index}: {line}")

    # Add outputs to the module
    for s in m["output"].split(","):
        if s != '':
            module.subscribers.append(s.strip())

    if verbose:
        print(f"Module \"{module.id}\" created with subscribers {module.subscribers}")


def create_state_machine():
    # Start by adding the button
    button = Button("button")

    # Process input to set up module list
    index = 0
    for line in open("input.txt"):
        for q in line.splitlines():
            create_module(index, q)
            index += 1

    # Since conjunctions need to know all incoming connections, we iterate over the module list checking.
    for name, module in modules.copy().items():
        for subscriber in module.subscribers:
            # Modules that were referenced but not declared can be added as dummies here.
            if subscriber not in modules:
                Dummy(subscriber)

            # Add to conjunctions
            if isinstance(modules[subscriber], Conjunction):
                modules[subscriber].state[name] = Signal.LOW
                if verbose:
                    print(f"Conjunction module {subscriber} gained issuer {name}")

    if verbose:
        print("State machine complete.\n\n")

    return button


def press_button(button):
    button.process()
    while processing_queue:
        module, sender, signal = processing_queue.pop(0)
        module.process(sender, signal)


verbose = False


