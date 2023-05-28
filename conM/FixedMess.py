from collections import defaultdict

import scipy.stats as stats

from chromosome.Chromo import Chromosome

class FixedMes(object):
    """
    distance:
    orderInputMes:
    """


    distance = [[]]

    numJzjPos = 18
    numHumanAll = [18,60]

    planeOrderNum = 19
    planeNum = 8
    jzjNumbers=[1,2,3,4,5,6,7,8]  #舰载机编号

    #座舱限制。相当于是每个站位都有一个座舱，每个舰载机只能用自己座舱。
    space_resource_type = planeNum
    total_space_resource = [1 for i in range(planeNum)]

    Human_resource_type = 4 #先考虑只有一类人
    # 特设、航电、军械、机械
    total_Huamn_resource = [5,7,10,12]  # 每种人员数量

    # total_Huamn_resource = [30]
    constraintOrder = defaultdict(lambda: []) #记录每类人的可作用工序，和可作用舰载机范围
    # constraintOrder[0] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

    constraintOrder[0] = [ 1, 2, 5]
    constraintOrder[1] = [3,4, 16,17]
    constraintOrder[2] = [7, 8, 14,16]
    constraintOrder[3] = [6, 9, 10, 11,12,13,15]

    modeflag = 0 #0是单机、1是全甲板，这里考虑全甲板，如果是全甲板
    # constraintJZJ = defaultdict(lambda: []) #保障人员可作用舰载机范围,两种模式，单机或者全甲板

    station_resource_type = 5
    total_station_resource = [6,12,5,5,6]

    #飞机数量比较少的时候，这些燃料资源的限制约束不起作用。
    # total_renew_resource = [5,5,2,4,2]
    # # total_renew_resource = [1,1,1,1,1]
    total_renew_resource = [99,99,99,99,99]

    constraintS_Order = defaultdict(lambda: [])  # 记录每类设备的可作用工序，和可作用舰载机范围

     # 设备保障范围约束
    constraintS_JZJ = defaultdict(lambda: [])

    constraintS_JZJ[0] = [[1, 2, 3],
                          [3, 4, 5],
                          [6, 7],
                          [7,8,9],
                          [9,10,11],
                          [12]]

    constraintS_JZJ[1] = [[1],
                          [2],
                          [3],
                          [4],
                          [5],
                          [6],
                          [7],
                          [8],
                          [9],
                          [10],
                          [11],
                          [12]
                          ]
    constraintS_JZJ[2] = [[1,2,3,4],
                          [4,5,6,7],
                          [7,8,9],
                          [9,10,11],
                          [12]
                          ]

    constraintS_JZJ[3] = [[1,2,3,4],
                          [4,5,6,7],
                          [7,8,9],
                          [9,10,11],
                          [12]
                          ]

    constraintS_JZJ[4] = [[1,2,3],
                          [2,3,4],
                          [4,5,6],
                          [7,8,9],
                          [9,10,11],
                          [12]
                          ]

    Activity_num  = (planeOrderNum)*planeNum+2 #活动数量
    #工序顺序
    SUCOrder = defaultdict(lambda: [])
    SUCOrder[1] = [2,4,6,11,12,13]
    SUCOrder[2] = [3]
    SUCOrder[3] = [10]
    SUCOrder[4] = [5]
    SUCOrder[5] = [10]
    SUCOrder[6] = [3,5,7,9]
    SUCOrder[7] = [14]
    SUCOrder[8] = [9]
    SUCOrder[9] = [10]
    SUCOrder[10] = [14]
    SUCOrder[11] = [18]
    SUCOrder[12] = [18]
    SUCOrder[13] = [18]
    SUCOrder[14] = [15,16]
    SUCOrder[15] = [17]
    SUCOrder[16] = [17]
    SUCOrder[17] = [18]
    SUCOrder[18] = [19]
    SUCOrder[19] = []
    # SUCOrder[1] = [2,4,6,9,10,11,12,13,14]
    # SUCOrder[2] = [3]
    # SUCOrder[3] = [15]
    # SUCOrder[4] = [5]
    # SUCOrder[5] = [15]
    # SUCOrder[6] = [7]
    # SUCOrder[7] = [8]
    # SUCOrder[8] = [15]
    # SUCOrder[9] = [15]
    # SUCOrder[10] = [15]
    # SUCOrder[11] = [18]
    # SUCOrder[12] = [15]
    # SUCOrder[13] = [18]
    # SUCOrder[14] = [18]
    # SUCOrder[15] = [16,17]
    # SUCOrder[16] = [18]
    # SUCOrder[17] = [18]
    # SUCOrder[18] = [19]
    # SUCOrder[19] = []

    # SUCOrder[1] = [2, 3]
    # SUCOrder[2] = [4]
    # SUCOrder[3] = [4]
    # SUCOrder[4] = [5, 6, 7]
    # SUCOrder[5] = [12]
    # SUCOrder[6] = [8, 9]
    # SUCOrder[7] = [10]
    # SUCOrder[8] = [11]
    # SUCOrder[9] = [12]
    # SUCOrder[10] = [12]
    # SUCOrder[11] = [12]
    # SUCOrder[12] = [13]
    # SUCOrder[13] = []
    #
    # OrderInputMes = [[],
    #                  [(0, 0), (0, 0), (0, 0)],  # 虚拟1
    #                  [(0, 1), (0, 0), (0, 0)],  # 2通风
    #                  [(0, 1), (1, 1), (0, 1)],  # 3电源
    #                  [(1, 1), (0, 0), (0, 0)],  # 4机翼展开
    #                  [(1, 1), (1, 1), (0, 0)],  # 5充氧
    #                  [(2, 1), (0, 0), (0, 0)],  # 6充氮
    #                  [(2, 2), (1, 1), (0, 1)],  # 7通电
    #                  [(2, 2), (0, 0), (0, 0)],  # 8,挂弹
    #                  [(3, 1), (0, 1), (0, 1)],  # 9加油
    #                  [(3, 1), (4, 1), (0, 0)],  # 10飞参
    #                  [(3, 1), (3, 1), (0, 0)],  # 11弹药加载
    #                  [(3, 2), (1, 1), (0, 1)],  # 12机翼展开
    #                  [(3, 1), (0, 0), (0, 0)],  # 13
    #                  [(3, 1), (0, 0), (0, 1)],  # 14
    #                  [(0, 1), (2, 1), (0, 0)],  # 15
    #                  [(2, 1), (0, 0), (0, 0)],  # 16
    #                  [(2, 1), (0, 0), (0, 0)],  # 17
    #                  [(1, 2), (0, 0), (0, 0)],  # 18
    #                  [(0, 0), (0, 0), (0, 0)]  # 19
    #                  ]
    #

    OrderInputMes = [[],
                     [(0, 0), (0, 0), (0, 0)],  # 虚拟1
                     [(0, 1), (0, 0), (0, 0)],  # 2
                     [(0, 1), (1, 1), (0, 1)],  # 3
                     [(1, 1), (0, 0), (0, 0)],  # 4
                     [(1, 1), (1, 1), (0, 1)],  # 5
                     [(0, 1), (2, 1), (0, 0)],  # 6
                     [(3, 2), (0, 1), (0, 0)],  # 7
                     [(2, 2), (0, 0), (0, 0)],  # 8,
                     [(2, 1), (1, 1), (0, 1)],  # 9
                     [(3, 1), (0, 0), (0, 1)],  # 10
                     [(3, 1), (3, 1), (0, 0)],  # 11
                     [(3, 2), (0, 0), (0, 0)],  # 12
                     [(3, 1), (0, 0), (0, 0)],  # 13
                     [(3, 1), (4, 1), (0, 0)],  # 14
                     [(2, 1), (0, 0), (0, 0)],  # 15
                     [(2, 1), (0, 0), (0, 0)],  # 16
                     [(3, 1), (4, 1), (0, 0)],  # 17
                     [(1, 2), (0, 0), (0, 0)],  # 18
                     [(0, 0), (0, 0), (0, 0)]  # 19
                     ]

    VACP =[0,
                 0,  # 虚拟1
                 1.8,  # 2 特设外观检查 #供电
                 1,  # 3 特设座舱检查
                 1,  # 4 航电外观检查
                 1,  # 5 航电座舱检查
                 1.5,  # 6 充氧
                 2,  # 7 加油
                 1,  # 8 军械外观检查
                 1,  # 9 军械座舱检查
                 1,  # 10 机械座舱检查
                 1.5,  # 11 充氮
                 1, # 12 机械外观检查
                 1, # 13 发动机检查
                 1.2, # 14 机翼展开
                 2, # 15 挂弹
                 2, # 16 挂弹
                 1.2, # 17 收机翼
                 1.2, # 18 惯导
                 0 # 19
            ]


    OrderTime = [0,
                 0,  # 虚拟1
                 3,  # 2 特设外观检查
                 6,  # 3 特设座舱检查
                 3,  # 4 航电外观检查
                 6,  # 5 航电座舱检查
                 5,  # 6 充氧
                 4,  # 7 加油
                 5,  # 8 军械外观检查
                 13,  # 9 军械座舱检查
                 4,  # 10 机械座舱检查
                 4,  # 11 充氮
                 3,  # 12 机械外观检查
                 12,  # 13 发动机检查
                 8,  # 14 机翼展开
                 3,  # 15 挂弹
                 8,  # 16 挂弹
                 10,  # 17 收机翼
                 7, # 18 惯导
                 0 # 19
                 ]
    lowTime = 90  # 不能超过90 min
    HS = 3
    Lpk = [0 for _ in range(Human_resource_type)]
    for p in range(planeNum):
        for i in range(1,planeOrderNum+1):
            needRtype = OrderInputMes[i][0][0]
            needNums = OrderInputMes[i][0][1]
            dur = OrderTime[i]
            Lpk[needRtype] += HS*needNums*dur/lowTime

    Lpk = [int(i) for i in Lpk]
    total_Huamn_resource = Lpk

    # OrderInputMes = [[],
    #                  [(0, 0), (0, 0), (0, 0)],  # 虚拟1
    #                  [(0, 1), (0, 0), (0, 0)],  # 2
    #                  [(0, 1), (1, 1), (0, 1)],  # 3
    #                  [(0, 1), (0, 0), (0, 0)],  # 4
    #                  [(0, 1), (1, 1), (0, 0)],  # 5
    #                  [(0, 1), (0, 0), (0, 0)],  # 6
    #                  [(0, 2), (1, 1), (0, 1)],  # 7
    #                  [(0, 2), (0, 0), (0, 0)],  # 8,
    #                  [(0, 1), (0, 1), (0, 1)],  # 9
    #                  [(0, 1), (4, 1), (0, 0)],  # 10
    #                  [(0, 1), (3, 1), (0, 0)],  # 11
    #                  [(0, 2), (1, 1), (0, 1)],  # 12
    #                  [(0, 1), (0, 0), (0, 0)],  # 13
    #                  [(0, 1), (0, 0), (0, 1)],  # 14
    #                  [(0, 1), (2, 1), (0, 0)],  # 15
    #                  [(0, 1), (0, 0), (0, 0)],  # 16
    #                  [(0, 1), (0, 0), (0, 0)],  # 17
    #                  [(0, 2), (0, 0), (0, 0)],  # 18
    #                  [(0, 0), (0, 0), (0, 0)]  # 19
    #                  ]


    #17位 为了让虚拟从1开始
    sigma = 0.3
    shedule_num=0
    act_info={}


    cross = 0.5
    cross1 = 2.5
    MutationRate = 0.25
    MutationRatePmo = 0.05

    transferrate = 0.2
    transfer_iter = 50
    human_walk_speed = 800000000 #人员行走速度8 m/(in)

    populationnumber = 40
    ge = 15

    # 记录每一代的最优染色体
    recordBest = [Chromosome() for _ in range(ge+1)]
    # 记录每一代的最坏染色体
    recordBad = [Chromosome() for _ in range(ge + 1)]

    recordBestD = [Chromosome() for _ in range(ge+1)]
    # 记录每一代的最坏染色体
    recordBadD = [Chromosome() for _ in range(ge + 1)]

    threadNum = 1
    populationnumberson = populationnumber

    AgenarationIten = ge / 3
    GenarationIten = 0

    #保存每代染色体信息 父代
    AllFit = []
    AllFitSon = []
    AllFitFamily = []
    #vnsIter = -1

    resver_k1 = [ 0 for _ in range(ge)]
    resver_k2 = [ 0 for _ in range(ge)]
    #populationnumber*populationnumber
    slect_F_step_alone = [[] for _ in range(populationnumber)]
    # slect_F_step = [[] for _ in range(populationnumber)]

    Paternal = [[0,0] for _ in range(int(populationnumber/2))]
    #每一代的平均值
    Avufit = {}
    BestCmax = {}
    BestPr = {}
    BestEcmax = {}
    Bestzonghe = {}
    var ={}
    f = {}
    d = {}
    m = {}

    AverPopmove = 0
    AverPopTime = 0
    AverPopVar = 0
    Diversity = 0.0
    keyChainOrder = []
    #死锁辅助检查列表
    # dealLockList=[[0 for _ in range(Activity_num)] for _ in range(Activity_num)]

    bestHumanNumberTarget=[]

    Allactivity = []
    constraintHuman =[]
    constraintStation=[]
    constraintSpace = []

    humanNum = 0
    targetWeight =[1,0.3,0.1]
    boundUpper =[0,0]
    boundLowwer=[]





    AON=[]

    @classmethod
    def getTime(cls,i):
        # 定义每种任务的时间分布
        sigma = 0.3
        if i == 0:
            return 0
        elif i == 1:
            return 0
        elif i == 2:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc = cls.OrderTime[2], scale=sigma).rvs()
        elif i == 3:
            return stats.truncnorm((-0.8) / sigma, 0.8 / sigma, loc=cls.OrderTime[3], scale=sigma).rvs()
        elif i == 4:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[4], scale=sigma).rvs()
        elif i == 5:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[5], scale=sigma).rvs()
        elif i == 5:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[5], scale=sigma).rvs()
        elif i == 6:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[6], scale=sigma).rvs()
        elif i == 7:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[7], scale=sigma).rvs()

        elif i == 8:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[8], scale=sigma).rvs()
        elif i == 9:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[9], scale=sigma).rvs()

        elif i == 10:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[10], scale=sigma).rvs()
        elif i == 11:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[11], scale=sigma).rvs()

        elif i == 12:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[12], scale=sigma).rvs()
        elif i == 13:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[13], scale=sigma).rvs()
        elif i == 14:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[14], scale=sigma).rvs()

        elif i == 15:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[15], scale=sigma).rvs()
        elif i == 16:
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=cls.OrderTime[16], scale=sigma).rvs()
        elif i == 17:
            return 0
    @classmethod
    def my(cls):

        cls.AllFit=[]
        cls.AllFitSon=[]
        for i in range(cls.populationnumber):

            cls.AllFit.append(Chromosome())
            cls.AllFitSon.append(Chromosome())
            cls.AllFitFamily.append(Chromosome())
            cls.AllFitFamily.append(Chromosome())

        for i in range(cls.planeOrderNum):
            cls.keyChainOrder.append(set())

        num=0
        for i in range(len(cls.total_Huamn_resource)):
            cls.constraintHuman.append([])
            for j in range(cls.total_Huamn_resource[i]):
                num+=1
                cls.constraintHuman[i].append(num)
        cls.humanNum = num
        num = 0
        for i in range(len(cls.total_station_resource)):
            cls.constraintStation.append([])
            for j in range(cls.total_station_resource[i]):
                num+=1
                cls.constraintStation[i].append(num)

        num = 0
        for i in range(len(cls.total_space_resource)):
            cls.constraintSpace.append([])
            for j in range(cls.total_space_resource[i]):
                num+=1
                cls.constraintSpace[i].append(num)





    # import scipy.stats as stats
    # mu, sigma = 5, 0.7
    # lower, upper = mu - 2 * sigma, mu + 2 * sigma  # 截断在[μ-2σ, μ+2σ]
    # X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    # print(X.rvs())
    # print(X.rvs())
    #
    # x=FixedMes()
    # x.my()
    # print()







