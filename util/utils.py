import bisect
import random
from collections import defaultdict

import matplotlib.pyplot  as plt
import pandas as pd

from conM import FixedMess
from conM.FixedMess import FixedMes
import scipy.stats as stats
def judgeS1S2(s1,s2):
    for i in range(len(s1)):
        if s1[i] < s2[i]:
            return False
    return True

def recordTime(allTasks):
    jzj = defaultdict(lambda: [])

    for id, value in allTasks.items():
        planeid = value.belong_plane_id
        if planeid == 0:
            continue
        taskid = value.taskid
        if taskid == 1:
            continue
        if taskid == FixedMes.planeOrderNum:
            continue
        es = value.es
        ef = value.ef
        jzj[planeid].append((es, ef))
def build_Pc_q_table(n_states, actions):
    return pd.DataFrame(
        np.zeros((n_states, len(actions))),
        columns=actions
    )


def build_Pm_q_table(n_states, actions):
    return pd.DataFrame(
        np.zeros((n_states, len(actions))),
        columns=actions
    )
def get_next_execution_time(i):
    sigma = 0.3
    if i == 0:
        return 0
    elif i == 1:
        return 0
    elif i == 2:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[2], scale=sigma).rvs()
    elif i == 3:
        return stats.truncnorm((-0.8) / sigma, 0.8 / sigma, loc=FixedMes.OrderTime[3], scale=sigma).rvs()
    elif i == 4:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[4], scale=sigma).rvs()
    elif i == 5:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[5], scale=sigma).rvs()
    elif i == 5:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[5], scale=sigma).rvs()
    elif i == 6:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[6], scale=sigma).rvs()
    elif i == 7:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[7], scale=sigma).rvs()

    elif i == 8:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[8], scale=sigma).rvs()
    elif i == 9:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[9], scale=sigma).rvs()

    elif i == 10:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[10], scale=sigma).rvs()
    elif i == 11:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[11], scale=sigma).rvs()

    elif i == 12:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[12], scale=sigma).rvs()
    elif i == 13:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[13], scale=sigma).rvs()
    elif i == 14:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[14], scale=sigma).rvs()

    elif i == 15:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[15], scale=sigma).rvs()
    elif i == 16:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[16], scale=sigma).rvs()
    elif i == 17:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[17], scale=sigma).rvs()
    elif i == 18:
        return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[18], scale=sigma).rvs()
    elif i == 19:
        return 0
class Logger(object):
    log_level = 3
    @staticmethod
    def warning(message):
        if Logger.log_level > 1:
            Logger.log("warning", message)

    @staticmethod
    def error(message):
        Logger.log("error", message)

    @staticmethod
    def info(message):
        if Logger.log_level > 2:
            Logger.log("info", message)
    @staticmethod
    def debug(message):
        if Logger.log_level > 3:
            Logger.log("debug", message)
    @staticmethod
    def log(log_type, message):
        if log_type == "warning":
            print(PrintColors.WARNING),
            print("WARNING: "),
        elif log_type == "error":
            print(PrintColors.FAIL),
            print("ERROR: "),
        elif log_type == "info":
            print("INFO: "),
        elif log_type == "debug":
            print("DEBUG: ")
        print(message),
        print(PrintColors.ENDC)
class DeepThoughtException(Exception):
    pass

class UnfeasibleScheduleException(DeepThoughtException):
    pass
class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
def getRandNum(start,end):
    return (random.random() *100000) % (end -start)

import numpy as np
import copy

def _cdf(weights):
    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        result.append(cumsum / total)
    return result

def choice(population, weights):
    assert len(population) == len(weights)
    cdf_vals = _cdf(weights)
    x = random.random()
    idx = bisect.bisect(cdf_vals, x)
    return population[idx]

def findW(D, total_resource, P):
    W = []
    useNowResource = [0 for i in range(len(total_resource))]

    for k in range(len(total_resource)):
        for p in P:
            useNowResource[k] = useNowResource[k] + p.resources[k]

    tempuseNowResource = copy.deepcopy(useNowResource)

    for task in D:
        for k in range(len(useNowResource)):
            if tempuseNowResource[k] > total_resource[k]:
                break
        flag = True
        for k in range(len(useNowResource)):
            if tempuseNowResource[k] + task.resources[k] > total_resource[k]:
                flag = False
                break
        if flag == True:
            W.append(task)

            for k in range(len(useNowResource)):
                tempuseNowResource[k] += task.resources[k]
    W.sort(key=lambda x: x.priority)
    return W


def conditionCheck(allltasks, AON, code, s):
    D = []
    for i in code:
        if i in s:
            continue
        flag = True
        prenumber = AON[i]  # 前序
        for ordernumber in prenumber:
            if ordernumber not in s:
                flag = False
                break
        if flag == True:
            D.append(allltasks[i - 1])
    return D

def randomint_plus(low, high=None, cutoff=None, size=None):
    """用来生成不包含一些中间数值的随机整数或序列

    Parameters
    ----------
    low : int
        生成随机整数的下界
    high: int
        生成随机整数的上界
    cutoff: int/list
        不需要包含的一个或多个值
    size: tuple
        需要产生的随机数规模
    Notes
    -----
    1. 在调用过程中，如果high, cutoff, size都缺省，就默认返回一个[0, low)的值
    2. 如果cutoff, size缺省，返回[low, high)的一个随机整数值
    3. 如果size缺省， 则返回一个[low, cutoff)U(cutoff, high)的随机整数值
    4. 返回一个给定size的矩阵，矩阵元素为[low, cutoff)U(cutoff, high)的随机整数值

    See Also
    --------
    np.random.randint()

    """
    if high is None:
        assert low is not None, "必须给定一个值作为上界"
        high = low
        low = 0
    number = 1  # 将size拉长成为一个向量
    if size is not None:
        for i in range(len(size)):
            number = number * size[i]

    if cutoff is None:  # 如果不需要剔除值，就通过numpy提供的函数生成随机整数
        random_result = np.random.randint(low, high, size=size)
    else:
        if number == 1:  # 返回一个随机整数
            random_result = randint_digit(low, high, cutoff)
        else:  # 返回一个形状为size的随机整数数组
            random_result = np.zeros(number, )
            for i in range(number):
                random_result[i] = randint_digit(low, high, cutoff)
            random_result = random_result.reshape(size)

    return random_result.astype(int)


def randint_digit(low, high, cutoff):
    """用来生成一个在区间[low, high)排除cutoff后的随机整数
    Parameters
    ----------
    low: int
        下限，能够取到
    high: int
        上限，不能够取到
    cutoff: int/list
        一个需要剔除的数或者数组，要求在(low, high)区间之间
    """
    digit_list = list(range(low, high))
    if type(cutoff) is int:  # 只需要剔除一个值
        if cutoff in digit_list:  # 如果需要剔除的值不存在，则不执行剔除操作
            digit_list.remove(cutoff)
    else:
        for i in cutoff:  # 需要剔除多个值的情况
            if i not in digit_list:  # 如果需要剔除的值不存在，则不执行剔除操作
                continue
            digit_list.remove(i)

    np.random.shuffle(digit_list)
    return digit_list.pop()  # 生成的序列打乱并且返回当前的随机值

def gen_randint(low, high, discard):
    result_list = list(range(low, high))
    result_list.remove(discard)
    np.random.shuffle(result_list)
    return result_list.pop()

def Dominate(Pop1, Pop2):
    '''
    :param Pop1:
    :param Pop2:
    :return: If Pop1 dominate Pop2, return True
    '''
    if (Pop1.f[0] > Pop2.f[0] and Pop1.f[1] < Pop2.f[1]) or \
            (Pop1.f[0] >= Pop2.f[0] and Pop1.f[1] < Pop2.f[1]) or \
            (Pop1.f[0] > Pop2.f[0] and Pop1.f[1] <= Pop2.f[1]):
        return True
    else:
        return False

def crowding_distance(NDSet):
    Distance = [0] * len(NDSet)
    NDSet_obj = {}

    for i in range(len(NDSet)):
        NDSet_obj[i] = NDSet[i].f

    ND = sorted(NDSet_obj.items(), key=lambda x: (-x[1][0],x[1][1]))

    Distance[ND[0][0]] = 1e+20
    NDSet[0].c_distance = 1e+20
    Distance[ND[-1][0]] = 1e+20
    NDSet[-1].c_distance = 1e+20
    for i in range(1, len(ND) - 1):
        if Distance[ND[i][0]] == 0:
            Distance[ND[i][0]] = abs(ND[i + 1][1][0] - ND[i - 1][1][0]) + abs(ND[i + 1][1][1] - ND[i - 1][1][1])
            NDSet[i].c_distance = Distance[ND[i][0]]
    distance = dict(enumerate(Distance))
    New_distance = sorted(distance.items(), key=lambda x: x[1], reverse=True)
    L = [A[0] for A in New_distance]
    return L

def fast_non_dominated_sort(Pop):
            S = [[] for i in range(len(Pop))]
            front = [[]]
            n = [0 for i in range(len(Pop))]
            rank = [0 for i in range(len(Pop))]

            for p in range(len(Pop)):
                S[p] = []
                n[p] = 0
                for q in range(len(Pop)):
                    if Dominate(Pop[p], Pop[q]):
                        if q not in S[p]:
                            S[p].append(q)
                            Pop[p].sp.append(q)

                    elif Dominate(Pop[q], Pop[p]):
                        n[p] = n[p] + 1
                        Pop[p].np+=1
                if n[p] == 0:
                    rank[p] = 0
                    if p not in front[0]:
                        front[0].append(p)
            i = 0
            while (front[i] != []):
                Q = []
                for p in front[i]:
                    for q in S[p]:
                        n[q] = n[q] - 1
                        if (n[q] == 0):
                            rank[q] = i + 1
                            Pop[q].rank = i+1
                            if q not in Q:
                                Q.append(q)
                i = i + 1
                front.append(Q)
            del front[len(front) - 1]
            NDSet = []
            for Fi in front:
                NDSeti = []
                for pi in Fi:

                    NDSeti.append(Pop[pi])
                NDSet.append(NDSeti)
            return NDSet

def getTwoDimensionListIndex(L, value):
    index1 = -1
    index2 = -1
    """获得二维列表某个值的一维索引值的另一种方法"""
    for i in range(len(L)):
        for j in range(len(L[i])):
            if len(L[i][j]):
                for m in range(len(L[i][j])):
                    if L[i][j][m] == value:
                        index1 = i
                        index2 = j
    return index1, index2

#判断是否存在重复
def judgeDuplicated(array):
    array.sort()
    count=0
    while count<len(array)-1:
        if array[count]==array[count+1]:
            return True
        else:
            count+=1
    return False

#多目标 帕累托前沿画图
def Plot_NonDominatedSet(EP):
    x = []
    y = []
    for i in range(len(EP)):
        x.append(EP[i].f[0])
        y.append(EP[i].f[1])
    plt.plot(x, y, '*')
    plt.xlabel('makespan')
    plt.ylabel('Average Load')
    plt.legend()
    plt.savefig(r'obj_result/'+'first'+'.png')
    plt.close()


def writeTxt(filename,content):
    with open(filename, 'w') as f:
        for i in content:
            f.write(i + '\n')
# networkX_5c.py
# Demo of critical path method(CPM) with NetworkX
# Copyright 2021 YouCans, XUPT
# Crated：2021-05-25
# Youcans 原创作品：[Python数模笔记@Youcans](https://blog.csdn.net/youcans )

def cpm(Activities):
    edge = []
    for activity in Activities:
        id = activity.id
        for toid in activity.successor:
            edge.append((id,toid,activity.duration))

    DG = nx.DiGraph()  # 创建：空的 有向图
    DG.add_nodes_from(range(0, len(Activities)), VE=0, VL=0)
    DG.add_weighted_edges_from(edge)

    lenCriticalPath = nx.dag_longest_path_length(DG)  # 关键路径的长度

    print("关键路径长度：{}".format(lenCriticalPath))  # 51

    pos = {1: (0, 4), 2: (5, 8), 3: (5, 4), 4: (5, 0), 5: (10, 8), 6: (10, 0), 7: (15, 4), 8: (20, 4)}  # 指定顶点位置
    nx.draw(DG, pos, with_labels=True, alpha=0.8)  # 绘制无向图
    labels = nx.get_edge_attributes(DG, 'weight')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=labels, font_color='c')  # 显示边的权值
    plt.show()

import networkx as nx
def CPM(newedge):


    idTime =[0.0 for i in range(FixedMess.FixedMes.Activity_num)]

    for  _,activity in FixedMess.FixedMes.act_info.items():
        if activity.taskid == 1:
            idTime[activity.id] = 0
        elif activity.taskid == FixedMess.FixedMes.planeOrderNum:
            idTime[activity.id] = 0
        else:
            idTime[activity.id] = round(FixedMess.FixedMes.getTime(activity.taskid) *100,1)
            #idTime[activity.id] = FixedMess.FixedMes.OrderTime[activity.taskid]

    for i  in range(len(newedge)):
            id = newedge[i][0]
            to =newedge[i][1]
            tu = (id, to, idTime[id])
            newedge[i] = tu


    DG = nx.DiGraph()  # 创建：空的 有向图
    DG.add_nodes_from(range(0, FixedMess.FixedMes.Activity_num), VE=0, VL=0)
    DG.add_weighted_edges_from(newedge)

    lenNodes = len(DG.nodes)  # 顶点数量 YouCans
    topoSeq = list(nx.topological_sort(DG))  # 拓扑序列: [1, 3, 4, 2, 5, 7, 6, 8]

    lenCriticalPath = nx.dag_longest_path_length(DG)  # 关键路径的长度

    return lenCriticalPath/100  # 51

def judgeFitness(pop1, pop2):
        Cmax = FixedMes.lowTime
        if pop1.WorkTime < Cmax and pop2.WorkTime < Cmax:
            if pop1.Pr > pop2.Pr:
                return -1
            elif pop1.Pr < pop2.Pr:
                return 1
            else:
                if pop1.Ecmax < pop2.Ecmax:
                    return -1
                else:
                    return 1

        elif pop1.WorkTime > Cmax and pop2.WorkTime < Cmax:
            return 1
        elif pop1.WorkTime < Cmax and pop2.WorkTime > Cmax:
            return -1
        elif pop1.WorkTime > Cmax and pop2.WorkTime > Cmax:
            if pop1.WorkTime > pop2.WorkTime:
                return -1
            if pop1.WorkTime < pop2.WorkTime:
                return 0


