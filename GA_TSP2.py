# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 00:03:40 2020

@author: Azumi Mamiya
"""
import time
import random
import TSP2 as tsp

class Route:# 経路クラス
    def __init__(self, number, route):
        self.number = number # 個体番号
        self.route = route   # 経路
        self.fitness = None    # 適応度
    
    def print_route(self):
        print(f"ID:{self.number} {self.route}")
        print(f"fitness: {self.fitness}")
    
class GeneticAlgorithm:
    def __init__(self, n_node, N, max_generation):
        self.N = N # 個体数
        self.max_generation = max_generation # 世代数の最大値
        self.route_list = self.__generate_route(n_node, N) # 経路クラス生成
    
    # ランダムな集団（ルート）生成
    def __generate_route(self, n_node, N):
        tmp_route_list = [[i for i in range(n_node)] for j in range(N)]
        for route in tmp_route_list:
            random.shuffle(route) # 経路シャッフル
        
        route_list = [Route(j, route) for j, route in enumerate(tmp_route_list)]
        
        return route_list  
    
    # 新しい集団（ルート）生成
    def __set_route(self, tmp_route_list):#
        route_list = [Route(j, route) for j, route in enumerate(tmp_route_list)]
        self.route_list = route_list
        
    # 適応度計算
    def __calculate_fitness(self, route_class, generation):
        individual_number = route_class.number
        route = route_class.route
        t = tsp.TSP(route, individual_number, generation)
        result = t.cal_total_distanse()
        
        return result
    
    # 選択
    def __selection(self):
        num1 = random.randint(0, self.N - 1)
        num2 = random.randint(0, self.N - 1)
        
        if self.route_list[num1].fitness > self.route_list[num2].fitness:
            return self.route_list[num2].route
        else:
            return self.route_list[num1].route
    
    # 交叉
    def __crossover(self):
        for n in range(self.N):
            if random.random() < 0.6:
                num = random.randint(0, self.N - 1)
                
                n_node = len(self.route_list[n].route)//2 # ノード数
                
                if random.random() < 0.5:
                    route1 = self.route_list[n].route[:n_node]
                    route2 = sorted(self.route_list[n].route[n_node:], 
                                    key=self.route_list[num].route.index)
                else:
                    route1 = sorted(self.route_list[n].route[:n_node], 
                                    key=self.route_list[num].route.index)
                    route2 = self.route_list[n].route[n_node:]
                
                next_list = route1 + route2
                
                self.route_list[n].route = next_list
            
    # 突然変異
    def __mutation(self):
        for n in range(self.N):
            if random.random() < 0.1:
                n_node = len(self.route_list[0].route)
                
                num1 = random.randint(0, n_node - 1)
                num2 = random.randint(0, n_node - 1)
                
                tmp1 = self.route_list[n].route[num1]
                tmp2 = self.route_list[n].route[num2]
                
                self.route_list[n].route.pop(num1)
                self.route_list[n].route.insert(num1, tmp2)
                self.route_list[n].route.pop(num2)
                self.route_list[n].route.insert(num2, tmp1)
        
    # 経路表示    
    def print_route(self):
        print("---output_population---")
        for i in range(len(self.route_list)):
            print(f"ID:{i:2d} Fitness: {self.route_list[i].fitness}\n{self.route_list[i].route}")
    
    # 遺伝的アルゴリズムを実行
    def run_evolve(self):
        for generation in range(self.max_generation):
            # 個体0の適応度計算
            self.route_list[0].fitness = self.__calculate_fitness(self.route_list[0], generation)
            sum_fitness = self.route_list[0].fitness # 適応度の合計
            min_fitness = self.route_list[0].fitness # 集団におけるBestな適応度
            route_class_min_fitness = self.route_list[0] #　集団におけるBestな経路
            
            # 個体1以降の適応度計算
            for route_class in self.route_list[1:]:
                route_class.fitness = self.__calculate_fitness(route_class, generation)
                random.seed(time.time())
                sum_fitness += route_class.fitness
                
                if min_fitness > route_class.fitness:
                    min_fitness = route_class.fitness
                    route_class_min_fitness = route_class
            
            ave_fitness = sum_fitness / len(self.route_list)
            
            # self.print_route()
            print(f"--Result--\nFitness\nAverage: {ave_fitness}\nMinimum: {min_fitness}")
            
            # 次のpopulationを作る
            # 選択
            new_route_list = []
            for i in range(self.N):
                new_route_list.append(self.__selection())
            
            self.__set_route(new_route_list) # 新しいRouteオブジェクト生成
            self.__crossover()               # 巡回路の交叉
            self.__mutation()                # 突然変異
            
            print()
    
        return route_class_min_fitness.route

if __name__ == '__main__':
    n_node = 20 # ノードの数
    population_size = 35
    max_generation = 5000
    GA = GeneticAlgorithm(n_node, population_size, max_generation)
    best_route = GA.run_evolve()
    
    # 最終結果　表示
    print(best_route)
    t = tsp.TSP(best_route, 0, 0)
    print(t.cal_total_distanse())
    t.plot_route()
    
    