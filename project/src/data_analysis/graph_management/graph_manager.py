import datetime
import random
from operator import itemgetter
from random import shuffle
import matplotlib.dates as mdates
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


class GraphManager:
    def __init__(self):
        pass

    @staticmethod
    def plot_graph(Xs, Ys, x_label=None, y_label=None, title=None, labels=None):
        plt.figure()
        if(type(Xs[0]) != list and type(Xs[0]) != tuple):
            Xs = [Xs]
            Ys = [Ys]
            labels = [labels]

        for i in range(len(Xs)):
            current_label = None
            if(labels):
                current_label = labels[i]
            GraphManager.__plot_single_line(Xs[i], Ys[i], x_label, y_label, title, current_label)

    @staticmethod
    def __plot_single_line(X, Y, x_label=None, y_label=None, title=None, labels=None):
        if(labels):
            if(type(labels) != list and type(labels) != tuple):
                plt.plot(X, Y, label=labels)
                plt.legend()
            else:
                GraphManager.__plot_fraction_label_line(X, Y, labels)
        else:
            plt.plot(X, Y)

        if(x_label):
            plt.xlabel(x_label)
        if(y_label):
            plt.ylabel(y_label)
        if(title):
            plt.title(title)
        plt.axhline(y=0, color='b', linestyle='-')

    @staticmethod
    def __plot_fraction_label_line(X, Y, labels):
        segments = []
        X_Y = [(mdates.date2num(date_time), value) for date_time, value in list(zip(X, Y))]
        colors = []
        segment_buffer = []
        artists = []
        for i in range(len(X_Y)):
            if((i != 0 and labels[i] != labels[i - 1]) or i == len(X) - 1):
                segments.append(segment_buffer)
                color = GraphManager.__random_color(labels[i - 1])
                colors.append(color)
                artists.append(plt.Line2D((0, 1), (0, 0), color=color))
                segment_buffer = [X_Y[i-1]]
            segment_buffer.append(X_Y[i])

        coll = LineCollection(segments, colors=colors)
        plt.gca().add_collection(coll)

        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,3,5,7,9,11]))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.gca().xaxis.set_tick_params(which='major', rotation=45)

        unique_labels, _ = zip(*sorted(((e, labels.count(e)) for e in set(labels)), key=lambda x: x[1], reverse=True))
        plt.legend([plt.Line2D((0, 1), (0, 0), color=GraphManager.__random_color(label)) for label in unique_labels], unique_labels, loc="best")
        plt.plot()

    @staticmethod
    def plot_3d_histogram(X, Y, Z, title=None):
        fig = plt.figure()
        ax1 = fig.add_subplot(111, projection='3d')

        X_ints = GraphManager.__convert_to_ints(X)
        Y_ints = GraphManager.__convert_to_ints(Y)

        size_bar = 0.5

        ax1.set_xticks(X_ints)
        ax1.set_xticklabels(X)
        ax1.set_yticks(Y_ints)
        ax1.set_yticklabels(Y)

        if(title):
            plt.title(title)

        x_unique_values = set(X_ints)
        for unique_value in x_unique_values:
            position_x = []
            position_y = []
            dz = []
            for i in range(len(X_ints)):
                if (X_ints[i] == unique_value):
                    position_x.append(X_ints[i] - size_bar / 2)
                    position_y.append(Y_ints[i] - size_bar / 2)
                    dz.append(Z[i])

            position_z = np.zeros(len(position_x))
            dx = np.ones(len(position_x)) * size_bar
            dy = np.ones(len(position_x)) * size_bar

            ax1.bar3d(position_x, position_y, position_z, dx, dy, dz, alpha=0.8)

        ax1.set_zlim3d(0)

    @staticmethod
    def __random_color(seed=None):
        random.seed(seed)
        # Max is 255, Min is 0
        r_middle = lambda: random.randint(30, 240)
        r_low = lambda: random.randint(0, 80)
        r_high = lambda: random.randint(146, 240)
        rgb = [r_middle(), r_low(), r_high()]
        shuffle(rgb)
        return '#%02X%02X%02X' % tuple(rgb) # '#%02X%02X%02X' % (r(), r(), r())

    @staticmethod
    def __convert_to_ints(items):
        seen_value = {}
        index = 1
        result = []
        for item in items:
            if(item not in seen_value):
                seen_value[item] = index
                index += 1
            result.append(seen_value[item])
        return result

    @staticmethod
    def plot_histogram(X, Ys, labels=None, bar_ids=None, x_label=None, y_label=None, title=None, color_per_bar=False):
        if (type(Ys) != list):
            Ys = [Ys]
        fig = plt.figure()
        ax = fig.add_subplot(111)

        width = 1. / (len(Ys) + 1)

        for i, Y in enumerate(Ys):
            x_pos = X if bar_ids else np.arange(len(X))
            current_label = labels[i] if labels else ""
            x_final_position = x_pos if bar_ids else (x_pos + i * width) - 0.5 + width
            bar_list = ax.bar(x_final_position, Y, width, align='center', label=current_label)

        if(color_per_bar):
            for i in range(len(bar_list)):
                color = GraphManager.__random_color(bar_ids[i])
                bar_list[i].set_color(color)
            unique_labels, _ = zip(*sorted(((e, bar_ids.count(e)) for e in set(bar_ids)), key=lambda x: x[1], reverse=True))
            plt.legend([plt.Line2D((0, 1), (0, 0), color=GraphManager.__random_color(label)) for label in unique_labels], unique_labels, loc="best")
        else:
            plt.legend(loc="best")
            plt.xticks(x_pos, X)
            plt.xticks(rotation=35)

        if (x_label):
            plt.xlabel(x_label)
        if (y_label):
            plt.ylabel(y_label)
        if (title):
            plt.title(title)
        plt.axhline(y=0, color="black", linestyle="-", linewidth="1")

    @staticmethod
    def show():
        plt.show()