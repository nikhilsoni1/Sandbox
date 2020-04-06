import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import random
plt.style.use("assets/deloitte.mplstyle")


def currency(x, pos):
    """The two args are the value and tick position"""

    if x >= 1e6:
        s = '${:1.1f}M'.format(x*1e-6)
    else:
        s = '${:1.0f}K'.format(x*1e-3)
    return s


def y_tick(x, pos):
        dummy = True
        return x


data = {"a": random.uniform(100000, 200000),
        "b": random.uniform(100000, 200000),
        "c": random.uniform(100000, 200000),
        "d": random.uniform(100000, 200000),
        "e": random.uniform(100000, 200000),
        "f": random.uniform(100000, 200000),
        "g": random.uniform(100000, 200000),
        "h": random.uniform(100000, 200000),
        "i": random.uniform(100000, 200000),
        "j": random.uniform(100000, 200000)}

group_data = list(data.values())
group_names = list(data.keys())
group_mean = np.mean(group_data)
data_values = list(data.values())
max_dat = max(data_values)
min_dat = min(data_values)
max_index = data_values.index(max_dat)
min_index = data_values.index(min_dat)
formatter = FuncFormatter(currency)
fig, ax = plt.subplots()
plot = ax.barh(group_names, group_data, label='Sales')
plot[max_index].set_color("red")
plot[max_index].set_edgecolor("black")
plot[min_index].set_color("green")
plot[min_index].set_edgecolor("black")
ax.set_title("This is a plot")
ax.set_xlabel("Some-Label")
ax.xaxis.set_major_formatter(formatter)
# ax.margins(1)
legend = ax.legend(bbox_to_anchor=(0.5, -0.25), loc='center', fontsize='small')
labels = ax.get_yticklabels()
x_lab = ax.xaxis.get_label()
print(x_lab.get_position())

plt.savefig("output/some_plot.png")