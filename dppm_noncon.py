# -*- coding: utf-8 -*-
"""DPPM_NEW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QI_NXJupP0EDU5THWVtpEk_Ffj26RIAg
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

#define function g_0 and its gradient
def g_0(p):
  return 0.5*(np.linalg.norm(p)**2)

def gradient_g_0(p, epsilon = 1.0e-6):
  grad = np.zeros(dim)
  for i in range(dim):
    next = p.copy()
    next[i] = next[i] + epsilon
    grad[i] = (g_0(next) - g_0(p))/epsilon
  return grad

#define function g_1 and its gradient
def g_1(p, delta=1.0e-4):
  return f(bar_x + p) + delta - f(bar_x) - gradient_f(bar_x)@p

def gradient_g_1(p, epsilon = 1.0e-6):
  grad = np.zeros(dim)
  for i in range(dim):
    next = p.copy()
    next[i] = next[i] + epsilon
    grad[i] = (g_1(next) - g_1(p))/epsilon
  return grad

#define function g_2 and its gradient
def g_2(p):
  return gradient_f(bar_x)@p

def gradient_g_2(p, epsilon = 1.0e-6):
  grad = np.zeros(dim)
  for i in range(dim):
    next = p.copy()
    next[i] = next[i] + epsilon
    grad[i] = (g_2(next) - g_2(p))/epsilon
  return grad

#define objective function
def rosen(p):
  return gradient_g_0(p_0)@(p-p_0) + mu/2.0 * np.linalg.norm(p-p_0)**2

#define constraints
ineq_cons = {'type': 'ineq',
             'fun' : lambda p: np.array([-g_1(p_0) - gradient_g_1(p_0)@(p - p_0),
                             -g_2(p_0) - gradient_g_2(p_0)@(p - p_0)]),
             'jac' : lambda p: np.array([ [-gradient_g_1(p_0)[0], -gradient_g_1(p_0)[1], -gradient_g_1(p_0)[2]],[-gradient_g_2(p_0)[0], -gradient_g_2(p_0)[1], -gradient_g_2(p_0)[2]] ])}
eq_cons = {'type': 'eq',
           'fun' : lambda p: np.array([0]),
           'jac' : lambda p: np.array([0, 0, 0])}
def rosen_der(p):
  return (gradient_g_0(p_0) + mu*(p-p_0)).reshape(1, 3)

def find_direction(p_0):
  res = minimize(rosen, p_0, method='SLSQP', jac=rosen_der, constraints=[ineq_cons], options={'ftol': 1e-9, 'disp': True}, bounds=None)
  return res.x

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
  # RetVal['exe02'] = exec02(RetVal['EXPr'])
  # RetVal['exe03'] = exec02(RetVal['EXPr'])
  # ********************************
  # output
  watch_EXP(RetVal)
  
  return RetVal

f = lambda x : np.linalg.norm(x)**2 + 4 * np.sin(x[2])**2

def EXPinit( ):
# *********************************
#   name: execpy
#   type: function
#   thxto: hjinn
# *********************************
  RetVal = 0
  EXp = dict()

  global dim; dim = 3
  # int_bar_x = 30*np.random.rand(dim) + 10*np.ones(dim)
  int_bar_x = [10., 10., 10.]
  print('initial bar_x is %s' % int_bar_x)

  EXp['iteration'] =  1500
  EXp['Lambda'] = 0.1
  EXp['mu'] = 1000
  EXp['dim'] = dim
  EXp['beta1'] = 0
  EXp['beta2'] = 0.6
  EXp['beta3'] = 0
  # EXp['Mat_t'] = Mat_t
  # EXp['min_egv'] = np.linalg.eigvalsh(Mat_t)[0]
  EXp['bar_x'] = 1*int_bar_x
  EXp['bar_p'] = -gradient_f(int_bar_x)
  EXp['num_seg'] = 1000
  EXp['tryagain'] = 10
  EXp['iterStop'] = 1.0e-5

  output_lst = dict()
  output_lst['iteration'] = np.array([])
  output_lst['error'] = np.array([])
  # output_lst['it_norm'] = np.array([1.0])
  # output_lst['it_ratio'] = np.array([])

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

  EXPr = copy.deepcopy(pEXPr)
  exp_lst = EXPr['output_lst'] # output

  beta = EXPr['beta1']  # setting the meomentum weight
  dim = EXPr["dim"]
  global mu; mu = EXPr['mu']
  
  global bar_x; bar_x = 1*EXPr['bar_x']
  global bar_p; bar_p = 1*EXPr['bar_p']
  pre_bar_p = np.zeros(EXPr['dim'])
  v = 2*np.linalg.norm(bar_x)

  # n2_bar_x1 = 1
  # n2_bar_x0 = exp_lst['it_norm'][0] 
  #**********************************************************
  grLstApd = lambda pTagName,pVal : np.append(exp_lst[pTagName], np.array([pVal]))
  #Loop: iteration on bar_x
  for i in range(EXPr['iteration']):

  # save information in each iterations
    # n2_bar_x1 = np.linalg.norm(bar_x)
    TagN = 'iteration'; exp_lst[TagN] = grLstApd(TagN,i)
    TagN = 'error'; exp_lst[TagN] = grLstApd(TagN,f(bar_x))
    # TagN = 'it_norm'; exp_lst[TagN] = grLstApd(TagN,n2_bar_x1)
    # TagN = 'it_ratio'; exp_lst[TagN] = grLstApd(TagN,(n2_bar_x1 / n2_bar_x0))

    # n2_bar_x0 = 1*n2_bar_x1

  # normalize direction bar_p and consider the momentum
    bar_p = beta * pre_bar_p + (1 - beta) * bar_p #compute i-th momentum and decide the direction
    pre_bar_p = bar_p
    bar_p = bar_p / np.linalg.norm(bar_p) #normalize the momentum
    EXPr['bar_p'] = bar_p

  # find convex segement
    num_seg = EXPr['num_seg']
    for k in range(num_seg):
      v = 1/num_seg * k
      a = directionf(1/num_seg * (k+1)) - directionf(1/num_seg * k)
      b = directionf(1/num_seg * (k+2)) - directionf(1/num_seg * (k+1))
      if a > b :
        break
    if v < 0.005:
      v = 0.005
  # compute stepsize
    global t; t = v/ np.linalg.norm(derivativef())
    # t = Lambda
    minw = gsm(wf, 0, v)

  # update next iteration point bar_x
    bar_x = bar_x + minw * bar_p

  # update direction p
    bar_p = -gradient_f(bar_x)


  # show iinformation every 10 step
    if i%10 == 0:
      print("%s-th" % i, "error of f is %s" % f(bar_x))
      print(" ")
  # terminal condition
    if np.linalg.norm(bar_x, ord = inf) < EXPr['iterStop']:
        break
  

  #return RetVal
  return exp_lst

def exec02(pEXPr):
# ****************************
#    name: exec02(momentum method)
#    type: function
#    thxto: hMY
# ****************************

  # set initial parameters
  RetVal = 0

  EXPr = copy.deepcopy(pEXPr)
  exp_lst = EXPr['output_lst'] # output

  beta = EXPr['beta2']  # setting the meomentum weight
  dim = EXPr["dim"]
  global mu; mu = EXPr['mu']

  global bar_x; bar_x = 1*EXPr['bar_x']
  global bar_p; bar_p = 1*EXPr['bar_p']
  pre_bar_p = np.zeros(EXPr['dim'])
  v = 2*np.linalg.norm(bar_x)

  # n2_bar_x1 = 1
  # n2_bar_x0 = exp_lst['it_norm'][0] 
  #**********************************************************
  grLstApd = lambda pTagName,pVal : np.append(exp_lst[pTagName], np.array([pVal]))
  #Loop: iteration on bar_x
  for i in range(EXPr['iteration']):

  # save information in each iterations
    # n2_bar_x1 = np.linalg.norm(bar_x)
    TagN = 'iteration'; exp_lst[TagN] = grLstApd(TagN,i)
    TagN = 'error'; exp_lst[TagN] = grLstApd(TagN,f(bar_x))
    # TagN = 'it_norm'; exp_lst[TagN] = grLstApd(TagN,n2_bar_x1)
    # TagN = 'it_ratio'; exp_lst[TagN] = grLstApd(TagN,(n2_bar_x1 / n2_bar_x0))

    # n2_bar_x0 = 1*n2_bar_x1

  # normalize direction bar_p and consider the momentum
    bar_p = beta * pre_bar_p + (1 - beta) * bar_p #compute i-th momentum and decide the direction
    pre_bar_p = bar_p
    bar_p = bar_p / np.linalg.norm(bar_p) #normalize the momentum
    EXPr['bar_p'] = bar_p

  # find convex segement
    num_seg = EXPr['num_seg']
    for k in range(num_seg):
      v = 1/num_seg * k
      a = directionf(1/num_seg * (k+1)) - directionf(1/num_seg * k)
      b = directionf(1/num_seg * (k+2)) - directionf(1/num_seg * (k+1))
      if a > b :
        break
    if v < 0.005:
      v = 0.005
  
  # compute stepsize
    global t; t = v/ np.linalg.norm(derivativef())
    # t = Lambda
    minw = gsm(wf, 0, v)

  # update next iteration point bar_x
    bar_x = bar_x + minw * bar_p

  # update direction p
    bar_p = -gradient_f(bar_x)

  # show iinformation every 10 step
    if i%10 == 0:
      print("%s-th" % i, "error of f is %s" % f(bar_x))
      print(" ")
  # terminal condition
    if np.linalg.norm(bar_x, ord = inf) < EXPr['iterStop']:
        break
  

  #return RetVal
  return exp_lst

def exec03(pEXPr):
# ****************************
#    name: exec03(DLC direction)
#    type: function
#    thxto: hMY
# ****************************

  # set initial parameters
  RetVal = 0

  EXPr = copy.deepcopy(pEXPr)
  exp_lst = EXPr['output_lst'] # output

  beta = EXPr['beta3']  # setting the meomentum weight
  dim = EXPr["dim"]
  global mu; mu = EXPr['mu']

  global bar_x; bar_x = 1*EXPr['bar_x']
  global bar_p; bar_p = 1*EXPr['bar_p']
  pre_bar_p = np.zeros(EXPr['dim'])
  v = 2*np.linalg.norm(bar_x)

  # n2_bar_x1 = 1
  # n2_bar_x0 = exp_lst['it_norm'][0]

  #**********************************************************
  grLstApd = lambda pTagName,pVal : np.append(exp_lst[pTagName], np.array([pVal]))
  #Loop: iteration on bar_x
  for i in range(EXPr['iteration']):

  # save information in each iterations
    # n2_bar_x1 = np.linalg.norm(bar_x)
    TagN = 'iteration'; exp_lst[TagN] = grLstApd(TagN,i)
    TagN = 'error'; exp_lst[TagN] = grLstApd(TagN,f(bar_x))
    # TagN = 'it_norm'; exp_lst[TagN] = grLstApd(TagN,n2_bar_x1)
    # TagN = 'it_ratio'; exp_lst[TagN] = grLstApd(TagN,(n2_bar_x1 / n2_bar_x0))

    # n2_bar_x0 = 1*n2_bar_x1

  # normalize direction bar_p and consider the momentum
    bar_p = beta * pre_bar_p + (1 - beta) * bar_p #compute i-th momentum and decide the direction
    pre_bar_p = bar_p
    bar_p = bar_p / np.linalg.norm(bar_p) #normalize the momentum
    EXPr['bar_p'] = bar_p

  # find convex segement
    num_seg = EXPr['num_seg']
    for k in range(num_seg):
      v = 1/num_seg * k
      a = directionf(1/num_seg * (k+1)) - directionf(1/num_seg * k)
      b = directionf(1/num_seg * (k+2)) - directionf(1/num_seg * (k+1))
      if a > b :
        break
    if v < 0.005:
      v = 0.005
  
  # compute stepsize
    global t; t = v/ np.linalg.norm(derivativef())
    # t = Lambda
    minw = gsm(wf, 0, v)

  # update next iteration point bar_x
    bar_x = bar_x + minw * bar_p

  # update direction p
    p_0 = -gradient_f(bar_x)

    tryagain = EXPr['tryagain']
    for j in range(tryagain):
      a = np.random.uniform(-1, 1, dim)
      a = a / np.linalg.norm(a)
      p_0 = p_0 + (j) * 0.5 * a * np.linalg.norm(gradient_f(bar_x))
      res = minimize(rosen, p_0, method='SLSQP', jac=rosen_der, constraints=[ineq_cons], options={'ftol': 1e-9, 'disp': False}, bounds=None)
      if (res.success == False):
        continue
      else:
        bar_p = res.x 
        break
    if (j == tryagain - 1):
      bar_p = -gradient_f(bar_x)
      grad_num = grad_num + 1
      print(" ")
      print("\033[1;30;43m", "%s-th itration use gradient" % i,"\033[0m\n")
      print(" ")


  # show iinformation every 10 step
    if i%10 == 0:
      print("%s-th" % i, "error of f is %s" % f(bar_x))
      print(" ")
  # terminal condition
    if np.linalg.norm(bar_x, ord = inf) < EXPr['iterStop']:
        break
  

  # return RetVal
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

  if 'exec01' in pEXPr:
    exec01 = pEXPr['exec01']
    plt.plot(exec01['iteration'], exec01['error'], 'b', label='gradient method')
  if 'exec02' in pEXPr:
    exec02 = pEXPr['exec02']
    plt.plot(exec02['iteration'], exec02['error'], 'r', label='momentum method')
  if 'exec03' in pEXPr:
    exec03 = pEXPr['exec03']
    plt.plot(exec03['iteration'], exec03['error'], 'g', label='DLC direction')

  plt.ylim([0, 500])
  plt.xlim([0, 800])

  plt.show()

execpy()