import sys
import pygame
from operator import sub
from matplotlib.pyplot import text
import pandas as pd
import random
import numpy as np
import math

import color as c
import axis as ax
import palletts as p
import graph_props as m

def round_dig(num, base=5, dig=1):
    num = float(num)
    num = num / (math.pow(base, dig))
    num = round(num)
    return num * (math.pow(base, dig))


class distribution:
    def __init__(self, graph, data, x, series, dir=1, domain=m.default_domain, point=-1, pallett=p.green_tea, title="", ):
        self.graph = graph
        self.data = data
        self.x = data[x]
        self.dir = dir

        self.__ordered__ = self.__sort_df__(self.x)
        self.__min__ = self.__find_extremum__(min, 0)
        self.__max__ = self.__find_extremum__(max, -1)

        self.series = data[series]
        self.__unique_series__ = self.unique_series(self.series)
        self.series_data = self.create_series()

        self.pos = domain.pos
        self.size = domain.size

        self.value_axis = ax.Axis(
            self, [self.__min__, self.__max__], self.dir, min=self.__min__)
        self.series_axis = ax.Axis(
            self, self.__return_series_names__(), abs(self.dir - 1),  min=self.__min__)

        self.pallett = pallett

        self.domain = domain
        self.domain.__reinit__(self)
        self.point = self.__return_default_point__(point)
        self.point.__reinit__(self)

        self.title = title

    def __return_default_point__(self, point):
        if point == -1:
            return m.point(self.pallett.prim_RGB)
        return point

    def __find_extremum__(self, func, index):
        extremum = 0
        for series in self.__ordered__:
            extremum = func(series[index], extremum)
        return extremum

    def __sort_df__(self, df):
        returning = []
        rotated = np.rot90(df.to_numpy())
        for series in rotated:
            returning.append(
                list(np.sort(series[np.logical_not(np.isnan(series))])))
        return returning

    def __return_series_names__(self):
        returning = []
        for series in self.series_data:
            returning.append(series.name)
        return returning

    def unique_series(self, series):
        a = series.to_numpy()
        unique_series = np.unique(a)
        return unique_series

    def create_series(self):
        returning = []
        index = 0

        for series in self.__unique_series__:
            for column in self.x:
                rows = self.series == series
                selection = self.data.loc[rows, column]
                # series_obj = self.Series(self, "" + series + ", " + column, selection, index)
                series_obj = self.Series(self, "" + series, selection, index)
                returning.append(series_obj)
                index += 1

        return returning

    # RENDER

    def render(self):
        self.domain.render()
        # self.graph.handler.render_text(self.title, (self.pos[0] + (
        #     self.size[0] / 2),  self.pos[1] + (self.size[1])), self.pallett.text_RGB, 20)

        for series in self.series_data:
            series.render()

        self.value_axis.render()
        self.series_axis.render()

        self.graph.handler.render_que()

    class Series:
        def __init__(self, parent, name, x, index):
            self.parent = parent
            self.name = name
            self.x = np.sort(x.to_numpy())
            self.index = index

            self.random = -1

        def render(self):

            series_space = (self.parent.size[abs(
                self.parent.dir - 1)] / len(self.parent.series_data))

            steps = 1 / len(self.parent.__unique_series__)

            for value in self.x:

                rand = series_space / 3
                if self.random != -1:
                    rand = self.random
                series = (self.index * series_space) + random.uniform(0, rand)

                # print(self.parent.value_axis.interval)
                value = ((value - self.parent.__min__) *
                         self.parent.value_axis.interval) + self.parent.pos[self.parent.dir]
                series += self.parent.pos[abs(self.parent.dir - 1)]

                color = self.parent.pallett.primary_color.return_color_between(
                    self.parent.pallett.secondary_color, steps * self.index).return_color_in("RGB")

                if not np.isnan(value):

                    if self.parent.dir == 0:
                        self.parent.point.render((value, series), color)
                    else:
                        self.parent.point.render((series, value), color)

    # user functions:

    def update_series_rand(self, rand):
        for series in self.series_data:
            series.random = rand
        return self


class area:
    def __init__(self, graph, data, x, y, series, dir=0, domain=m.default_domain, point=-1, line=-1, title=-1, value_axis=-1, series_axis=-1, pallett=p.green_tea,):
        self.graph = graph
        self.data = data
        self.dir = dir

        self.series = data[series]
        self.__unique_series__ = self.unique_series(data[series])

        # this does not gaurentee the data is ready
        self.x = self.__order_data__(x)
        self.y = self.__order_data__(y)

        # get the count of data, if it was specified (this will also override the dir, if one series is the count)
        # By this point the dir is known
        self.x = self.__count__(self.y, y, self.x, 1)
        self.y = self.__count__(self.x, x, self.y, 0)
        self.opp = abs(self.dir - 1)

        # this needs the prepared data
        self.series_data = self.create_series()

        self.__x_min__ = self.__find_extremum__(min, self.x)
        self.__y_min__ = self.__find_extremum__(min, self.y)
        self.__x_max__ = self.__find_extremum__(max, self.x)
        self.__y_max__ = self.__find_extremum__(max, self.y)

        # for the series render function
        self.mins = [self.__x_min__, self.__y_min__]
        self.maxs = [self.__x_max__, self.__y_max__]

        self.pos = domain.pos
        self.size = domain.size

        self.pallett = pallett

        self.value_axis = ax.Axis(self, self.__return_values__(
        ), self.dir, min=self.__x_min__, axis=value_axis)
        self.series_axis = ax.Axis(self, self.__return_series_names__(
        ), self.opp, min=self.__y_min__, axis=series_axis)

        self.domain = domain
        self.domain.__reinit__(self)
        self.point = self.__return_default__(
            point, m.point(self.pallett.prim_RGB))
        self.point.__reinit__(self)
        self.line = self.__return_default__(
            line, m.line(self.pallett.text_RGB))
        self.line.__reinit__(self)
        self.title = self.__return_default__(title, m.text(text=""))
        self.title.__reinit__(self)

    def __return_default__(self, obj, default):
        if obj == -1:
            return default
        return obj

    # find the value series depending on the dir
    def __return_values__(self):
        if self.dir == 0:
            return self.x
        else:
            return self.y

    # orders the data sets, unless they are counts, that will be dealt with later
    def __order_data__(self, series):
        data = ["count()"]
        if series != "count()":
            data = self.data[series]

        if self.__is_numeric__(data):
            return self.__sort_df__(data)
        return data

    # Get the count if it was passed in:
    def __count__(self, counted_series, cs_name, counting_series, dir):
        returning = counting_series
        if str(counting_series[0]) == "count()":
            returning = []

            # The value should always be the primary axis (dir = 0)
            self.dir = dir
            for series in self.__unique_series__:
                counts = []
                rows = self.series == series
                sub_section = self.data.loc[rows, cs_name]
                sub_section = pd.Series(map(round_dig, sub_section))

                for value in counted_series:
                    count = (sub_section == round_dig(value)).sum()
                    counts.append(count)
                returning.append(counts)
        return returning

    # DF management
    def __is_numeric__(self, arr):
        string = str(arr[0])
        if "-" in string:
            string = string.lstrip("-")
        return string.isdigit()

    def __sort_df__(self, df):
        returning = []
        arr = df.to_numpy()
        arr = arr[np.logical_not(np.isnan(arr))]
        returning = np.sort(arr)
        return returning

    def unique_series(self, series):
        a = series.to_numpy()
        unique_series = np.unique(a)
        return unique_series

    def __find_extremum__(self, func, arr):
        extremum = 0
        if isinstance(arr[0], list):
            for series in arr:
                extremum = func(extremum, self.__find_extremum__(func, series))
        else:
            if self.__is_numeric__(arr):
                for value in arr:
                    extremum = func(value, extremum)
        return extremum

    # SERIES

    def __return_series_names__(self):
        returning = []
        for series in self.series_data:
            returning.append(series.name)
        return returning

    def create_series(self):
        returning = []
        index = 0

        for series in self.__unique_series__:
            # depending on the dir, the value series gets the y or x series, and same with the series series

            series_obj = self.Series(self, "", self.x, self.y[index], index)
            if self.dir == 1:
                series_obj = self.Series(
                    self, str(series), self.y, self.x[index], index)
            returning.append(series_obj)
            index += 1

        return returning

    # RENDER

    def render(self):
        self.domain.render()
        self.title.render("", (self.pos[0] + (
            self.size[0] / 2),  self.pos[1] + (self.size[1] + 20)), self.pallett.text_RGB, alignmentY="bottom")

        for series in self.series_data:
            series.render()

        self.value_axis.render()
        self.series_axis.render()

        self.graph.handler.render_que()

    class Series:
        def __init__(self, parent, name, x, y, index):
            self.parent = parent
            self.name = name
            self.x = x
            self.y = y
            self.index = index

        def render(self):

            points = []
            dir = self.parent.dir
            opp = self.parent.opp

            # Basically:
            # There are two coordinate points the value (the dir axis) and the count (the opp axis), both can be on either the x or y axis, and so I need to supply the right x or y data depdning on the orientation of the graph ( this is what all the [dir]  and [opp] are)
            # The self.x and self.y are already changed depending on what the direction is, as they are passed in considering the directin, so I dont need to do any work here

            value_space = (
                self.parent.size[dir] / (self.parent.maxs[dir] - self.parent.mins[dir]))

            count_space = (self.parent.size[opp]) / (len(self.parent.__unique_series__) * (
                20 + self.parent.maxs[opp] - self.parent.mins[opp]))
            total_count_space = (
                self.parent.size[opp]) / (len(self.parent.__unique_series__))

            steps = 1 / len(self.parent.__unique_series__)
            color = self.parent.pallett.primary_color.return_color_between(
                self.parent.pallett.secondary_color, steps * self.index).return_color_in("RGB")

            for i in range(0, len(self.x)):

                value = ((self.x[i] - self.parent.mins[dir])
                         * value_space) + self.parent.pos[dir]
                count = ((self.y[i] - self.parent.mins[opp]) * count_space)

                count += (total_count_space * self.index) + \
                    self.parent.pos[opp]

                point = 0
                if dir == 1:
                    point = (count, value)
                if dir == 0:
                    point = (value, count)
                points.append(point)
                self.parent.point.render(point, color)

            points.sort(key=lambda y: y[dir])
            for i in range(0, len(points) - 1):

                self.parent.line.render(points[i], points[i + 1], color)


# import cofffee.color as c
# import cofffee.palletts as p

# import cofffee.pyg as pg
# import cofffee.graphers as g
# import cofffee.grapher as go
# import cofffee.graph_props as m

# xls = pd.ExcelFile(
#     "/Users/brianmasse/Developer/Classes/CSC630/independent_work/cofffee Chain Visualization/PART I/data/cofffee Chain.xlsx"
# )
# data = pd.read_excel(xls, "cofffee Chain")

# width = 1700
# height = 900

# active_pallett = p.blue_lagoon

# handler = pg.handler( width, height, title="cofffee Shop Data")
# main = go.Grapher(handler, (1700, 1000))

# thick_line = m.line(
#         color=(255, 0, 0),
#         stroke=5
#     )

# area = g.area(main, data, "count()", "Marketing", "Product Type",
#     domain=m.domain(
#         pos=(100, 550),
#         size=( 1200, 300 )),
#     line=thick_line,
#     point=m.point(
#         color=(0, 0, 0),
#         shape=3
#     ),
#     title=m.text(
#         fontSize=25,
#         text="Quantity of Marketing Campaigns for Various Beverages",
#     ),
#     value_axis=ax.axis(
#         line=thick_line,
#         ticks=thick_line,
#         labels=m.text(
#             color=(255, 0, 0),
#             fontSize=10
#         ),
#     ),
#     pallett=active_pallett,
# )


# main.graphs = [ area ]
# main.handler.screen.fill( active_pallett.back_RGB )
# main.render()

# handler.start()
