"Dendrogram: tree formed by branches."

import copy

import constants
import utils
from chart import Chart
from dimension import Dimension
from path import Path


class Dendrogram(Chart):
    "Dendrogram: tree formed by branches."

    DEFAULT_WIDTH = 600
    DEFAULT_SIZE = 20
    DEFAULT_COLOR = "blue"

    SCHEMA = {
        "title": __doc__,
        "$anchor": "dendrogram",
        "type": "object",
        "required": ["entries"],
        "additionalProperties": False,
        "properties": {
            "title": {
                "title": "Title of the chart.",
                "$ref": "#text",
            },
            "width": {
                "title": "Width of chart, in pixels.",
                "type": "number",
                "default": DEFAULT_WIDTH,
                "exclusiveMinimum": 0,
            },
            # "axis": {
            #     "title": "Axis specification.",
            #     "$ref": "#axis",
            # },
            "entries": {
                "title": "Branches.",
                "type": "array",
                "items": {
                    "$anchor": "branch",
                    "type": "object",
                    "required": ["length"],
                    "additionalProperties": False,
                    "properties": {
                        "label": {
                            "title": "Label for the branch.",
                            "type": "string",
                        },
                        "start": {
                            "title": "Starting point of the branch.",
                            "type": "number",
                        },
                        "length": {
                            "title": "Length of the branch.",
                            "type": "number",
                            "exclusiveMinimum": 0,
                        },
                        "branches": {
                            "title": "Branches from this branch.",
                            "type": "array",
                            "items": {"$ref": "#branch"},
                        },
                    },
                },
            },
        },
    }

    def __init__(
        self,
        title=None,
        entries=None,
        width=None,
    ):
        super().__init__(title=title, entries=entries)
        assert width is None or (isinstance(width, (int, float)) and width > 0)

        self.width = width or self.DEFAULT_WIDTH

    def append(self, entry):
        "Append the entry to the diagram."
        self.check_entry(entry)
        self.entries.append(entry)

    def check_entry(self, entry):
        Check(entry).process()

    def as_dict(self):
        for entry in self.entries:
            entry_copy = copy.deepcopy(entry)
            cleanup = Cleanup(entry_copy)
            cleanup.process()
            entries.append(entry_copy)
        result = super().as_dict()
        if self.width != self.DEFAULT_WIDTH:
            result["width"] = self.width
        if self.axis is not True:
            result["axis"] = self.axis
        result["entries"] = entries = []
        return result

    def entries_as_dict(self):
        result = []
        for entry in self.entries:
            entry2 = {"start": entry["start"], "end": entry["end"]}
            # XXX add other non-default properties
            result.append(entry2)
        return {"entries": result}

    def build(self):
        """Create the SVG elements in the 'svg' attribute. Adds the title, if given.
        Set the 'svg' and 'height' attributes.
        """
        super().build()

        dimension = Dimension(width=self.width)

        area_height = self.height
        for entry in self.entries:
            dimension.update_span(entry["start"])
            dimension.update_span(entry["end"])
            self.count_branches(entry)
            self.height += self.DEFAULT_SIZE * entry["count"]

        # Axis lines and their labels.
        absolute = False
        color = "gray"
        self.svg += (axis := Element("g"))
        ticks = dimension.get_ticks(absolute=absolute)
        path = Path(ticks[0].pixel, area_height).V(self.height)
        for tick in ticks[1:]:
            path.M(tick.pixel, area_height).V(self.height)
        path.M(ticks[0].pixel, area_height).H(self.width)
        path.M(ticks[0].pixel, self.height).H(self.width)
        axis += Element("path", d=path, stroke=color)

        axis += (labels := Element("g"))
        labels["text-anchor"] = "middle"
        labels["stroke"] = "none"
        labels["fill"] = "black"
        self.height += self.DEFAULT_FONT_SIZE
        for tick in ticks:
            labels += (
                label := Element(
                    "text",
                    tick.label,
                    x=utils.N(tick.pixel),
                    y=utils.N(self.height),
                )
            )
            if tick is ticks[0]:
                label["text-anchor"] = "start"
            elif tick is ticks[-1]:
                label["text-anchor"] = "end"
        self.height += self.DEFAULT_FONT_SIZE * (1 + constants.FONT_DESCEND)

        # Graphics for branches.
        self.relative_height = -(self.height - area_height) / 2
        branches = Element("g", transform=f"translate(0,{-self.relative_height})")
        for entry in self.entries:
            self.render_branch(entry, branches, dimension)
        self.svg += branches

    def count_branches(self, entry):
        count = 1
        for branch in entry.get("branches", []):
            count += self.count_branches(branch)
        entry["count"] = count
        return count

    def render_branch(self, entry, branches, dimension):
        for branch in entry.get("branches", []):
            self.render_branch(branch, branches, dimension)
        branch = Element(
            "path",
            d=Path(
                dimension.get_pixel(entry["start"]),
                self.relative_height + self.DEFAULT_SIZE / 2,
            ).H(dimension.get_pixel(entry["end"])),
            stroke=self.DEFAULT_COLOR,
        )
        branch["stroke-width"] = 4
        branches += branch
        self.relative_height += self.DEFAULT_SIZE


class Traverser:
    "Traverse and process the tree of branches."

    def __init__(self, entry):
        self.entry = entry

    def process(self):
        self.walk(self.entry)

    def walk(self, entry):
        self.preprocess(entry)
        for branch in entry.get("branches", []):
            self.walk(branch)
        self.postprocess(entry)

    def preprocess(self, entry):
        pass

    def postprocess(self, entry):
        pass


class Check(Traverser):
    "Check that branch is of the correct type; dict."

    def preprocess(self, entry):
        if not isinstance(entry, dict):
            raise ValueError(f"invalid entry: {entry}; not a dict")


class Cleanup(Traverser):
    "Remove all superfluous fields in the entries for YAML."

    def preprocess(self, entry):
        keys = set(entry.keys())
        keys.difference_update(["label", "start", "length", "branches"])
        for key in key:
            del entry[key]
