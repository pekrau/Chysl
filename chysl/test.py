"Test diagrams."

from icecream import ic

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
    "piechart": ["pyramid", "day", "pies_column", "pies_row",],
    # XXX dendrogram
    "plot2d": ["scatter_points", "scatter_iris", "line_random_walks",],
    "column": [
        "universe_earth",
        "pies_column",
        "notes_column",
        "notes",
        "markers",
        "dimensions",
        "scatter_iris",
    ],
    "row": ["pies_row", "scatter_iris",],
    "note": ["declaration", "notes_column", "notes", "pies_column", "poster",],
    "board": ["poster", "notes",],
}


def get_universe(legend=True):
    universe = Timelines(
        dict(text="Universe", bold=True, color="blue"),
        legend=legend,
        axis=dict(absolute=True, caption="Billion years ago"),
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
        "Earth", legend=legend, axis=dict(absolute=True, caption="Billion years ago")
    )
    earth += Period("Earth", -4_567_000_000, 0)
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
    day = Piechart(dict(text="Day", size=30), total=24, diameter=400)
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
        footer=dict(text="Copyright 2025 Per Kraulis", italic=True),
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
        title=dict(text="Declaration", placement="left", bold=True),
        body=dict(text="This software was\nwritten by me.", placement="right"),
        footer=dict(text="Copyright 2025 Per Kraulis", italic=True),
    )

    decl.save("declaration.yaml")
    decl.render("declaration.svg")


def test_scatter_points():
    colors = itertools.cycle(
        ["blue", "red", "green", "purple", "cyan", "orange", "lime", "black"]
    )
    markers = itertools.cycle(["disc", "alpha", "mars"])
    plot = Plot2d("Scattered points inline")
    plot += Scatter2d(
        [
            dict(
                x=random.uniform(0, 100),
                y=random.uniform(0, 100),
                color=next(colors),
                marker=next(markers),
                size=random.uniform(40, 100),
                opacity=random.uniform(0.3, 0.8),
            )
            for i in range(25)
        ]
    )
    plot.save("scatter_points.yaml")
    plot.render("scatter_points.svg")


def test_scatter_iris():
    "Plots of the classic iris dataset published by R.A. Fisher, 1936."
    all_plots = Column(dict(text="Iris flower measurements", size=30))
    for field1 in ["sepal length", "sepal width", "petal length", "petal width"]:
        all_plots += (row := Row())
        for field2 in ["sepal length", "sepal width", "petal length", "petal width"]:
            if field1 == field2:
                row += Note(
                    body=dict(text=field1.capitalize(), size=24),
                    background="white",
                    width=300,
                    frame=0,
                )
            else:
                row += (plot := Plot2d(width=300))
                plot += Scatter2d(
                    dict(
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
                )
    all_plots += (caption := Column())
    caption += Note(
        body=dict(text="Iris setosa: red circles", size=24, color="red"),
        background="white",
        frame=0)
    caption += Note(
        body=dict(text="Iris versicolor: green triangles", size=24, color="green"),
        background="white",
        frame=0)
    caption += Note(
        body=dict(text="Iris virginica: blue squares", size=24, color="blue"),
        background="white",
        frame=0)
    all_plots.save("scatter_iris.yaml")
    all_plots.render("scatter_iris.svg")


def test_line_random_walks():
    # Prepare database.
    random.seed(12345)
    cnx = sqlite3.connect("line_random_walks.db")
    cnx.execute("CREATE TABLE IF NOT EXISTS walks(i INTEGER PRIMARY KEY, x REAL, y REAL, run INTEGER)")
    cnx.execute("DELETE FROM walks")
    counter = itertools.count()
    runs = list(range(1, 10))
    for run in runs:
        x = 0
        y = 0
        for i in range(1, 200):
            x += random.uniform(-1.0, 1.0)
            y += random.uniform(-1.0, 1.0)
            cnx.execute("INSERT INTO walks VALUES(?, ?, ?, ?)", (next(counter), x, y, run))
        cnx.commit()
    cnx.close()

    plot = Plot2d("Random walks (source: db)")
    colors = itertools.cycle(["red", "green", "blue", "lime",  "orange",
                              "cyan", "gold",  "dodgerblue",  "gray"])
    for run in runs:
        plot += Line2d(dict(source=dict(database="sqlite",
                                        location="line_random_walks.db",
                                        select=f"SELECT x, y FROM walks WHERE run={run} ORDER BY i")),
                       color=next(colors)
                       )

    plot.save("line_random_walks.yaml")
    plot.render("line_random_walks.svg")

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
    poster.append(dict(x=0, y=100, component=dict(include="universe.yaml")))
    poster.append(dict(x=50, y=230, component=dict(include="earth.yaml")))
    poster.render("poster.svg")
    poster.save("poster.yaml")


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
        test_line_random_walks()
        test_notes()
        test_poster()
        test_dimensions()
    finally:
        os.chdir(origdir)


if __name__ == "__main__":
    run_tests()
