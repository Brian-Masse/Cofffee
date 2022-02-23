from cProfile import label
import pandas as pd
import random
import numpy as np
import math
import b_grapher.color as c



prim = c.color(190, 232, 194)
second = c.color( 209, 255, 252 )

grad = prim.return_color_grad(second, 100)

back = c.color( 255, 255, 255)
text = c.color(73, 89, 84)

default = c.pallet(grad, prim, second, back, back, text)



def round_dig(num, dig):
    num = float(num)
    num = num * (math.pow( 10, dig ))
    num = round(num)
    return num / ( math.pow(10, dig) )

class Axis:
    def __init__( self, chart, series, dir, interval=-1 ):
        self.chart = chart
        self.interval = interval
        self.series = series
        self.dir = dir
        self.rendering = True

        self.__series_type__ = self.return_series_type()

        if interval == -1 and (self.__series_type__ == "int" or self.__series_type__ == "float"):
            self.interval = self.return_auto_interval()
    
    def return_series_type(self):
        string = str(self.series[0])
        string = string.lstrip("-")
        if string.isdigit():
            return "float"
    
    def return_auto_interval(self):
        return self.chart.size[0] / (self.series[-1] - self.series[0])

    def render(self):
        if self.rendering:
            # domain
        
            origin  = ( self.chart.pos[0] - 10, self.chart.pos[1] - 10  )
            x = math.cos(self.dir * (math.pi / 2))
            y = math.sin(self.dir * (math.pi / 2))
            end     = ( origin[0] + (self.chart.size[0] + 10 ) * x, origin[1] + (self.chart.size[1] + 10 ) * y )
            self.chart.graph.handler.render_line( origin, end, self.chart.pallett.text_RGB  )

            # labels

            if self.__series_type__ == "int" or self.__series_type__ == "float":
                spacing =  ((self.series[-1] - self.series[0]) / self.chart.size[self.dir]) * 100
                print(spacing)
                pos = int(self.series[0])
                
                while pos <= self.series[-1]:
                    label_pos = ( origin[0] + (( (pos - self.chart.min) * self.interval ) * x) - ( 10 * y ), origin[1] + (( (pos - self.chart.min) * self.interval ) * y) - ( 10 * x ) )
                    self.chart.graph.handler.render_text( str(round_dig( pos, 3 )), label_pos, self.chart.pallett.text_RGB, 10  )
                    pos += spacing

            else:
                spacing = self.chart.size[self.dir] / len(self.series)
                for i, label in enumerate(self.series):
                    label_pos = ( origin[0] + (( i * spacing ) * x) - ( 10 * y ), origin[1] + (( i * spacing ) * y) - ( 10 * x ) )
                    self.chart.graph.handler.render_text( label, label_pos, self.chart.pallett.text_RGB, 10, "right" )





class distribution:
    def __init__(self, graph, data, x, series, size=(500, 500), pos=(100, 100), title="", pallett=default):
        self.graph = graph
        self.data = data
        self.x = data[x]

        self.min = self.sort_df( self.x )[0]

        self.series = data[series]
        self.unique_series = self.unique_series(self.series)
        self.series_data = self.create_series()

        self.pos = pos
        self.size = size
        
        self.x_axis = Axis( self, self.sort_df( self.x ), 0)
        self.y_axis = Axis( self, self.return_series_names(), 1 )

        self.title = title

        self.pallett = pallett


    def sort_df( self, df ):
        rotated = np.rot90(df.to_numpy())
        
        return np.sort( rotated[np.logical_not(np.isnan(rotated))] )

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

        for series in self.unique_series:
            for column in self.x:
                rows = self.series == series
                selection = self.data.loc[rows, column]
                series_obj = self.Series(self, "" + series + ", " + column, selection, index)
                returning.append(series_obj)
                index += 1

        return returning

    def render(self):
        for series in self.series_data:
            series.render()
        
        self.x_axis.render()
        self.y_axis.render()

        self.graph.handler.render_text(self.title, ( self.pos[0] + ( self.size[0] / 2 ),  self.pos[1] + ( self.size[1] ) ), self.pallett.text_RGB, 20)

    class Series:
        def __init__(self, parent, name, x, index):
            self.parent = parent
            self.name = name
            self.x = np.sort(x.to_numpy())
            self.index = index

        def render(self):
    
            y_space = (self.parent.size[1] / len(self.parent.series_data))

            steps = 1 / len(self.parent.unique_series)

            for x in self.x:

                y = (self.index * y_space) + random.uniform(-y_space / 5,  y_space / 5)

                x = ((x - self.parent.min ) * self.parent.x_axis.interval ) + self.parent.pos[0]
                y = y + self.parent.pos[1]


                color = self.parent.pallett.primary_color.return_color_between( self.parent.pallett.secondary_color, steps * self.index ).return_color_in("RGB")

                if not np.isnan(x):
                    self.parent.graph.handler.render_point( (x, y), color, 2 )

