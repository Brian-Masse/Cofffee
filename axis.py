import math


def round_dig(num, dig):
    num = float(num)
    num = num * (math.pow( 10, dig ))
    num = round(num)
    return num / ( math.pow(10, dig) )

class Axis:
    def __init__( self, parent, series, dir, interval=-1, min=0 ):
        self.parent = parent
        self.interval = interval
        self.series = series

        self.dir = dir
        self.min = min

        self.rendering = True

        self.__series_type__ = self.__return_series_type__()

        # the interval is the steps that a value must take to reach its end by the end of some space
        if interval == -1 and (self.__series_type__ == "int" or self.__series_type__ == "float"):
            self.interval = self.__return_auto_interval__()
    
    def __return_series_type__(self):
        string = str(self.series[0])
        string = string.lstrip("-")
        if string.isdigit():
            return "float"
    
    def __return_auto_interval__(self):
        return self.parent.size[self.parent.dir] / (self.series[-1] - self.series[0])

    # for aligning axis labels 
    def __return_alignment__(self):
        if self.dir == 0: return "center"
        else: return "right"



    def render(self):
        if self.rendering:
            # domain
        
            origin  = ( self.parent.pos[0] - 10, self.parent.pos[1] - 10  )
            x = math.cos(self.dir * (math.pi / 2))
            y = math.sin(self.dir * (math.pi / 2))
            end     = ( origin[0] + (self.parent.size[0] + 10 ) * x, origin[1] + (self.parent.size[1] + 10 ) * y )
            self.parent.graph.handler.render_line( origin, end, self.parent.pallett.text_RGB  )

            # labels

            if self.__series_type__ == "int" or self.__series_type__ == "float":
                
                spacing =  ((self.series[-1] - self.series[0]) / self.parent.size[self.dir]) * 50
                pos = int(self.series[0])
                # render all numbers
                while pos <= self.series[-1]:
                    prim = origin[self.dir] + ( (pos - self.min) * self.interval ) 
                    second = origin[abs(self.dir - 1)] - 10
                    
                    label_pos = (( prim * x) + ( second * y ), ( prim * y) + ( second * x ))

                    self.parent.graph.handler.render_text( str(round_dig( pos, 1 )), label_pos, self.parent.pallett.text_RGB, 10, self.__return_alignment__()  )
                    pos += spacing
                
            # render all series
            else:
                spacing = self.parent.size[self.dir] / len(self.series)
                for i, label in enumerate(self.series):
                    label_pos = ( origin[0] + (( i * spacing ) * x) - ( 10 * y ), origin[1] + (( i * spacing ) * y) - ( 10 * x ) )
                    self.parent.graph.handler.render_text( str(label), label_pos, self.parent.pallett.text_RGB, 10, self.__return_alignment__() )


    # USER FUNCTIONS

    def update_visibility(self, vis):
        self.rendering = vis
        return self.parent