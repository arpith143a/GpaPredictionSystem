import csv
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.legend_handler import HandlerLine2D

sem1_true = 5
sem1_pred = 9

sem2_true = 6
sem2_pred = 10

sem3_true = 7
sem3_pred = 11

sem4_true = 8
sem4_pred = 12

def get_classes(true_gpa_list, pred_gpa_list):
    class_0 = [] # 0.00-2.49
    class_1 = [] # 2.50-2.74
    class_2 = [] # 2.75-2.99
    class_3 = [] # 3.00-3.49
    class_4 = [] # 3.50-3.95
    class_5 = [] # 3.96-4.00

    maes = np.abs( np.array(true_gpa_list) - np.array(pred_gpa_list) )

    for i in range(len(true_gpa_list)):
        if  0 <=  true_gpa_list[i] < 2.5:
            class_0.append(maes[i])
        elif 2.5 <=  true_gpa_list[i] < 2.75:
            class_1.append(maes[i])
        elif 2.75 <=  true_gpa_list[i] < 3:
            class_2.append(maes[i])
        elif 3 <=  true_gpa_list[i] < 3.5:
            class_3.append(maes[i])
        elif 3.5 <=  true_gpa_list[i] < 3.96:
            class_4.append(maes[i])
        elif 3.95 <=  true_gpa_list[i] <= 4:
            class_5.append(maes[i])
    return [
            np.mean(class_0),
            np.mean(class_1),
            np.mean(class_2),
            np.mean(class_3),
            np.mean(class_4),
            np.mean(class_5)]


sem1_true_list = []
sem2_true_list = []
sem3_true_list = []
sem4_true_list = []

sem1_pred_list = []
sem2_pred_list = []
sem3_pred_list = []
sem4_pred_list = []
with open('graph.csv', 'rt') as csvfile:
    my_reader = csv.reader(csvfile, delimiter=',')
    count = 0
    for row in my_reader:

        if count == 0:
            count = 1
            continue

        sem1_true_list.append(float(row[sem1_true]))
        sem2_true_list.append(float(row[sem2_true]))
        sem3_true_list.append(float(row[sem3_true]))
        sem4_true_list.append(float(row[sem4_true]))

        sem1_pred_list.append(float(row[sem1_pred]))
        sem2_pred_list.append(float(row[sem2_pred]))
        sem3_pred_list.append(float(row[sem3_pred]))
        sem4_pred_list.append(float(row[sem4_pred]))

plt.xticks(np.arange(6), ('0-2.49', '2.5-2.74', '2.75-2.99', '3.0-3.49', '3.5-3.95', '3.96-4.0'))
line1, = plt.plot(get_classes(sem1_true_list, sem1_pred_list), '-',  marker='.', label="Semester 1")
line2, = plt.plot(get_classes(sem2_true_list, sem2_pred_list), '--', marker='.', label="Semester 2")
line3, = plt.plot(get_classes(sem3_true_list, sem3_pred_list), '-.', marker='.', label="Semester 3")
line4, = plt.plot(get_classes(sem4_true_list, sem4_pred_list), ':',  marker='.', label="Semester 4")

# Create a legend for the first line.
first_legend = plt.legend(handles=[line1], loc=1)

# Add the legend manually to the current Axes.
ax = plt.gca().add_artist(first_legend)

plt.legend(handler_map={line1: HandlerLine2D(numpoints=0)})

plt.show()
