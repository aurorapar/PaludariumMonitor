import time

import matplotlib.pyplot as plt

# TODO: thread this so that other code is not blocked
import numpy as np


class Graph:
    def __init__(self, title, x_label, x_input, y_labels=(), y_inputs=(), colors=()):

        if len(y_labels) != len(y_inputs):
            raise ValueError("There are not enough labels for the y values")

        plt.ion()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        lines = list()

        self.fig.patch.set_facecolor('xkcd:black')
        self.lines = []
        self.axes = []

        for i, data_set in enumerate(y_inputs):
            # Not using list(map()) so we can more easily use spines below
            axs = None
            if i < 1:
                axs = self.ax
            else:
                axs = self.ax.twinx()
                axs.spines.right.set_position(("axes", 1 + .2*(i-1)))

            self.axes.append(axs)
            axs.set_xlabel(x_label)
            axs.set_ylabel(y_labels[i])
            axs.set_facecolor((0.06,0.06,0.06))
            axs.spines['bottom'].set_color('white')
            axs.spines['top'].set_color('white')
            axs.spines['left'].set_color('white')
            axs.spines['right'].set_color('white')
            axs.xaxis.label.set_color('white')
            axs.yaxis.label.set_color('white')
            axs.grid(alpha=0.1)
            axs.title.set_color('white')
            axs.tick_params(axis='x', colors='white')
            axs.tick_params(axis='y', colors='white')
            axs, = axs.plot(x_input[0 if len(x_input) == 1 else i], data_set)
            self.lines.append(axs)
            axs.set_label(y_labels[i])
            lines.append((axs, data_set))
            if colors:
                lines[-1][0].set_color(colors[i])

        handles = list(zip(*lines))[0]
        self.ax.legend(loc='best', handles=handles)
        plt.title(title)

    def update(self, x_input, y_input):
        for i, data_set in enumerate(y_input):
            axs = self.lines[i]
            axs.set_xdata(x_input)
            axs.set_ydata(y_input[i])
            self.ax.set_xlim(min(x_input), max(x_input))
            self.axes[i].set_ylim(min(y_input[i]) - np.mean(y_input[i]) / 2, max(y_input[i]) + np.mean(y_input[i]) / 2)
        plt.subplots_adjust(right=.75)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        time.sleep(.1)
