"All currently defined diagram classes and their support classes."

from chart import register, retrieve

from timelines import Timelines, Event, Period
from piechart import Piechart, Slice
from plot2d import Plot2d, Scatter2d, Line2d
# from dendrogram import Dendrogram
from note import Note
from column import Column
from row import Row
from overlay import Overlay
from board import Board

register(Timelines)
register(Event)
register(Period)
register(Piechart)
register(Slice)
register(Plot2d)
register(Scatter2d)
register(Line2d)
# register(Dendrogram)
register(Note)
register(Column)
register(Row)
register(Overlay)
register(Board)
