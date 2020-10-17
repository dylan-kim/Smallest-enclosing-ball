# coding=utf-8
# Author KIM Dylan - 2017

"""Interface using Tkinter and showing a naive approach for the smallest enclosing circle problem."""

import random

from math import sqrt
from math import acos
from math import sin
from math import pi

from tkinter import Tk
from tkinter import Canvas
from tkinter import Frame
from tkinter import Scale
from tkinter import Button
from tkinter import ALL

dots = []
distances = []
widgets = []
colors = ["red", "orange", "green", "blue", "violet"]

fen = Tk()
fen.title('Project : The smallest enclosing ball')
cv = Canvas(fen, width=750, height=600, bg='snow')
cv.pack(side = 'left')
commande = Frame(fen, width=390, height=560)
commande.pack()

# Initialize scroll widget.
scale = Scale(commande, orient = 'horizontal', from_ = 3, to = 100, resolution = 1, length = 350, label = 'Number of dots')
scale.grid(row = 1,column = 1)

def create_points() :
    """Create n random dots on the canvas."""
    global n, dots
    n = scale.get()
    dots = [(random.randint(220,500), random.randint(170,400)) for k in range(n)]
    for (x,y) in dots:
        cv.create_rectangle(x, y, x+3, y+3, fill ='blue')

def triangle(liste, a, b, c, x_dot_1, x_dot_2, x_dot_3, y_dot_1, y_dot_2, y_dot_3) :
    # Al-Kashi Theorem.
    angle_radian_u = acos((-a**2+b**2+c**2)/(2*b*c))
    angle_degre_u = int((angle_radian_u*180)/pi)
    angle_radian_v = acos((-b**2+a**2+c**2)/(2*a*c))
    angle_degre_v = int((angle_radian_v*180)/pi)
    angle_radian_w = acos((-c**2+a**2+b**2)/(2*a*b))
    angle_degre_w = int((angle_radian_w*180)/pi)

    # Coefficient of barycenter.
    m = sin(2*angle_radian_u) 
    n = sin(2*angle_radian_v)
    p = sin(2*angle_radian_w)
    s = m+n+p
    m1 = m/s
    n1 = n/s
    p1 = p/s
    r = a/2
    distances_barycentre = []
    # Acute triangle : 3 acutes angles
    if angle_degre_u < 90 and angle_degre_v < 90 and angle_degre_w < 90: 
        x_barycentre = (p1*x_dot_1) + (n1*x_dot_2) + (m1*x_dot_3)
        y_barycentre = (p1*y_dot_1) + (n1*y_dot_2) + (m1*y_dot_3)
        cv.create_rectangle(x_barycentre, y_barycentre, x_barycentre+3, y_barycentre+3, fill = 'red')
        r = sqrt((x_barycentre-x_dot_1)**2 + (y_barycentre-y_dot_1)**2)
        for l in range (0, len(liste)):
            x_dot_4 = liste[l][0]
            y_dot_4 = liste[l][1]
            distance_barycentre_dot_4 = sqrt((x_barycentre-x_dot_4)**2 + (y_barycentre-y_dot_4)**2)
            distances_barycentre.append(distance_barycentre_dot_4)
        if max(distances_barycentre) > r:
            radius = max(distances_barycentre)
            cv.create_oval(x_barycentre-radius, y_barycentre-radius, x_barycentre+radius, y_barycentre+radius, outline = 'green', width = 1)
        else :
            cv.create_oval(x_barycentre-r, y_barycentre-r, x_barycentre+r, y_barycentre+r, outline = 'purple', width = 1) 

    # Obtuse triangle
    else :
        cv.create_oval(((x_dot_1+x_dot_2)/2)-r, ((y_dot_1+y_dot_2)/2)-r, ((x_dot_1+x_dot_2)/2)+r, ((y_dot_1+y_dot_2)/2)+r, outline = 'green', width=1)

def create_triangle(dot_1, dot_2, dot_3):
    """Create 3 segments composing the triangle."""
    cv.create_line(dot_1[0], dot_1[1], dot_2[0], dot_2[1], fill = 'orange')
    cv.create_line(dot_2[0], dot_2[1], dot_3[0], dot_3[1], fill = 'orange')
    cv.create_line(dot_1[0], dot_1[1], dot_3[0], dot_3[1], fill = 'orange')

def create_diameter(dot_1, dot_2):
    """Create 1 segment for the diameter."""
    cv.create_line(dot_1[0], dot_1[1], dot_2[0], dot_2[1], fill = 'blue')

def create_circle(x_center, y_center, radius):
    """Create a circle made up with 2 dots and the radius."""
    cv.create_oval(x_center-radius, y_center-radius, x_center+radius, y_center+radius, outline = 'blue', width = 1)

def clean_list(): 
    """Clean global lists."""
    distances[:] = []
    dots[:] = []

def reinitialize_widget():
    """Reinitialise the widget scale."""
    scale.set(0)
    for widget in widgets:
        widget.pack_forget()

def clean_all():
    """Clean every list and reinitialise the widget scale."""
    cv.delete(ALL)
    clean_list()
    reinitialize_widget()

# Determination si le resultat est pair ou triplet (cercle de diamètre de 2 points, ou d'un cercle formé par un triangle)
def main():
    cv.delete(ALL)
    create_points()
    segments = []
    probable_third_dots = []
    have_third_dot = False

    for (x1,y1) in dots:
        for (x2,y2) in dots:
            distance = sqrt((x1-x2)**2 + (y1-y2)**2)
            distances.append(distance)

            # segment contains all the distance between 2 dots, and the coord of the 2 dots.
            segment = distance, (x1,y1), (x2,y2)
            segments.append(segment)

    # Get the max distance, and the 2 dots composing it.
    max_distance = segments[0][0]
    for segment in segments:
        distance_segment = segment[0]
        if distance_segment > max_distance:
            max_distance = distance_segment
            dot_1 = (segment[1][0], segment[1][1])
            dot_2 = (segment[2][0], segment[2][1])
            x_center = (segment[1][0] + segment[2][0]) / 2
            y_center = (segment[1][1] + segment[2][1]) / 2
            radius = segment[0] / 2

    # Check if there is a 3rd dot outside the radius.
    for (x,y) in dots:
        distance_center_dot = sqrt((x_center-x)**2 + (y_center-y)**2)
        if distance_center_dot > radius:
            probable_third_dot = distance_center_dot, (x,y)
            probable_third_dots.append(probable_third_dot)
            have_third_dot = True

    if have_third_dot == True:
        max_distance = probable_third_dots[0][0]
        dot_3 = (probable_third_dots[0][1][0], probable_third_dots[0][1][1])

        for probable_third_dot in probable_third_dots:
            if probable_third_dot[0] > max_distance:
                max_distance = probable_third_dot[0]
                dot_3 = (probable_third_dot[1][0], probable_third_dot[1][1])

        a = int(sqrt((dot_1[0]-dot_2[0])**2 + (dot_1[1]-dot_2[1])**2))
        b = int(sqrt((dot_3[0]-dot_1[0])**2 + (dot_3[1]-dot_1[1])**2))
        c = int(sqrt((dot_2[0]-dot_3[0])**2 + (dot_2[1]-dot_3[1])**2))

        create_triangle(dot_1, dot_2, dot_3)
        triangle(dots, a, b, c, dot_1[0], dot_2[0], dot_3[0], dot_1[1], dot_2[1], dot_3[1])

    else : 
        create_diameter(dot_1, dot_2) 
        create_circle(x_center, y_center, radius)
        
    clean_list()

validate = Button(commande, text = 'Enclosing ball with n dots', command = main)
validate.grid(row=3, column=1)

quit = Button(fen, text = 'Quit', command = fen.destroy)
quit.pack(side = 'bottom')

clean = Button(fen, text = 'Clean', command = clean_all)
clean.pack(side = 'bottom')

fen.mainloop()