# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 16:47:07 2020

@author: 81808
"""
import time
import random
import copy
import TSP
import matplotlib.pyplot as plt
import numpy as np
def OX (a,b):#順序交差半分片親からもう半分片親からの相対的な順序を受け継ぐ
    copy_a=copy.copy(a)
    copy_b=copy.copy(b)
    next_list_a=[]
    next_list_b=[]
    num=0
    for i in a:
        num+=1
        if num<=len(a)//2 :
            next_list_a.append(i)
            copy_b.remove(i)
    next_list_a[len(next_list_a):len(next_list_a)]=copy_b
    num=0     
    for j in b:
         num+=1
         if num<=len(b)//2:
             pass
         else:
             next_list_b.append(j)
             copy_a.remove(j)
    copy_a.extend(next_list_b)
    return next_list_a, copy_a

def swap(a):
    num1=0
    num2=0
    while num1==num2:
        num1=(random.randint(0, len(a)-1))
        num2=(random.randint(0, len(a)-1))
    add1=copy.copy(a[num1])
    add2=copy.copy(a[num2])
    a.pop(num1)
    a.insert(num1,add2)
    a.pop(num2)
    a.insert(num2,add1)
    
    return a
def _tournamentSelection():
    num1=0
    num2=0
    while num1==num2:
        num1=(random.randint(0, N-1))
        num2=(random.randint(0, N-1))
    
    if population[num1].fitness < population[num2].fitness:
        return population[num1].Route
    else:
        return population[num2].Route

def change_list(temp):
    for k in range(len(temp)):
        if random.random()>0.4:
            num1=0
            num2=0
            while num1==num2:
                num1=(random.randint(0, N-1))
                num2=(random.randint(0, N-1))
            
            add1,add2=OX(temp[num1], temp[num2])
            temp.pop(num1)
            temp.insert(num1,add2)
            temp.pop(num2)
            temp.insert(num2,add1)
        
        if random.random()>0.9:
            num3=(random.randint(0, N-1))
            add3=swap(temp[num3])
            temp.pop(num3)
            temp.insert(num3,add3)
    return temp
    
class Person():
    def __init__(self, Route):
        self.Route = Route
        self.fitness = -1

def output_fitness_fig(max_generation, fitness_list, fig_name):
    # 適応度の図を作成
    plt.figure(figsize=(8,8), dpi=50)
    plt.xlabel('Generation', fontsize=18)
    plt.ylabel('Total distance', fontsize=18)
    plt.tick_params(labelsize=18)
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"
    # plt.title('Fitness', fontsize=20)
    
    plt.ylim(350, 1100)
    plt.xlim(0, max_generation)
    plt.plot([i for i in range(len(fitness_list))], 
              fitness_list, 
              linewidth = 10)##fitnessの図を作成
    plt.savefig('./fig_fitness/{}'.format(fig_name))
    plt.close()

    
if __name__ == '__main__':
    while(True):
        random.seed(time.time())
        
        N = 30
        max_generation = 300
        random.seed(random.randint(0, 100))
        
        # 初期RouteのN個生成
        Route_list = [[i for i in range(20)] for j in range(N)]
        random.shuffle(Route_list)
        for l in Route_list: random.shuffle(l)# シャッフル
        # 初期RouteのN個を基に集団生成
        population = [Person(Route) for Route in Route_list]# 初期の集団作成
        
        fitness_list = []# min適応度リスト for figure
        min_fitness = 10000# 適応度が最も良いもの
        fig_num = 0#図の数，名前用
        for num_gen in range(max_generation):
            print('generation {}'.format(num_gen))
            person_num = 0
            #個体ごとに適応度計算
            for person in population:
                if person_num % 6 == 0:
                    fitness = TSP.TSP(person.Route, True, num_gen, person_num, fig_num, 'graph')
                else:
                    fitness = TSP.TSP(person.Route, False, num_gen, person_num, fig_num, 'graph')
                
                person.fitness = fitness
                if min_fitness > fitness:
                    min_fitness = fitness
                    min_Route = person.Route
                    min_num_gen = num_gen
                    min_person_num = person_num
                if person_num % 6 == 0:
                    # fitness = TSP.TSP(person.Route, True, min_num_gen, person_num, fig_num)
                    TSP.TSP(min_Route, True, min_num_gen, min_person_num, fig_num, 'graph_best')
                    fig_num += 1
                person_num += 1
            
            random.seed(time.time())
            fitness_list.append(np.mean([person.fitness for person in population]))
            print('min: {}'.format(min([person.fitness for person in population])))
            
            # 次のpopulationを作る
            new_Route_list = []# 
            for num in range(N):
                new_Route_list.append(_tournamentSelection())
            new_Route_list = change_list(new_Route_list)#交叉と突然変異したあとのRoute_list
            population = [Person(Route) for Route in new_Route_list]# 次のpopulation
            output_fitness_fig(max_generation, fitness_list, f'{num_gen}.png')
        # 最も良かった結果を出力
        # TSP.TSP(min_Route, True, min_num_gen, min_person_num, 10000)
        print()
        print(f'Result\n Minimum Length: {min_fitness}')
        
        output_fitness_fig(max_generation, fitness_list, 'min.png')
        
        if min_fitness < 419:
            break

