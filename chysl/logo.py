"Chysl logo."

import constants
from minixml import Element
from vector2 import Vector2
from path import Path


def logo(size=100):
    svg = Element(
        "svg",
        xmlns=constants.SVG_XMLNS,
        width=size,
        height=size,
        viewBox=f"0 0 {size} {size}",
    )
    svg += (
        g := Element("g", transform=f"translate(0, {5*size/1000}) scale({size/10})")
    )
    g += (
        path := Element(
            "path", d=Path(0, 8).h(4).l(1, 1).l(1, -1).h(4), stroke="black", fill="none"
        )
    )
    path["stroke-width"] = 0.5
    g += (
        path := Element(
            "path",
            d=Path(0, 0).L(7, -1).C(8.5, -1.2, 8.5, 1.2, 7, 1).Z(),
            stroke="none",
            fill="black",
        )
    )
    path["transform"] = "translate(5, 7.8) rotate(297)"
    g += (
        line := Element(
            "line", x1=0.8, y1=0.8, x2=1.8, y2=1.8, stroke="black", fill="none"
        )
    )
    line["stroke-width"] = 0.1
    line["stroke-linecap"] = "round"
    line["transform"] = "translate(5, 7.8) rotate(159)"
    g += (line := line.copy())
    line["transform"] = "translate(5, 7.8) rotate(192)"
    g += (line := line.copy())
    line["transform"] = "translate(5, 7.8) rotate(225)"
    g += (line := line.copy())
    line["transform"] = "translate(5, 7.8) rotate(286)"
    return svg


if __name__ == "__main__":
    for size in [32, 64, 128]:
        with open(f"../docs/logo{size}.svg", "w") as outfile:
            logo(size).write(outfile, indent=2, xml_decl=True)
