from SolarPy import SolarPy

import matplotlib.pyplot as plt


# Ultimate goal of plotting the best time to view the aurora
# 1. Read and plot Kp values
# 1a. Eval Kp frequency patterns (every 27 days for solar min times?)
# 1b. Combine Kp observations with lunar cycles
# 2. Gather cloud cover data for regions
# 2a. Combine observation data with cloud cover information
# 3. Combine everything to estimate best viewing times

def get_kp_color(val):
    """ Return string of color based on Kp """
    if val > 4:
        return "Red"
    elif val < 4:
        return "Green"
    else:
        return "Yellow"

sp = SolarPy.SolarPy()

str_dir = "data_kp"
str_filename = "kp0001.tab"
str_filepath = str_dir + "\\" + str_filename

# Example calls
# print(sp.get_filelist(str_dir))
# sp.read_kp_tab(str_filepath)
# sp.read_kp_year(str_dir, [2021, 2020, 2019, 2018, 2017, 2016])
sp.read_kp_all(str_dir)

# Separate out into high, med, low
df_kp_high = sp.df_kp_all[sp.df_kp_all.Kp >= 4.66]
df_kp_med  = sp.df_kp_all[(sp.df_kp_all.Kp < 4.66) & (sp.df_kp_all.Kp >= 3.66)]
df_kp_low  = sp.df_kp_all[sp.df_kp_all.Kp < 3.66]

kp_avg = sp.df_kp_all.resample('W').mean()

# color_list = [get_kp_color(kp_val) for kp_val in sp.df_kp_all["Kp"]]
m_size = 5

plt.figure()

plt.scatter(df_kp_high.index, df_kp_high["Kp"],   s=m_size, c="Red")
plt.scatter(df_kp_med.index,  df_kp_med["Kp"],    s=m_size, c="Orange")
plt.scatter(df_kp_low.index,  df_kp_low["Kp"],    s=m_size, c="Green")

plt.plot(kp_avg.index, kp_avg["Kp"], linewidth=2)

# Bar chart
# Takes awhile to load
# plt.bar(df_kp_high["Time"], df_kp_high["Kp"],   color="Red")
# plt.bar(df_kp_med["Time"], df_kp_med["Kp"],     color="Orange")
# plt.bar(df_kp_low["Time"], df_kp_low["Kp"],     color="Green")

plt.show()

print('done')