"Test diagrams."

from icecream import ic

import itertools
import os
import string

import constants
from lib import *


TESTS = {
    "timelines": ["universe", "earth", "universe_earth", "markers", "poster", "dimensions"],
    "piechart": ["pyramid", "day", "pies_column", "pies_row"],
    # XXX dendrogram
    "plot": ["scatter", "scatter2"],
    "column": ["universe_earth", "pies_column", "notes_column", "notes", "markers", "dimensions"],
    "row": ["pies_row", "markers"],
    "note": ["declaration", "notes_column", "notes", "pies_column", "poster"],
    "board": ["poster", "notes"],
}


def get_universe(legend=True):
    universe = Timelines(
        {"text": "Universe", "bold": True, "color": "blue"},
        legend=legend,
        axis={"absolute": True, "caption": "Billion years ago"},
    )
    universe += Event(
        "Big Bang", -13_787_000_000, timeline="Universe", marker="burst", color="red"
    )
    universe += Period(
        "Milky Way galaxy",
        {"value": -7_500_000_000, "low": -8_500_000_000},
        0,
        timeline="Universe",
        color="dodgerblue",
        fuzzy="gradient",
    )
    universe += Event(
        "",
        -8_500_000_000,
        timeline="Universe",
        color="navy",
        marker="galaxy",
    )
    universe += Period("Earth", -4_567_000_000, 0, color="lightgreen")
    return universe


def get_earth(legend=True):
    earth = Timelines(
        "Earth", legend=legend, axis={"absolute": True, "caption": "Billion years ago"}
    )
    earth += Period("Earth", -4_567_000_000, 0)
    earth += Period(
        "Archean",
        {"value": -4_000_000_000, "low": -4_100_000_000, "high": -3_950_000_000},
        {"value": -2_500_000_000, "error": 200_000_000},
        color="wheat",
        fuzzy="gradient",
    )
    earth += Event("LUCA?", -4_200_000_000, timeline="Unicellular")
    earth += Period(
        "Unicellular organisms",
        {"value": -3_480_000_000, "low": -4_200_000_000},
        0,
        timeline="Unicellular",
        fuzzy="gradient",
    )
    earth += Period("Eukaryotes", -1_650_000_000, 0)
    earth += Period(
        "Engineers",
        {"value": -3_300_000_000, "error": 200_000_000},
        -1_650_000_000,
        color="lightgray",
        fuzzy="wedge",
    )
    earth += Period("Photosynthesis", -3_400_000_000, 0, color="springgreen")
    earth += Period(
        "Plants",
        -470_000_000,
        0,
        timeline="Photosynthesis",
        color="green",
        placement="left",
    )
    return earth


def test_universe():
    universe = get_universe()
    universe.save("universe.yaml")
    universe.render("universe.svg")

    universe2 = retrieve("universe.yaml")
    assert universe == universe2
    assert universe.render(restart_unique_id=True) == universe2.render(
        restart_unique_id=True
    )


def test_earth():
    earth = get_earth()
    earth.save("earth.yaml")
    earth.render("earth.svg")


def test_universe_earth():
    both = Column("Universe and Earth")
    both += get_universe(legend=False)
    both += get_earth(legend=False)
    both.save("universe_earth.yaml")
    both.render("universe_earth.svg")


def test_markers():
    colors = itertools.cycle(["gray", "coral", "dodgerblue", "orange", "lime"])
    N_PER_ROW = 3
    all_markers = Row("Markers", align="top")
    all_markers += (left_panel := Column())
    all_markers += (right_panel := Column())

    left_panel += (markers := Timelines("Geometry markers", legend=False, axis=False))
    markers += Period("Length", 0, N_PER_ROW)
    for pos, marker in enumerate(constants.GEOMETRY_MARKERS):
        markers += Event(
            marker,
            pos % N_PER_ROW + 0.25,
            timeline=f"Row {1 + pos // N_PER_ROW}",
            marker=marker,
            color=next(colors),
        )

    left_panel += (markers := Timelines("Symbol markers", legend=False, axis=False))
    markers += Period("Length", 0, N_PER_ROW)
    for pos, marker in enumerate(constants.SYMBOL_MARKERS):
        markers += Event(
            marker,
            pos % N_PER_ROW + 0.25,
            timeline=f"Row {1 + pos // N_PER_ROW}",
            marker=marker,
            color=next(colors),
        )

    left_panel += (markers := Timelines("Astronomy markers", legend=False, axis=False))
    markers += Period("Length", 0, N_PER_ROW)
    for pos, marker in enumerate(constants.ASTRONOMY_MARKERS):
        markers += Event(
            marker,
            pos % N_PER_ROW + 0.25,
            timeline=f"Row {1 + pos // N_PER_ROW}",
            marker=marker,
            color=next(colors),
        )
 
    left_panel += (markers := Timelines("Greek markers", legend=False, axis=False))
    markers += Period("Length", 0, N_PER_ROW)
    for pos, marker in enumerate(constants.GREEK_MARKERS):
        markers += Event(
            marker,
            pos % N_PER_ROW + 0.25,
            timeline=f"Row {1 + pos // N_PER_ROW}",
            marker=marker,
            color=next(colors),
        )

    right_panel += (markers := Timelines("Character markers", legend=False, axis=False))
    markers += Period("Length", 0, N_PER_ROW)
    characters = string.ascii_letters + string.digits + string.punctuation
    for pos, marker in enumerate(characters):
        markers += Event(
            marker,
            pos % N_PER_ROW + 0.25,
            timeline=f"Row {1 + pos // N_PER_ROW}",
            marker=marker,
            color=next(colors),
        )

    all_markers.save("markers.yaml")
    all_markers.render("markers.svg")


def test_pyramid():
    pyramid = Piechart("Pyramid", start=132, palette=["#4c78a8", "#9ecae9", "#f58518"])
    pyramid += Slice("Shadow", 7)
    pyramid += Slice("Sunny", 18)
    pyramid += Slice("Sky", 70)
    pyramid.save("pyramid.yaml")
    pyramid.render("pyramid.svg")

    pyramid2 = retrieve("pyramid.yaml")
    assert pyramid == pyramid2
    assert pyramid.render() == pyramid2.render()


def test_day():
    day = Piechart({"text": "Day", "size": 30}, total=24, diameter=400)
    day += Slice("Sleep", 8, color="gray")
    day += Slice("Breakfast", 1, color="lightgreen")
    day += Slice("Gym", 2, color="lightblue")
    day += Slice("Read", 1, color="navy")
    day += Slice("Lunch", 1, color="lightgreen")
    day += Slice("Shuteye", 0.4, color="gray")
    day += Slice("Write", 4.6, color="pink")
    day += Slice("Dinner", 1, color="lightgreen")
    day += Slice("TV", 3, color="orange")
    day += Slice("Read", 2, color="navy")

    day.save("day.yaml")
    day.render("day.svg")

    day2 = retrieve("day.yaml")
    assert day == day2
    assert day.render() == day2.render()


def test_tree():
    pass
    # tree = Dendrogram("Tree")
    # tree += {
    #     "start": 0,
    #     "length": 4,
    #     "branches": [{"length": 5}, {"length": 6, "branches": [{"length": 4}]}],
    # }
    # tree.save("tree.yaml")
    # tree.render("tree.svg")


def test_pies_column():
    pajer = Column("Pies in column")

    pajer += (paj := Piechart("Strawberry pie", diameter=100))
    paj += Slice("Flour", 7, color="white")
    paj += Slice("Eggs", 2, color="yellow")
    paj += Slice("Butter", 3, color="gold")
    paj += Slice("Strawberries", 3, color="orangered")

    pajer += (paj := Piechart("Rhubarb pie"))
    paj += Slice("Flour", 7, color="white")
    paj += Slice("Eggs", 2, color="yellow")
    paj += Slice("Butter", 3, color="gold")
    paj += Slice("Rhubarb", 3, color="green")

    pajer += Note(
        title="Comment",
        body="Strawberry pie is good.",
        footer={"text": "Copyright 2025 Per Kraulis", "italic": True},
    )

    pajer.save("pies_column.yaml")
    pajer.render("pies_column.svg")

    pajer2 = retrieve("pies_column.yaml")
    assert pajer == pajer2
    assert pajer.render() == pajer2.render()


def test_pies_row():
    pajer = Row("Pies in row")

    palette = ["white", "yellow", "gold", "red"]
    pajer += (paj := Piechart("Strawberry pie", diameter=300, palette=palette))
    paj += Slice("Flour", 7)
    paj += Slice("Eggs", 2)
    paj += Slice("Butter", 3)
    paj += Slice("Strawberries", 3)

    pajer += (paj := Piechart("Rhubarb pie", palette=palette))
    paj += Slice("Flour", 7)
    paj += Slice("Eggs", 2)
    paj += Slice("Butter", 3)
    paj += Slice("Rhubarb", 3, color="green")

    pajer.save("pies_row.yaml")
    pajer.render("pies_row.svg")

    pajer2 = retrieve("pies_row.yaml")
    assert pajer == pajer2
    assert pajer.render() == pajer2.render()


def test_declaration():
    decl = Note(
        title={"text": "Declaration", "placement": "left", "bold": True},
        body={"text": "This software was\nwritten by me.", "placement": "right"},
        footer={"text": "Copyright 2025 Per Kraulis", "italic": True},
    )

    decl.save("declaration.yaml")
    decl.render("declaration.svg")


def test_scatter():
    plot = Plot("Scattered points inline")
    plot += Scatter(
        [
            dict(x=5, y=20),
            dict(x=12, y=12.5, color="red", marker="alpha"),
            dict(x=13, y=12, color="red", marker="beta"),
            dict(x=14, y=11, color="red", marker="gamma"),
            dict(x=19, y=9, color="orange", marker="#"),
            dict(x=0, y=0, size=10),
            dict(x=1, y=1),
            dict(x=6, y={"value": 7, "error": 1}, color="lime"),
        ]
    )
    plot.save("scatter.yaml")
    plot.render("scatter.svg")


def test_scatter_csv():
    plot = Plot("Scattered points from CSV")
    plot += Scatter({"source": "scatter2.csv"})
    plot.save("scatter2.yaml")
    plot.render("scatter2.svg")


def test_notes():
    column = Column()
    column += Note("Header", "Body", "Footer")
    column += Note("Header", "Body")
    column += Note(body="Body", footer="Footer")
    column += Note("Header")
    column += Note(body="Body")
    column += Note(footer="Footer")
    column += Note("Header", "Body", "Footer", line=0)
    column += {"include": "declaration.yaml"}

    column.save("notes_column.yaml")
    column.render("notes_column.svg")

    board = Board()
    board.append(x=0, y=0, scale=1.5, component=column)
    board.save("notes.yaml")
    board.render("notes.svg")


def test_poster():
    poster = Board("Poster")
    poster.append(
        x=250,
        y=10,
        component=Note("By Per Kraulis", body="Ph.D.", footer="Stockholm University"),
    )
    poster.append(dict(x=0, y=100, component={"include": "universe.yaml"}))
    poster.append(dict(x=50, y=230, component={"include": "earth.yaml"}))
    poster.render("poster.svg")
    poster.save("poster.yaml")


def test_dimensions():
    column = Column("Dimension tick ranges")
    for last in [1.00001, 1.0001, 1.0002, 1.1, 2, 5, 10, 2000, 10_000_000, 10_000_000_000]:
        column += (timelines := Timelines(f"1 - {last}"))
        timelines += Period("Period", 1, last)
    column.save("dimensions.yaml")
    column.render("dimensions.svg")
    
               
def run_tests():
    origdir = os.getcwd()
    try:
        os.chdir("../docs")
        test_universe()
        test_earth()
        test_universe_earth()
        test_markers()
        test_pyramid()
        test_day()
        test_tree()
        test_pies_column()
        test_pies_row()
        test_declaration()
        test_scatter()
        test_scatter_csv()
        test_notes()
        test_poster()
        test_dimensions()
    finally:
        os.chdir(origdir)


if __name__ == "__main__":
    run_tests()
