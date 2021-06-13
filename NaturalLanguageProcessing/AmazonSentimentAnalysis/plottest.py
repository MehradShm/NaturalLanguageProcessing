import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = ['iphone', 'battery&charge', 'screen', 'phone case', 'product&usability']
Positive = [123, 36, 27, 52, 521]
#Negative = [112, 42, 30, 83, 474]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, Positive, width, label='Positive', color = 'green')
#rects2 = ax.bar(x + width/2, Negative, width, label='Negative', color = 'red')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Reviews Count')
ax.set_title('Each Topic Count')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


#autolabel(rects1)
#autolabel(rects2)

fig.tight_layout()

plt.show()