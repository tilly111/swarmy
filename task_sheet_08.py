import numpy
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# for interactive plots
matplotlib.use('QtAgg')

td = 0.0001
t = np.arange(0.000, 160 + td, td)
alpha_r = 0.6
alpha_p = 0.1
tau_alpha = 2
tau_h = 15
n_s = np.zeros((t.shape[0],))
m = np.zeros((t.shape[0],))
n_h = np.zeros((t.shape[0],))
n_a = np.zeros((t.shape[0],))

n_s[0] = 1
n_h[0] = 0
n_a[0] = 0
m[0] = 1

# forward integration
for i in range(t.shape[0]-1):
    # init condiction t < tau_a
    if i < int(tau_alpha / td):
        n_s_tmp = 0
    else:
        n_s_tmp = n_s[i - int(tau_alpha / td)]
    if i < int(tau_h / td):
        n_h_tmp = 0
    else:
        n_h_tmp = n_h[i - int(tau_h / td)]
    # robots join comming from n_h and leaving avoid
    #n_s[i + 1] = n_s[i] + td * (-alpha_r * n_s[i] * (n_s[i] + 1) + alpha_r * n_s_tmp * (n_s_tmp + 1))
    n_s[i+1] = n_s[i] + td * (-alpha_r * n_s[i] * (n_s[i] + 1) + alpha_r * n_s_tmp * (n_s_tmp + 1)
                              - alpha_p * n_s[i] * (m[i]) + alpha_p * n_h_tmp * (n_h_tmp))
    #if n_s[i+1] < 0: n_s[i+1] = 0.0

    # avoiding state
    n_a[i + 1] = n_a[i] + td * (alpha_r * n_s[i] * (n_s[i] + 1) - alpha_r * n_s_tmp * (n_s_tmp + 1))
    #if n_a[i + 1] < 0: n_a[i + 1] = 0.0

    # robots join if puck fund, robots leave after time
    n_h[i+1] = n_h[i] + td * (alpha_p * n_s[i] * (m[i]) - alpha_p * n_h_tmp * (n_h_tmp))
    #if n_h[i + 1] < 0: n_h[i + 1] = 0.0

    # calculating the pucks
    m[i+1] = m[i] + td * (-alpha_p * n_s[i] * m[i])
    # m[i + 1] = m[i] + td * (-alpha_p * n_s[i] * (m[i]+1))
    if (i-1)*td == 80.0:
        m[i+1] = 0.5


plt.figure()
plt.plot(t, n_s, label="n_s")
plt.plot(t, n_a, label="n_a")
plt.plot(t, n_h, label="n_h")
plt.plot(t, n_s+n_a+n_h, label="whole swarm")
plt.plot(t, m, label="m")
plt.xlabel("time in [sec]")
plt.ylabel("percentage of swarm")
plt.legend()
plt.show()

