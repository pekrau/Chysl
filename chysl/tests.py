"Test diagrams."

from icecream import ic

import copy
import itertools
import os
import random
import sqlite3
import string

import constants
import chart
from lib import *

random.seed(12345)


TESTS = {
    "timelines": [
        "universe",
        "earth",
        "universe_earth",
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
        "markers",
        "points_marks",
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
        "points_marks",
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
    instance2 = chart.retrieve(filename)
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
        raise ValueError(f"instance renderings differ: {filename}")


def get_universe(legend=True):
    universe = Timelines(
        title=dict(text="Universe", bold=True, size=24, color="darkorchid"),
        legend=legend,
        axis=dict(absolute=True, caption="Billion years ago", max=50_000_000),
    )
    universe += dict(
        instant=-13_787_000_000,
        label="Big Bang",
        timeline="Universe",
        marker="burst",
        color="red",
    )
    universe += dict(
        begin=dict(value=-7_500_000_000, low=-8_500_000_000),
        end=0,
        label="Milky Way galaxy",
        timeline="Universe",
        color="dodgerblue",
        fuzzy="gradient",
        href="https://en.wikipedia.org/wiki/Milky_Way",
    )
    universe += dict(
        instant=-7_500_000_000,
        timeline="Universe",
        color="white",
        marker="galaxy",
        href="https://en.wikipedia.org/wiki/Milky_Way",
    )
    universe += dict(begin=-4_567_000_000, end=0, label="Earth", color="lightgreen")
    return universe


def get_earth(legend=True):
    earth = Timelines(
        title="Earth",
        legend=legend,
        axis=dict(absolute=True, caption="Billion years ago", max=20_000_000),
    )
    earth += dict(begin=-4_567_000_000, end=0, label="Earth", color="skyblue")
    earth += dict(
        begin=dict(value=-4_000_000_000, low=-4_100_000_000, high=-3_950_000_000),
        end=dict(value=-2_500_000_000, error=200_000_000),
        label="Archean",
        color="wheat",
        fuzzy="gradient",
    )
    earth += dict(instant=-4_200_000_000, label="LUCA?", timeline="Unicellular")
    earth += dict(
        begin=dict(value=-3_480_000_000, low=-4_200_000_000),
        end=0,
        label="Unicellular organisms",
        timeline="Unicellular",
        fuzzy="gradient",
    )
    earth += dict(
        begin=dict(value=-1_650_000_000, error=200_000_000), end=0, label="Eukaryotes"
    )
    earth += dict(
        begin=dict(value=-3_400_000_000, high=-2_600_000_000),
        end=0,
        label="Photosynthesis",
        color="springgreen",
        fuzzy="gradient",
    )
    earth += dict(
        begin=dict(value=-470_000_000, error=50_000_000),
        end=0,
        label="Plants",
        timeline="Photosynthesis",
        color="green",
        placement="left",
        fuzzy="wedge",
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


def test_pyramid():
    pyramid = Piechart(
        "Pyramid",
        start=132,
        palette=["#4c78a8", "#9ecae9", "#f58518"],
        frame=dict(color="gray", thickness=4),
    )
    pyramid += dict(value=7, label="Shadow")
    pyramid.add(dict(value=18, label="Sunny"))
    pyramid.add(dict(value=70, label="Sky"))
    pyramid.save("pyramid.yaml")
    pyramid.render("pyramid.svg")
    check_roundtrip(pyramid, "pyramid.yaml")


def test_markers():
    colors = itertools.cycle(["gray", "coral", "dodgerblue", "orange", "lime"])
    N_PER_ROW = 3

    all_markers = Column(padding=10)
    for title, markers in [
        ("Geometry markers", constants.GEOMETRY_MARKERS),
        ("Symbol markers", constants.SYMBOL_MARKERS),
        ("Astronomy markers", constants.ASTRONOMY_MARKERS),
        ("Greek markers", constants.GREEK_MARKERS),
    ]:
        all_markers += (
            chart := Scatter2d(
                title,
                width=400,
                height=25 * (1 + (len(markers) - 1) // N_PER_ROW),
                xaxis=dict(max=3.0, labels=False),
                yaxis=False,
                xgrid=False,
                ygrid=False,
            )
        )
        for pos, marker in enumerate(markers):
            chart += dict(
                x=pos % N_PER_ROW + 0.2,
                y=pos // N_PER_ROW + 1,
                marker=marker,
                label=marker,
                color=next(colors),
            )

    all_markers.save("markers.yaml")
    all_markers.render("markers.svg")
    check_roundtrip(all_markers, "markers.yaml")


def test_day():
    day = Piechart(
        title=dict(text="Day", size=30),
        slices=dict(source="day.csv", map=dict(value="hours")),
        total=24,
        diameter=400,
    )

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
    pajer = Column("Pies in column", padding=10)

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
    pajer = Row("Pies in row", padding=10)

    palette = ["white", "yellow", "gold", "red"]
    pajer += (paj := Piechart(title="Strawberry pie", diameter=300, palette=palette))
    paj += dict(value=7, label="Flour")
    paj += dict(value=2, label="Eggs")
    paj += dict(value=3, label="Butter")
    paj += dict(
        value=3, label="Strawberries", href="https://en.wikipedia.org/wiki/Strawberry"
    )

    pajer += (paj := Piechart(title="Rhubarb pie", palette=palette))
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
        width=200,
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
        title="Scattered points inline",
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
        xaxis=dict(caption="X dimension"),
        yaxis=dict(caption="Y dimension"),
    )
    scatter.save("scatter_points.yaml")
    scatter.render("scatter_points.svg")
    check_roundtrip(scatter, "scatter_points.yaml")


def test_scatter_iris():
    "Charts of the classic iris dataset published by R.A. Fisher, 1936."
    charts = Row(padding=4)
    fields = ["sepal length", "sepal width", "petal length", "petal width"]
    for field2 in fields:
        charts += (column := Column(padding=4, align=constants.RIGHT))
        for field1 in fields:
            yaxis = dict([(f, dict()) for f in fields])
            for params in yaxis.values():
                if field2 == "sepal length":
                    params["labels"] = True
                    params["caption"] = field1.capitalize()
                else:
                    params["labels"] = False
            # Last column.
            xaxis = dict([(f, dict()) for f in fields])
            if field1 == "petal width":
                xaxis[field2]["caption"] = field2.capitalize()
                xaxis[field2]["labels"] = True
            else:
                xaxis[field2]["labels"] = False
            column += Scatter2d(
                points=dict(
                    source="scatter_iris.csv",
                    map=dict(
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
                height=300,
                size=6,
            )
    caption = Column()
    caption += Note(
        body=dict(text="Iris setosa: red circles", size=24, color="red"),
        background="white",
        frame=False,
    )
    caption += Note(
        body=dict(text="Iris versicolor: green triangles", size=24, color="green"),
        background="white",
        frame=False,
    )
    caption += Note(
        body=dict(text="Iris virginica: blue squares", size=24, color="blue"),
        background="white",
        frame=False,
    )
    aggregate = Column(dict(text="Iris flower measurements", size=30), padding=4)
    aggregate += charts
    aggregate += caption
    aggregate.save("scatter_iris.yaml")
    aggregate.render("scatter_iris.svg")
    check_roundtrip(aggregate, "scatter_iris.yaml")


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
        for i in range(200):
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
        color="blue",
        thickness=10,
        opacity=0.25,
        href="https://en.wikipedia.org/wiki/Random_walk",
    )
    colors = itertools.cycle(
        ["red", "green", "blue", "lime", "orange", "cyan", "gold", "dodgerblue", "gray"]
    )
    for run in runs:
        lines += dict(
            line=dict(
                database="sqlite",
                source="lines_random_walks.db",
                select=f"SELECT x, y FROM walks WHERE run={run} ORDER BY i",
            ),
            color=next(colors),
        )

    lines.save("lines_random_walks.yaml")
    lines.render("lines_random_walks.svg")
    check_roundtrip(lines, "lines_random_walks.yaml")


def test_notes():
    column = Column("Notes in a column", padding=4)
    column += Note("Header", "Body", "Footer")
    column += Note("Header", "Body")
    column += Note(body="Body", footer="Footer")
    column += Note("Header")
    column += Note(body="Body", width=200)
    column += Note(footer="Footer", width=200)
    column += Note("Header", "Body (no lines)", "Footer", line=0, width=200)
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
        x=150,
        y=10,
        scale=1.5,
        subchart=Note("By Per Kraulis", body="Ph.D.", footer="Stockholm University"),
    )
    poster.add_item(x=0, y=150, subchart=dict(include="universe.yaml"))
    poster.add_item(x=50, y=290, subchart=dict(include="earth.yaml"))
    poster.render("poster.svg")
    poster.save("poster.yaml")
    check_roundtrip(poster, "poster.yaml")


def test_dimensions():
    column = Column("Dimension tick ranges", padding=20)
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
        timelines += dict(begin=1, end=last)
    column.save("dimensions.yaml")
    column.render("dimensions.svg")
    check_roundtrip(column, "dimensions.yaml")


def test_points_marks():
    points_marks = Overlay("One scatterplot on top of another")
    chart1 = Scatter2d(
        points=[
            dict(x=1, y=1, color="gold", href="https://en.wikipedia.org/wiki/Gold"),
            dict(x=2, y=2, color="blue"),
            dict(x=3, y=3, color="red"),
        ],
        size=60,
    )
    points_marks += dict(subchart=chart1)
    chart2 = Scatter2d(
        points=[
            dict(x=1, y=1, marker="alpha"),
            dict(x=2, y=2, marker="beta", color="white"),
            dict(x=3, y=3, marker="gamma"),
        ],
        size=30,
    )
    points_marks += dict(subchart=chart2, opacity=0.5)
    points_marks.save("points_marks.yaml")
    points_marks.render("points_marks.svg")
    check_roundtrip(points_marks, "points_marks.yaml")


def run_tests():
    origdir = os.getcwd()
    try:
        os.chdir("../docs")
        test_universe()
        test_earth()
        test_universe_earth()
        test_pyramid()
        test_markers()
        test_day()
        # test_tree()
        test_pies_column()
        test_pies_row()
        test_declaration()
        test_scatter_points()
        test_scatter_iris()
        test_lines_random_walks()
        test_notes()
        test_poster()
        test_dimensions()
        test_points_marks()
    finally:
        os.chdir(origdir)


if __name__ == "__main__":
    run_tests()
