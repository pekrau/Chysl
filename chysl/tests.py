"Test diagrams."

from icecream import ic

import copy
import itertools
import os
import random
import sqlite3
import string

import constants
from lib import *

random.seed(12345)


TESTS = {
    "timelines": [
        "universe",
        "earth",
        "universe_earth",
        "markers",
        "poster",
        "dimensions",
    ],
    "piechart": [
        "pyramid",
        "day",
        "pies_column",
        "pies_row",
    ],
    # XXX dendrogram
    "lines2d": [
        "lines_random_walks",
    ],
    "scatter2d": [
        "scatter_points",
        "scatter_iris",
        "overlay",
    ],
    "column": [
        "universe_earth",
        "pies_column",
        "notes_column",
        "notes",
        "markers",
        "dimensions",
        "scatter_iris",
    ],
    "row": [
        "pies_row",
        "scatter_iris",
    ],
    "overlay": [
        "overlay",
    ],
    "note": [
        "declaration",
        "notes_column",
        "notes",
        "pies_column",
        "poster",
    ],
    "board": [
        "poster",
        "notes",
    ],
}


def check_roundtrip(instance1, filename):
    """Ensure that the given instance is identical to the instance
    specified in the YAML file.
    """
    instance2 = retrieve(filename)
    if instance1 != instance2:
        ic(instance1, instance2)
        raise ValueError("instances differ")

    r1 = instance1.render(restart_unique_id=True)
    r2 = instance2.render(restart_unique_id=True)
    if r1 != r2:
        with open("i1.svg", "w") as outfile:
            outfile.write(r1)
        with open("i2.svg", "w") as outfile:
            outfile.write(r2)
        raise ValueError("instance renderings differ: filename")


def get_universe(legend=True):
    universe = Timelines(
        dict(text="Universe", bold=True, color="blue"),
        legend=legend,
        axis=dict(absolute=True, caption="Billion years ago"),
        grid=False,
    )
    universe += Event(
        "Big Bang", -13_787_000_000, timeline="Universe", marker="burst", color="red"
    )
    universe += Period(
        "Milky Way galaxy",
        dict(value=-7_500_000_000, low=-8_500_000_000),
        0,
        timeline="Universe",
        color="dodgerblue",
        fuzzy="gradient",
        href="https://en.wikipedia.org/wiki/Milky_Way",
    )
    universe += Event(
        "",
        -7_500_000_000,
        timeline="Universe",
        color="white",
        marker="galaxy",
        href="https://en.wikipedia.org/wiki/Milky_Way",
    )
    universe += Period("Earth", -4_567_000_000, 0, color="lightgreen")
    return universe


def get_earth(legend=True):
    earth = Timelines(
        "Earth",
        legend=legend,
        axis=dict(absolute=True, caption="Billion years ago"),
    )
    earth += Period("Earth", -4_567_000_000, 0, color="skyblue")
    earth += Period(
        "Archean",
        dict(value=-4_000_000_000, low=-4_100_000_000, high=-3_950_000_000),
        dict(value=-2_500_000_000, error=200_000_000),
        color="wheat",
        fuzzy="gradient",
    )
    earth += Event("LUCA?", -4_200_000_000, timeline="Unicellular")
    earth += Period(
        "Unicellular organisms",
        dict(value=-3_480_000_000, low=-4_200_000_000),
        0,
        timeline="Unicellular",
        fuzzy="gradient",
    )
    earth += Period("Eukaryotes", -1_650_000_000, 0)
    earth += Period(
        "Engineers",
        dict(value=-3_300_000_000, error=200_000_000),
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
    check_roundtrip(universe, "universe.yaml")


def test_earth():
    earth = get_earth()
    earth.save("earth.yaml")
    earth.render("earth.svg")
    check_roundtrip(earth, "earth.yaml")


def test_universe_earth():
    both = Column("Universe and Earth")
    both += get_universe(legend=False)
    both += get_earth(legend=False)
    both.save("universe_earth.yaml")
    both.render("universe_earth.svg")
    check_roundtrip(both, "universe_earth.yaml")


def test_markers():
    colors = itertools.cycle(["gray", "coral", "dodgerblue", "orange", "lime"])
    N_PER_ROW = 3

    all_markers = Column("Predefined markers")

    all_markers += (markers := Timelines("Geometry markers", legend=False, axis=False))
    markers += Period("Length", 0, N_PER_ROW)
    for pos, marker in enumerate(constants.GEOMETRY_MARKERS):
        markers += Event(
            marker,
            pos % N_PER_ROW + 0.25,
            timeline=f"Row {1 + pos // N_PER_ROW}",
            marker=marker,
            color=next(colors),
        )

    all_markers += (markers := Timelines("Symbol markers", legend=False, axis=False))
    markers += Period("Length", 0, N_PER_ROW)
    for pos, marker in enumerate(constants.SYMBOL_MARKERS):
        markers += Event(
            marker,
            pos % N_PER_ROW + 0.25,
            timeline=f"Row {1 + pos // N_PER_ROW}",
            marker=marker,
            color=next(colors),
        )

    all_markers += (markers := Timelines("Astronomy markers", legend=False, axis=False))
    markers += Period("Length", 0, N_PER_ROW)
    for pos, marker in enumerate(constants.ASTRONOMY_MARKERS):
        markers += Event(
            marker,
            pos % N_PER_ROW + 0.25,
            timeline=f"Row {1 + pos // N_PER_ROW}",
            marker=marker,
            color=next(colors),
        )

    all_markers += (markers := Timelines("Greek markers", legend=False, axis=False))
    markers += Period("Length", 0, N_PER_ROW)
    for pos, marker in enumerate(constants.GREEK_MARKERS):
        markers += Event(
            marker,
            pos % N_PER_ROW + 0.25,
            timeline=f"Row {1 + pos // N_PER_ROW}",
            marker=marker,
            color=next(colors),
        )

    all_markers.save("markers.yaml")
    all_markers.render("markers.svg")
    check_roundtrip(all_markers, "markers.yaml")


def test_pyramid():
    pyramid = Piechart("Pyramid", start=132, palette=["#4c78a8", "#9ecae9", "#f58518"])
    pyramid += dict(value=7, label="Shadow")
    pyramid.add_slice(18, label="Sunny")
    pyramid.add(dict(value=70, label="Sky"))
    pyramid.save("pyramid.yaml")
    pyramid.render("pyramid.svg")
    check_roundtrip(pyramid, "pyramid.yaml")


def test_day():
    day = Piechart(dict(text="Day", size=30), total=24, diameter=400)
    day += dict(value=8, label="Sleep", color="gray")
    day += dict(value=1, label="Breakfast", color="lightgreen")
    day += dict(value=2, label="Gym", color="lightblue")
    day += dict(value=1, label="Read", color="navy")
    day += dict(value=1, label="Lunch", color="lightgreen")
    day += dict(value=0.4, label="Shuteye", color="gray")
    day += dict(value=4.6, label="Write", color="pink")
    day += dict(value=1, label="Dinner", color="lightgreen")
    day += dict(value=3, label="TV", color="orange")
    day += dict(value=2, label="Read", color="navy")

    day.save("day.yaml")
    day.render("day.svg")
    check_roundtrip(day, "day.yaml")


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

    pajer += (paj := Piechart("Strawberry pie", diameter=200))
    paj += dict(value=7, label="Flour", color="white")
    paj += dict(value=2, label="Eggs", color="yellow")
    paj += dict(value=3, label="Butter", color="gold")
    paj += dict(
        value=3,
        label="Strawberries",
        color="orangered",
        href="https://en.wikipedia.org/wiki/Strawberry",
    )

    pajer += (paj := Piechart("Rhubarb pie", diameter=250))
    paj += dict(value=7, label="Flour", color="white")
    paj += dict(value=2, label="Eggs", color="yellow")
    paj += dict(value=3, label="Butter", color="gold")
    paj += dict(
        value=3,
        label="Rhubarb",
        color="green",
        href="https://en.wikipedia.org/wiki/Rhubarb",
    )

    pajer += Note(
        title="Comment",
        body="Strawberry pie is good.",
        footer=dict(text="Copyright 2025 Per Kraulis", italic=True),
    )

    pajer.save("pies_column.yaml")
    pajer.render("pies_column.svg")
    check_roundtrip(pajer, "pies_column.yaml")


def test_pies_row():
    pajer = Row("Pies in row")

    palette = ["white", "yellow", "gold", "red"]
    pajer += (paj := Piechart("Strawberry pie", diameter=300, palette=palette))
    paj += dict(value=7, label="Flour")
    paj += dict(value=2, label="Eggs")
    paj += dict(value=3, label="Butter")
    paj += dict(
        value=3, label="Strawberries", href="https://en.wikipedia.org/wiki/Strawberry"
    )

    pajer += (paj := Piechart("Rhubarb pie", palette=palette))
    paj += dict(value=7, label="Flour")
    paj += dict(value=2, label="Eggs")
    paj += dict(value=3, label="Butter")
    paj += dict(
        value=3,
        label="Rhubarb",
        color="green",
        href="https://en.wikipedia.org/wiki/Rhubarb",
    )

    pajer.save("pies_row.yaml")
    pajer.render("pies_row.svg")
    check_roundtrip(pajer, "pies_row.yaml")


def test_declaration():
    decl = Note(
        title=dict(text="Declaration", placement="left", bold=True),
        body=dict(text="This software was\nwritten by me.", placement="right"),
        footer=dict(text="Copyright 2025 Per Kraulis", italic=True),
    )
    decl.save("declaration.yaml")
    decl.render("declaration.svg")
    check_roundtrip(decl, "declaration.yaml")


def test_scatter_points():
    colors = itertools.cycle(
        ["blue", "red", "green", "purple", "cyan", "orange", "lime", "black"]
    )
    markers = itertools.cycle(["disc", "alpha", "mars"])
    scatter = Scatter2d(
        "Scattered points inline",
        points=[
            dict(
                x=random.uniform(0, 100),
                y=random.uniform(0, 100),
                color=next(colors),
                marker=next(markers),
                size=random.uniform(40, 100),
                opacity=random.uniform(0.3, 0.8),
            )
            for i in range(25)
        ],
    )
    scatter.save("scatter_points.yaml")
    scatter.render("scatter_points.svg")
    check_roundtrip(scatter, "scatter_points.yaml")


def test_scatter_iris():
    "Plots of the classic iris dataset published by R.A. Fisher, 1936."
    all_plots = Column(dict(text="Iris flower measurements", size=30), padding=4)
    axis = {
        "sepal length": dict(min=4, max=8),
        "sepal width": dict(min=2, max=4.5),
        "petal length": dict(min=0.5, max=7.5),
        "petal width": dict(min=0, max=3),
    }
    for field1 in ["sepal length", "sepal width", "petal length", "petal width"]:
        all_plots += (row := Row(padding=4))
        for field2 in ["sepal length", "sepal width", "petal length", "petal width"]:
            yaxis = copy.deepcopy(axis)
            for params in yaxis.values():
                params["labels"] = field2 == "sepal length"
                params["width"] = 24  # Only effective if 'labels' is True.
            # Last row.
            xaxis = copy.deepcopy(axis)
            if field1 == "petal width":
                xaxis[field2]["caption"] = field2.capitalize()
                xaxis[field2]["labels"] = True
            else:
                xaxis[field2]["labels"] = False
            row += Scatter2d(
                points=dict(
                    source="scatter_iris.csv",
                    parameters=dict(
                        x=field2,
                        y=field1,
                        color=dict(
                            field="class",
                            map={
                                "Iris-setosa": "red",
                                "Iris-versicolor": "green",
                                "Iris-virginica": "blue",
                            },
                        ),
                        marker=dict(
                            field="class",
                            map={
                                "Iris-setosa": "circle",
                                "Iris-versicolor": "triangle",
                                "Iris-virginica": "square",
                            },
                        ),
                    ),
                ),
                xaxis=xaxis[field2],
                yaxis=yaxis[field1],
                width=300,
                size=6,
            )
    all_plots += (caption := Column(padding=0))
    caption += Note(
        body=dict(text="Iris setosa: red circles", size=24, color="red"),
        background="white",
        frame=0,
    )
    caption += Note(
        body=dict(text="Iris versicolor: green triangles", size=24, color="green"),
        background="white",
        frame=0,
    )
    caption += Note(
        body=dict(text="Iris virginica: blue squares", size=24, color="blue"),
        background="white",
        frame=0,
    )
    all_plots.save("scatter_iris.yaml")
    all_plots.render("scatter_iris.svg")
    check_roundtrip(all_plots, "scatter_iris.yaml")


def test_lines_random_walks():
    # Prepare database containing points.
    random.seed(12345)
    cnx = sqlite3.connect("lines_random_walks.db")
    cnx.execute(
        "CREATE TABLE IF NOT EXISTS walks(i INTEGER PRIMARY KEY, x REAL, y REAL, run INTEGER)"
    )
    cnx.execute("DELETE FROM walks")
    counter = itertools.count()
    runs = list(range(1, 10))
    for run in runs:
        x = 0
        y = 0
        for i in range(1, 200):
            x += random.uniform(-1.0, 1.0)
            y += random.uniform(-1.0, 1.0)
            cnx.execute(
                "INSERT INTO walks VALUES(?, ?, ?, ?)", (next(counter), x, y, run)
            )
        cnx.commit()
    cnx.close()

    lines = Lines2d("Random walks (source: db)")
    lines += dict(
        line=[
            dict(x=-15, y=-15),
            dict(x=-15, y=15),
            dict(x=15, y=15),
            dict(x=15, y=-15),
            dict(x=-15, y=-15),
        ],
        color="black",
        linewidth=10,
        opacity=0.25,
        href="https://en.wikipedia.org/wiki/Random_walk",
    )
    colors = itertools.cycle(
        ["red", "green", "blue", "lime", "orange", "cyan", "gold", "dodgerblue", "gray"]
    )
    for run in runs:
        lines += dict(
            line=dict(
                source=dict(
                    database="sqlite",
                    location="lines_random_walks.db",
                    select=f"SELECT x, y FROM walks WHERE run={run} ORDER BY i",
                )
            ),
            color=next(colors),
        )

    lines.save("lines_random_walks.yaml")
    lines.render("lines_random_walks.svg")
    check_roundtrip(lines, "lines_random_walks.yaml")


def test_notes():
    column = Column()
    column += Note("Header", "Body", "Footer")
    column += Note("Header", "Body")
    column += Note(body="Body", footer="Footer")
    column += Note("Header")
    column += Note(body="Body")
    column += Note(footer="Footer")
    column += Note("Header", "Body", "Footer", line=0)
    column += dict(include="declaration.yaml")

    column.save("notes_column.yaml")
    column.render("notes_column.svg")

    board = Board()
    board.add_item(x=0, y=0, subchart=column, scale=1.5)
    board.save("notes.yaml")
    board.render("notes.svg")
    check_roundtrip(board, "notes.yaml")


def test_poster():
    poster = Board("Poster")
    poster.add_item(
        x=250,
        y=10,
        subchart=Note("By Per Kraulis", body="Ph.D.", footer="Stockholm University"),
    )
    poster.add_item(x=0, y=100, subchart=dict(include="universe.yaml"))
    poster.add_item(x=50, y=230, subchart=dict(include="earth.yaml"))
    poster.render("poster.svg")
    poster.save("poster.yaml")
    check_roundtrip(poster, "poster.yaml")


def test_dimensions():
    column = Column("Dimension tick ranges")
    for last in [
        1.00001,
        1.0001,
        1.0002,
        1.1,
        2,
        5,
        10,
        2000,
        10_000_000,
        10_000_000_000,
    ]:
        column += (timelines := Timelines(f"1 - {last}"))
        timelines += Period("Period", 1, last)
    column.save("dimensions.yaml")
    column.render("dimensions.svg")
    check_roundtrip(column, "dimensions.yaml")


def test_overlay():
    overlay = Overlay("One scatterplot on top of another")
    plot1 = Scatter2d(
        points=[
            dict(x=1, y=1, color="gold", href="https://en.wikipedia.org/wiki/Gold"),
            dict(x=2, y=2, color="blue"),
            dict(x=3, y=3, color="red"),
        ],
        size=60,
    )
    overlay += dict(subchart=plot1)
    plot2 = Scatter2d(
        points=[
            dict(x=1, y=1, marker="alpha"),
            dict(x=2, y=2, marker="beta", color="white"),
            dict(x=3, y=3, marker="gamma"),
        ],
        size=30,
    )
    overlay += dict(subchart=plot2, opacity=0.5)
    overlay.save("overlay.yaml")
    overlay.render("overlay.svg")
    check_roundtrip(overlay, "overlay.yaml")


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
        test_scatter_points()
        test_scatter_iris()
        test_lines_random_walks()
        test_notes()
        test_poster()
        test_dimensions()
        test_overlay()
    finally:
        os.chdir(origdir)


if __name__ == "__main__":
    run_tests()
