from optparse import Values
import pygame
import pandas as pd
import numpy as np
import sys

import pyg as pg

import color as c
import palletts as p

import graphers as g
import grapher as go
import graph_props as m
import axis as ax
import accessors as a

xls = pd.ExcelFile( a.coffee )
data = pd.read_excel(xls, "Coffee Chain")

width = 1700
height = 900

active_pallett = p.planetary_punch

handler = pg.handler(width, height, title="Coffee Shop Data")
main = go.Grapher(handler, (1700, 1000))


line = m.line(
    stroke=5)
labels = labels = m.text(
    font=a.fetch,
    fontSize=10)
axis = ax.axis(
    line=line,
    ticks=line,
    labels=labels)

marketing = g.area(main, data, "count()", "Marketing", "Product Type",
                   domain=m.domain(
                       pos=(100, 50),
                       size=(width / 4, height - 100)),
                   line=line,
                   title=m.text(
                       font=a.lulo,
                       fontSize=10,
                       text="Quantity of Marketing Campaigns for Various Beverages"),
                   value_axis=axis,
                   series_axis=axis,
                   pallett=active_pallett).point.update_visibility(False)


sales = g.area(main, data, "count()", "Sales", "Product Type",
               domain=m.domain(
                   pos=(200 + width / 4, 50),
                   size=(width / 4, height - 100)),
               point=m.point(
                   stroke=2,
                   radius=7),
               title=m.text(
                   fontSize=15,
                   text="Sales of Various Beverages ($)"),
               pallett=active_pallett)


axis1 = ax.axis(
    line=m.line(stroke=0))
axis2 = ax.axis(
    ticks=m.line(stroke=0))

expenses = g.area(main, data, "count()", "Total Expenses", "Product Type",
                  domain=m.domain(
                      pos=(350 + width / 2, 50),
                      size=(width / 4, height - 100)),
                  title=m.text(
                      fontSize=20,
                      text="Expenses for Various Beverages ($)"),
                  value_axis=axis1,
                  series_axis=axis2,
                  pallett=active_pallett).point.update_visibility(False)


main.graphs = [marketing, sales, expenses]
main.handler.screen.fill(active_pallett.back_RGB)
main.render()


handler.start()
