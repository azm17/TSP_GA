# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 16:20:51 2020

@author: azumi
"""
import random
import math
import itertools
import matplotlib.pyplot as plt


class Node():
    def __init__(self, num, point):
        self.num = num
        self.x = point[0]
        self.y = point[1]
    
    def print_profile(self):
        print('ID:{} (x,y)=({:2},{:2})'.format(self.num, self.x, self.y))
        
def calculate_length(node_i, node_j):
    result = math.sqrt((node_i.x - node_j.x)**2 + (node_i.y - node_j.y)**2)
    return result

def plot_Route(Node_list, L):
    x = []; y = []
    plt.figure(figsize=(8, 8))
    width = 10
    plt.ylim(-width, L + width); plt.xlim(-width, L + width)
    plt.xticks(color="None")
    plt.yticks(color="None")
    plt.title('Traveling Salesman Problem',  fontsize=20)
    plt.tick_params(length = 0)
    
    for node in Node_list:
        x.append(node.x); y.append(node.y)
    x.append(Node_list[0].x); y.append(Node_list[0].y)
    plt.plot(x, y)
    
    for node in Node_list:
        plt.plot(node.x, 
                 node.y, 
                 marker='o', 
                 markersize=15)

        plt.annotate(node.num, 
                     xy=(node.x, node.y), 
                     size = 25)
    
def TSP(Route, Bool):
    L = 100
    NumberOfNode = len(Route)
    length_Route = 0
    
    random.seed(1)    
    
    point_list = [(i,j) for i, j in itertools.product([i for i in range(L)], [i for i in range(L)])]
    random.shuffle(point_list)
    
    Node_list = [Node(i, point_list.pop()) \
                 for i in range(NumberOfNode)]
    
    # for n in Node_list: n.print_profile()
    
    
    i = 0
    while(True):
        length_Route += calculate_length(Node_list[Route[i]], Node_list[Route[i+1]])
        if i > NumberOfNode - 3:
            break
        i += 1
    Node_lsit_2 = []
    for i in range(len(Node_list)):
        Node_lsit_2.append(Node_list[Route[i]])
    if Bool: plot_Route(Node_lsit_2, L)
    
    return length_Route

if __name__ == "__main__":
    Route = [i for i in range(20)]
    fitness = TSP(Route, True)
    print('result: {}'.format(fitness))