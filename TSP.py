# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 19:22:01 2020

@author: azumi
"""

import random
import math
import itertools
import matplotlib.pyplot as plt

class Node:
    def __init__(self, num, point):
        self.num = num
        self.x = point[0]
        self.y = point[1]
    
    def print_profile(self):
        print('ID:{} (x,y)=({:2},{:2})'.format(self.num, self.x, self.y))

class TSP:
    def __init__(self, route, ind_num, generation):
        # 都市が存在する領域を指定 width * height
        width = 100  # 領域の広さ (0, wide)
        height = 100 # 領域の広さ (0, high)
        
        self.width = width
        self.height = height
        
        seed = 1     # シード値を固定，都市の位置が毎回バラバラににならないように
        
        self.ind_num = ind_num       # 個体番号
        self.generation = generation # 世代数
        self.route = route           # 巡回する順番[0, 1, 2, ...]
        
        # 都市を生成
        self.node_list = self.__generate_node(width, height, seed)
        
    # ノードを生成
    def __generate_node(self, width, height, seed):
        random.seed(seed)
        tmp_node_xy = [(i,j) for i, j in itertools.product([i for i in range(width)], [i for i in range(height)])]
        
        node_list = [Node(i, node_xy) for i, node_xy in enumerate(random.sample(tmp_node_xy, len(self.route)))]
        return node_list
    
    # ノード2点間の距離を計算
    def __calculate_length(self, node_i, node_j):
        dx = self.node_list[node_i].x - self.node_list[node_j].x
        dy = self.node_list[node_i].y - self.node_list[node_j].y
        result = math.sqrt(dx**2 + dy**2)
        
        return result 
    
    # すべての点をまわる総距離を計算
    def cal_total_distanse(self):
        length_Route = 0
        
        for i in range(len(self.route) - 1):
            length_Route += self.__calculate_length(self.route[i], self.route[i + 1])
        
        return length_Route
    
    # 図を表示する
    def plot_route(self):
        margin = 10 # 図の外枠（余白）
        x = []
        y = []
        
        plt.figure(figsize = (8, 8), dpi = 50)
        plt.ylim(-margin, self.width + margin)
        plt.xlim(-margin, self.width + margin)
        plt.xticks(color = "None")
        plt.yticks(color = "None")
        plt.title('Traveling Salesman Problem', fontsize = 20)
        plt.text(0, 90, 'Generation:{:2}\nIndividual:{:3}\nLength: {:4}'\
                 .format(self.generation, self.ind_num, round(self.cal_total_distanse())), fontsize = 20)
        plt.tick_params(length = 0)
        
        for node in self.node_list:
            plt.plot(node.x, node.y, marker = 'o', markersize = 15, color = 'green')
            plt.annotate(node.num, xy = (node.x, node.y), size = 25)
        
        node_list_sorted = []# 巡回順にノードを並べる
        for i in range(len(self.node_list)):
            node_list_sorted.append(self.node_list[self.route[i]])
        
        for node in node_list_sorted:
            x.append(node.x)
            y.append(node.y)
        x.append(node_list_sorted[0].x)
        y.append(node_list_sorted[0].y)
        plt.plot(x, y)
        
if __name__ == "__main__":
    # random.seed()
    route = [i for i in range(20)]
    # random.shuffle(route)
    generation = 0
    individual_number = 0
    tsp = TSP(route, individual_number, generation)
    print(tsp.cal_total_distanse())
    tsp.plot_route()