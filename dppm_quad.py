# -*- coding: utf-8 -*-
"""DPPM_quad.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15HaR_WcIcUCAB0VJs1wu0o4Pxte5yUy2
"""

import math
import copy
import numpy as np
from scipy.optimize import minimize
import scipy.sparse.linalg as sparlg
import matplotlib.pyplot as plt
from numpy import inf

#gradient of function f
def gradient_f(x, epsilon = 1.0e-6):
  grad = np.zeros(dim)
  for i in range(dim):
    next = x.copy()
    next[i] = next[i] + epsilon
    grad[i] = (f(next) - f(x))/epsilon
  return grad


# derivative of function f on the direction p at x_bar 
def derivativef(epsilon = 1.0e-8):
  return (f(bar_x + bar_p * epsilon) - f(bar_x))/epsilon

# function f on the direction p_bar at x_bar
def directionf(w):
  return f(bar_x + w*bar_p)

#golden section method from Wiki
gr = (math.sqrt(5) + 1) / 2

def gsm(f, a, b, tol=1e-8):
    c = b - (b - a) / gr
    d = a + (b - a) / gr
    while abs(b - a) > tol:
        if f(c) < f(d):
            b = d
        else:
            a = c

        c = b - (b - a) / gr
        d = a + (b - a) / gr

    return (b + a) / 2


# |w|**2 / (2*t) + f(bar_x + w*bar_p)
def wf(w):
  return w**2 /(2.0*t) + directionf(w)

def execpy( ):
# *********************************
#   name: execpy
#   type: function
#   thxto: hjinn
# *********************************
  RetVal = dict()
  
  # ********************************
  # initial setup
  RetVal['EXPr'] = EXPinit() 
  # ********************************
  # experiments
  RetVal['exe01'] = exec01(RetVal['EXPr'])
  # ********************************
  # output
  watch_EXP(RetVal)
  
  # return RetVal

def EXPinit( ):
# *********************************
#   name: execpy
#   type: function
#   thxto: hjinn
# *********************************
  RetVal = 0
  EXp = dict()

  # set the matrix Mat_t
  global dim; dim = 500
  a = 270*np.random.rand(dim)+ 30*np.ones(dim)
  global Mat_t; Mat_t = np.diag(a)
  global f; f = lambda x : 0.5 * (x @ (Mat_t @ x))

  int_bar_x = 30*np.random.rand(dim) + 10*np.ones(dim)
  print('initial bar_x is %s' % int_bar_x)
  int_bar_p = np.zeros(dim)
  int_bar_p[0] = -1


  EXp['iteration'] =  2000
  EXp['Lambda'] = 0.1
  EXp['dim'] = dim
  EXp['beta1'] = 0
  EXp['Mat_t'] = Mat_t
  EXp['min_egv'] = np.linalg.eigvalsh(Mat_t)[0]
  EXp['bar_x'] = 1*int_bar_x
  EXp['bar_p'] = 1*int_bar_p
  EXp['num_seg'] = 1000
  EXp['iterStop'] = 1.0e-5

  output_lst = dict()
  output_lst['iteration'] = np.array([])
  output_lst['Mat_t_norm'] = np.array([])
  output_lst['error'] = np.array([])
  output_lst['it_ratio'] = np.array([])

  EXp['output_lst'] = output_lst

  return EXp

def exec01(pEXPr):
# ****************************
#    name: exec01(gradient method)
#    type: function
#    thxto: hMY
# ****************************

  # set initial parameters
  RetVal = 0
  d = 0

  EXPr = copy.deepcopy(pEXPr)
  exp_lst = EXPr['output_lst'] # output

  beta = EXPr['beta1']  # setting the meomentum weight
  dim = EXPr["dim"]
  
  global bar_x; bar_x = 1*EXPr['bar_x']
  global bar_p; bar_p = 1*EXPr['bar_p']

  pre_bar_p = np.zeros(EXPr['dim'])
  v = 2*np.linalg.norm(bar_x)


  #**********************************************************
  grLstApd = lambda pTagName,pVal : np.append(exp_lst[pTagName], np.array([pVal]))
  #Loop: iteration on bar_x
  for i in range(EXPr['iteration']):

  # save information in each iterations
    TagN = 'error'; exp_lst[TagN] = grLstApd(TagN, f(bar_x))
    TagN = 'Mat_t_norm'; exp_lst[TagN] = grLstApd(TagN, 2*f(bar_x))
    
    if (i % dim) == 0 and (i > 0):
      TagN = 'iteration'; exp_lst[TagN] = grLstApd(TagN,i)
      TagN = 'it_ratio'; exp_lst[TagN] = grLstApd(TagN,(exp_lst['Mat_t_norm'][i] / exp_lst['Mat_t_norm'][(i - dim)]))

  # normalize direction bar_p and consider the momentum
    bar_p = beta * pre_bar_p + (1 - beta) * bar_p #compute i-th momentum and decide the direction
    pre_bar_p = bar_p
    bar_p = bar_p / np.linalg.norm(bar_p) #normalize the momentum
    EXPr['bar_p'] = bar_p

  # compute stepsize
    global t; t = EXPr['Lambda']
    minw = gsm(wf, 0, v)

  # update next iteration point bar_x
    bar_x = bar_x + minw * bar_p

  # update direction p
    d = (d + 1) % dim
    bar_p = np.zeros(dim)
    bar_p[d] = -1
    if (bar_p@(Mat_t @ bar_x)) > 0:
      bar_p = -1.0 * bar_p

  # show iinformation every 10 step
    if i%10 == 0:
      print("%s-th" % i, "error of f is %s" % f(bar_x))
      print(" ")
  # terminal condition
    if np.linalg.norm(bar_x, ord = inf) < EXPr['iterStop']:
        break
  

  #return RetVal
  return exp_lst

def watch_EXP(pEXPr):
#-----------------------------
#    name: watch_EXP(show the picture)
#    type: function
#    thxto: JMY
#------------------------------
  plt.xlabel("Iteration")
  plt.ylabel("Error")

  #set a test line
  # x = np.arange(0,3000)
  # y = 1.0 / (1.0 + EXPr['Lambda'] * EXPr['min_egv']) + 0*x

  if 'exe01' in pEXPr:
    exec01 = pEXPr['exe01']
    plt.scatter(exec01['iteration'], exec01['it_ratio'])


  #set the scale
  plt.ylim([0, 1])
  plt.xlim([0, pEXPr['EXPr']['iteration']])

  values = []
  for i in range(int(pEXPr['EXPr']['iteration']/ dim)):
    values.append("%s*dim" % (i+1))
    
  plt.xticks(exec01['iteration'], values)
  plt.show()

execpy()