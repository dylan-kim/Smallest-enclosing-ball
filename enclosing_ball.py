from math import*
import random
from tkinter import*

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
scale.grid(row=1,column=1)

# Create n random dots on the canvas.
def create_points() :
    global n, dots
    n = scale.get()
    dots = [(random.randint(220,500), random.randint(170,400)) for k in range(n)]
    for (x,y) in dots:
        cv.create_rectangle(x,y, x+3, y+3, fill ='blue')


# !Triplet! Determination et création d'un cerlcle grace au triangle (acutangle ou obtusangle)
def triangle(liste, a, b, c, xmax1, xmax2, xmax3, ymax1, ymax2, ymax3) :
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
    if angle_degre_u < 90 and angle_degre_v < 90 and angle_degre_w < 90 : 
        x_barycentre = (p1*xmax1) + (n1*xmax2) + (m1*xmax3)
        y_barycentre = (p1*ymax1) + (n1*ymax2) + (m1*ymax3)
        cv.create_rectangle(x_barycentre, y_barycentre, y_barycentre+3, y_barycentre+3, fill = 'red')
        r = sqrt((x_barycentre-xmax1)**2 + (y_barycentre-ymax1)**2)
        for l in range (0, len(liste)) :
            x3 = liste[l][0]
            y3 = liste[l][1]
            d1 = sqrt((x_barycentre-x3)**2 + (y_barycentre-y3)**2)
            distances_barycentre.append(d1)
        if max(distances_barycentre) > r :
            radius = max(distances_barycentre)
            cv.create_oval(x_barycentre-radius, y_barycentre-radius, x_barycentre+radius, y_barycentre+radius, outline = 'green', width = 1)
        else :
            cv.create_oval(x_barycentre-r, y_barycentre-r, x_barycentre+r, y_barycentre+r, outline = 'purple', width = 1) 

    # Obtuse triangle
    else :
        # cv.create_line(xmax1, ymax1, xmax2, ymax2, fill = 'orange')
        cv.create_oval(((xmax1+xmax2)/2)-r, ((ymax1+ymax2)/2)-r, ((xmax1+xmax2)/2)+r, ((ymax1+ymax2)/2)+r, outline = 'green', width=1)

# Determination si le resultat est pair ou triplet (cercle de diamètre de 2 points, ou d'un cercle formé par un triangle)
def main():
    cv.delete(ALL)
    create_points()
    segments = []
    probable_third_dots = []
    have_third_dot = False

    for (x1,y1) in dots :
        for (x2,y2) in dots :
            distance = sqrt((x1-x2)**2 + (y1-y2)**2)
            distances.append(distance)

            # segment contains all the distance between 2 dots, and the coord of the 2 dots.
            segment = distance, (x1,y1), (x2,y2)
            segments.append(segment)

    # Get the max distance, and the 2 dots composing it.
    max_distance = segments[0][0]
    for segment in segments :
        distance_segment = segment[0]
        if distance_segment > max_distance:
            max_distance = distance_segment
            dot_1 = (segment[1][0], segment[1][1])
            dot_2 = (segment[2][0], segment[2][1])
            x_center = (segment[1][0] + segment[2][0]) / 2
            y_center = (segment[1][1] + segment[2][1]) / 2
            radius = segment[0] / 2

    # Check if there is a 3rd dot outside the radius.
    for (x,y) in dots :
        distance_center_dot = sqrt((x_center-x)**2 + (y_center-y)**2)
        if distance_center_dot > radius :
            probable_third_dot = distance_center_dot, (x,y)
            probable_third_dots.append(probable_third_dot)
            have_third_dot = True

    if have_third_dot == True :
        max_distance = probable_third_dots[0][0]
        dot_3 = (probable_third_dots[0][1][0], probable_third_dots[0][1][1])

        for probable_third_dot in probable_third_dots :
            if probable_third_dot[0] > max_distance :
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

# Create 3 segments composing the triangle.
def create_triangle(dot_1, dot_2, dot_3) :
    cv.create_line(dot_1[0], dot_1[1], dot_2[0], dot_2[1], fill = 'orange')
    cv.create_line(dot_2[0], dot_2[1], dot_3[0], dot_3[1], fill = 'orange')
    cv.create_line(dot_1[0], dot_1[1], dot_3[0], dot_3[1], fill = 'orange')

# Create 1 segment for the diameter.
def create_diameter(dot_1, dot_2) :
    cv.create_line(dot_1[0], dot_1[1], dot_2[0], dot_2[1], fill = 'blue')

# Create a circle made up with 2 dots and the radius.
def create_circle(x_center, y_center, radius) :
    cv.create_oval(x_center-radius, y_center-radius, x_center+radius, y_center+radius, outline = 'blue', width = 1)

# Clean global lists.
def clean_list() : 
    distances[:] = []
    dots[:] = []

# Reinitialise the widget scale.
def reinitialize_widget() :
    scale.set(0)
    for widget in widgets:
        widget.pack_forget()

# Clean every list and reinitialise the widget scale.
def clean_all():  
    cv.delete(ALL)
    clean_list()
    reinitialize_widget()

validate=Button(commande, text = 'Enclosing ball with n dots', command = main)
validate.grid(row=3, column=1)

quit=Button(fen, text = 'Quit', command = fen.destroy)
quit.pack(side = 'bottom')

clean=Button(fen, text = 'Clean', command = clean_all)
clean.pack(side = 'bottom')

fen.mainloop()