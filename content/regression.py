import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from numpy import linspace

# reduce(lambda x,y: x+y,liste) = sum(liste)
# Beide summiert die an Liste gehörige Elemente nacheinander.

# Mittelwert berechnen
# Bei der Mittelwertberechnung tritt im Gegensatz zu R bei Outputs eine Differenz auf, weil R Programmierungssprache berechnet den Mittelwert anders als hier gemacht wurde.
def getmw(l):
    return sum(l) / len(l)


# Varianz
def var(l):
    l = list(map(lambda x: (x - getmw(l)) ** 2, l))
    return sum(l) / (len(l) - 1)


# Kovarianz
def cov(la, lb):
    return sum(list(map(lambda a, b: (a - getmw(la)) * (b - getmw(lb)), la, lb))) / (len(la) - 1)


# Regression Oberklasse, die uns ermöglicht, darin gesteckte Funktionen von Regression zu benutzen.
class Regression:
    def __init__(self,master, x, y, index: int, title=None, titlex="Titelx", titley="Titely"):
        self.master = master
        self.x = x
        self.x=list(map(float,self.x))
        self.y = y
        self.y=list(map(float,self.y))
        self.title = title
        self.titlex = titlex
        self.titley = titley
        self.index = index

        self.__kontroll(self.x, self.y)
        self.b1 = cov(self.x, self.y) / var(self.x)
        self.b0 = getmw(self.y) - (self.b1 * getmw(self.x))

    # Innere Funktion, die standardmäßige Kontrolle für die Benutzung der richtigen Daten durchführt.
    def __kontroll(self, x, y):
        if (not isinstance(x, list) and not all(isinstance(i, str) for i in x)) and (
                not isinstance(y, list) and not all(isinstance(i, str) for i in y)):
            raise TypeError()

        elif len(x) != len(y):
            raise IndexError()

    # Auf Regressiongsgerade liegenden Wert von parameterx finden
    def get_wert(self, parameterx):
        return self.b0 + (self.b1 * parameterx)

    # Alles Graphisch darstellen, man müsste am Ende diese Funkiton benutzen, um es zu visualisieren.
    def zeichnen(self):
        x = linspace(min(self.x), max(self.x))
        y = self.b0 + (self.b1 * x)

        fig = plt.figure(figsize=(7, 7), dpi=100)
        self.canvas = FigureCanvasTkAgg(figure=fig, master=self.master.master.rightframe.grafikframe)
        NavigationToolbar2Tk(self.canvas)
        axes = fig.add_axes([0.1, 0.1, 0.85, 0.85])
        a1 = axes.scatter(self.x, self.y)
        a2 = axes.plot(x, y, color="red")

        if isinstance(self.titlex, str) and isinstance(self.titley, str):
            a4 = axes.set_xlabel(self.titlex)
            a5 = axes.set_ylabel(self.titley)

        axes.legend(["Covarianz: "+str(cov(self.x,self.y))])
        setattr(self.master,"grafik"+str(self.index),self.canvas.get_tk_widget())
        getattr(self.master,"grafik"+str(self.index)).pack(side='top',expand=1)
    
