import pandas as pd
import random
import numpy as np
import math

import coffee.color as c
import coffee.axis as ax
import coffee.palletts as p
import coffee.graph_props as m


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

        self.value_axis = ax.Axis(self, [self.__min__, self.__max__], self.dir)
        self.series_axis = ax.Axis(
            self, self.return_series_names(), abs(self.dir - 1))

        self.pallett = pallett

        self.domain = domain
        self.domain.__reinit__(self)
        self.point = self.__return_default_point__(point)
        self.point.__reinit__(self)

        self.title = title

    def __return_default_point__(self, point):
        if point == -1:
            return m.point(self.pallett.prim_RGB)
        else:
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

    def return_series_names(self):
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
        self.graph.handler.render_text(self.title, (self.pos[0] + (
            self.size[0] / 2),  self.pos[1] + (self.size[1])), self.pallett.text_RGB, 20)

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
