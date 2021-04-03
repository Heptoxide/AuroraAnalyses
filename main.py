from SolarPy import SolarPy

import matplotlib.pyplot as plt


# Ultimate goal of plotting the best time to view the aurora
# 1. Read and plot Kp values
# 1a. Eval Kp frequency patterns (every 27 days for solar min times?)
# 1b. Combine Kp observations with lunar cycles
# 2. Gather cloud cover data for regions
# 2a. Combine observation data with cloud cover information
# 3. Combine everything to estimate best viewing times

sp = SolarPy.SolarPy()

str_dir = "tab"
str_filename = "kp0001.tab"
str_filepath = str_dir + "\\" + str_filename

# print(sp.get_filelist(str_dir))
# sp.read_kp_tab(str_filepath)
sp.read_kp_year(str_dir, [2011,2012,2013])
# sp.read_kp_all(str_dir)

plt.figure()

plt.plot(sp.df_kp_all["Time"], sp.df_kp_all["Kp"], alpha=0.5, linestyle='-', marker='o', markersize=0.5)

plt.show()

print('done')