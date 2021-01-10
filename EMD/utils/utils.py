import math
import numpy as np

from metrics import *

def check_total_image_values(dataset, queryset):
    prev_sum = None
    for image in dataset:
        image_sum = np.sum(image)
        if prev_sum is not None:
            if prev_sum != image_sum:
                return False
        else:
            prev_sum = image_sum

    for image in queryset:
        image_sum = np.sum(image)
        if prev_sum != image_sum:
            return False

    return True

def normalize_set(set):
    factor = 10000
    set = set.astype(np.float64)
    for i in range(len(set)):
        image_sum = np.sum(set[i])
        set[i] = set[i] / (image_sum*1.0)
        set[i] = set[i] * factor
        if (np.sum(set[i]) != factor):
            set[i][0][0] = set[i][0][0] + (factor-np.sum(set[i]))

    return set

def convert_to_cluster(set, size):
    if (size != 4 and size != 7):
        print("Cluster sizes of (4, 4) and (7, 7) supported")
        return None

    weights = []
    clusters_per_side = 28//size
    for i in range(len(set)):
        cluster_weights = []
        for row in range(clusters_per_side):
            cluster_row_weights = []
            for column in range(clusters_per_side):
                absolute_row = row*size
                absolute_col = column*size
                cluster = set[i][absolute_row:absolute_row+size, absolute_col:absolute_col+size]

                w = np.sum(cluster)
                cluster_weights.append(w)

            # cluster_weights.append(cluster_row_weights)

        weights.append(cluster_weights)

    return weights

def calculate_distances(size):
    clusters_per_side = 28//size
    distances = []
    for start_row in range(clusters_per_side):
        for start_col in range(clusters_per_side):
            centroid_distances = []
            for end_row in range(clusters_per_side):
                for end_col in range(clusters_per_side):
                    dist = euclidean((start_row, start_col), (end_row, end_col))
                    centroid_distances.append(dist)

            distances.append(centroid_distances)

    return distances

def sort_alongside(distances, neighbors):
    zipped = zip(distances, neighbors)
    std = sorted(zipped)

    tuples = zip(*std)
    distances, neighbors = [list(tuple) for tuple in tuples]

    return distances, neighbors

def kNN(dataset, queryset, N, metric):
    neighbors_arr = []
    distances_arr = []

    for i in range(len(queryset)):
        print(i)
        neighbors = [0 for i in range(N)]
        distances = [math.inf for i in range(N)]
        for j in range(len(dataset)):
            dist = metric(dataset[j], queryset[i])

            if (dist < distances[N-1]):
                distances[N-1] = dist
                neighbors[N-1] = j
                distances, neighbors = sort_alongside(distances, neighbors)


        neighbors_arr.append(neighbors)
        distances_arr.append(distances)

    return neighbors_arr, distances_arr

def evaluate(dlabels, qlabels, neighbors, N):
    correct_count = 0
    for i in range(len(neighbors)):
        qlabel = qlabels[i]

        for neighbor in neighbors[i]:
            nlabel = dlabels[neighbor]
            if nlabel == qlabel:
                correct_count += 1


    return correct_count / (len(neighbors)*N)


def print_image(image, rows, columns):
    """ function used to print an image to the console """

    # for each row of the image
    for i in range(rows):
        # for each column
        for j in range(columns):
            # print the value at the coordinate (i, j) if it is not 0
            if image[i, j] != 0:
                print("{:.1f}".format(image[i, j]), end="")
            else:
                print(" 0 ", end="")
        # print a newline since the row has finished
        print()
    print()
