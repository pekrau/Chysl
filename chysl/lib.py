"All currently defined diagram classes and their support classes."

from chart import register, retrieve

from timelines import Timelines, Event, Period

register(Timelines)
register(Event)
register(Period)

from piechart import Piechart, Slice

register(Piechart)
register(Slice)

# from dendrogram import Dendrogram
# register(Dendrogram)

from plot2d import Plot2d, Scatter2d

register(Plot2d)
register(Scatter2d)

from note import Note

register(Note)

from column import Column

register(Column)

from row import Row

register(Row)

from board import Board

register(Board)
