"All currently defined diagram classes and their support classes."

from chart import register, retrieve

from timelines import Timelines, Event, Period
from piechart import Piechart
from scatter2d import Scatter2d
from lines2d import Lines2d
# from dendrogram import Dendrogram
from note import Note
from column import Column
from row import Row
from overlay import Overlay
from board import Board

register(Timelines)
register(Piechart)
register(Scatter2d)
register(Lines2d)
# register(Dendrogram)
register(Note)
register(Column)
register(Row)
register(Overlay)
register(Board)
