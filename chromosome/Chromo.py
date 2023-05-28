import numpy as np


class Chromosome():
    def __init__(self):
        self.codes = []
        self.WorkTime = 999999999
        self.variance = 9999.0
        self.movetime = 9999.0
        self.num = 154

        #记录每个工序的开始时间
        self.activityES = [0.0 for i in range(self.num)]
        #记录每个工序的结束时间
        self.activityEF = [0.0 for i in range(self.num)]
        #
        self.DVPC = 0

        self.ForCluster = [0.0,0.0]

        self.Maxfagiue = 0
        self.Ecmax = 100
        self.Pr = 0.0
        self.np=0
        self.sp=[]

        self.f=None       #适应度
        self.rank = -1    #用于多目标
        self.crowding_distance = -1
        self.zonghe = 9999999999
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def setcodes(self,codes):
            self.codes=codes
    def __gt__(self, other):
        if self.rank > other.rank:
            return True
        if self.rank==other.rank and self.crowding_distance < other.crowding_distance:
            return True
        return  False

    def indices(self):
        """
        Returns a mapping from job -> idx in the schedule. Unscheduled
        jobs have index +inf.
        """
        indices = np.full(len(self.codes), 0, dtype=int)

        for idx, job in enumerate(self.codes):
            id = job[0]
            indices[id] = idx
        return indices

    def setf(self):

        self.zonghe = 10**7*(1.0-self.Pr) + self.Ecmax

        # self.newf =[self.Ecmax,self.Pr,self.WorkTime]
        self.f = [self.Pr, self.Ecmax]
        return self.f
    def setDVPU(self,bestEF):
        for i in range(len(bestEF)):
            self.DVPC += abs(self.activityEF[i]-bestEF[i])





