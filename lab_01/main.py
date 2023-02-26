import matplotlib.pyplot as plt
import math
import pylab
from tkinter import *
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

root = Tk()
root.title("graph drawer")
root.geometry("1000x800")


class Signal:
   def get(self, x):
      pass
   def sinc(self, x):
      if x == 0:
         return 0
      return math.sin(x) / x      
   def initial(self, limits, h):
      t = limits[0]
      y = []
      x = []
      while t <= limits[1]:
         y.append(self.get(t))
         x.append(t)
         t += h
      return (x, y)
   def discretization(self, limits, h):
      t = limits[0]
      y = []
      x = []
      while t <= limits[1]:
         y.append(self.get(t))
         x.append(t)
         t += h
      return (x, y, h)
   def recovery(self, discrets, h):
      dix = discrets[0]
      diy = discrets[1]
      dh = discrets[2]

      y = []
      x = []
      t = limits[0]
      while t <= limits[1]:
         x.append(t)
         val = 0
         for i in range(len(dix)):
            val += diy[i] * self.sinc(math.pi / dh * (t - dix[i]))
         y.append(val)
         t += h
      return (x, y)
            
      
class RectSignal(Signal):
   def __init__(self, params):
      self.l = params[0]
   def get(self, x):
      return 1 if abs(x / l) <= 1 else 0
class GaussSignal(Signal):
   def __init__(self, params):
      self.sigma = params[0]
      self.a = params[1]
   def get(self, x):
      return a * math.exp(- x * x / sigma / sigma)

def draw_graph(plots, names):
   i = 0
   for plot in plots:
      pylab.plot(plot[0], plot[1], label = names[i])
      i += 1
   pylab.legend()

def draw():
   h = 0
   try:
      h = float(entry_h.get())
   except (Exception):
      print("error read")

   names = ["initial", "discrete", "recovered"]

   
   fig1 = pylab.figure(1, figsize=(5, 3.5))
   fig1.clf()
   pylab.subplot(1, 1, 1)
   disG = gs.discretization(limits, h)
   gauss_plots = [gs.initial(limits, 0.01), disG , gs.recovery(disG, 0.01)]
   draw_graph(gauss_plots, names)
   pylab.title("gauss signal")

   canvas = FigureCanvasTkAgg(fig1, master = root)  
   canvas.draw()
   canvas.get_tk_widget().grid(row=2, column=0, columnspan=20)

   fig2 = pylab.figure(2, figsize=(5, 3.5))
   fig2.clf()
   pylab.subplot(1, 1, 1)
   disR = rs.discretization(limits, h)
   rect_plots = [rs.initial(limits, 0.01), disR, rs.recovery(disR, 0.01)]
   draw_graph(rect_plots, names)
   pylab.title("rect signal")

   canvas = FigureCanvasTkAgg(fig2, master = root)  
   canvas.draw()
   canvas.get_tk_widget().grid(row=3, column=0,columnspan=20)
   


l = 2
sigma = 1.5
a = 1

rs = RectSignal([l])
gs = GaussSignal([sigma, a])

##n = int(input('Input number of samples: '))
##h = float(input('Input sample step: '))

t_max = 4 # h * (n - 1) / 2
limits = [-t_max, t_max]

Label(text="step: ").grid(row=0, column=0)
entry_h = Entry(root)
entry_h.grid(row=0, column = 1)

btnDraw = Button(root, text="draw", command=draw)
btnDraw.grid(row=1, column = 0)

root.mainloop()



##% Исходные сигналы
##x = -t_max:0.005:t_max;
##gauss_ref = exp(-(x/sigma).^2);
##rect_ref = zeros(size(x));
##rect_ref(abs(x) - tt < 0) = 1;
##
##% Восстановленные сигналы
##gauss_restored = zeros(1, length(x));
##rect_restored = zeros(1, length(x));
##for i=1:length(x)
##   for j = 1:n
##       gauss_restored(i) = gauss_restored(i) + gauss_discrete(j) * sin((x(i)-t(j))/dt * pi) / ((x(i)-t(j))/dt * pi);
##       rect_restored(i) = rect_restored(i) + rect_discrete(j) * sin((x(i)-t(j))/dt * pi) / ((x(i)-t(j))/dt * pi);
##   end
##end
##
##figure;
##
##subplot(2,1,1);
##title('Прямоугольный импульс');
##hold on;
##grid on;
##plot(x, rect_ref, 'k');
##plot(x, rect_restored, 'b');
##plot(t, rect_discrete, '.m');
##legend('Исходная', 'Восстановленная', 'Дискретная');
##
##subplot(2,1,2);
##title('Гауссовский фильтр');
##hold on;
##grid on;
##plot(x, gauss_ref, 'k');
##plot(x, gauss_restored, 'b');
##plot(t, gauss_discrete, '.m');
##legend('Исходная', 'Восстановленная', 'Дискретная');
