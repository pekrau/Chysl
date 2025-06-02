"Various utility functions."

import itertools
import math

import webcolors

import constants
from minixml import Element


def get_unique_id():
    count = itertools.count(1)
    while True:
        yield f"id{next(count)}"


unique_id = get_unique_id()


def restart_unique_id():
    global unique_id
    unique_id = get_unique_id()


def N(x):
    "Return a minimal string representation of the numerical value."
    assert isinstance(x, (int, float))
    if math.isclose(
        x, (rounded := round(x)), rel_tol=constants.REL_TOL, abs_tol=constants.ABS_TOL
    ):
        return f"{rounded:d}"
    else:
        return f"{x:.3f}".rstrip("0").rstrip(".")


def is_color(value):
    "Is the given value a valid color?"
    if not isinstance(value, str):
        return False
    try:
        webcolors.normalize_hex(value)
    except ValueError:
        try:
            webcolors.name_to_hex(value)
        except ValueError:
            return False
    return True


def is_marker(value):
    "Is the given value a valid marker?"
    if not isinstance(value, str):
        return False
    return value in constants.MARKERS or len(value) == 1


def get_text_length(text, font, size, italic=False, bold=False):
    """Compute length of string given the size in points (pt).
    Uses empirically based measurements.
    """
    assert font in ("sans-serif", "serif", "monospace"), font
    widths = constants.CHARACTER_WIDTHS[font]
    if italic:
        if bold:
            key = "ib"
        else:
            key = "i"
    elif bold:
        key = "b"
    else:
        key = "n"
    if text:
        total = sum([widths.get(c, widths["default"])[key] for c in text])
    else:
        total = 0
    return total * size / 100


if __name__ == "__main__":
    print(next(unique_id))
    print(next(unique_id))
    print(next(unique_id))
    restart_unique_id()
    print(next(unique_id))
