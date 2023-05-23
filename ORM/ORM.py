import math
import pickle
import numpy as np
from enum import Enum
from read import data
from conM.FixedMess import FixedMes
import scipy.stats as stats
class DistributionType(Enum):
    FIXED = 1
    FITTED = 2
    PHASE = 3
    PRECOMPUTED = 4
class Job(object):
    def __init__(self):
        # 读取所有任务数据
        self.tasks = {}
        # 只考虑供给型资源
        self.resources = FixedMes.total_renew_resource
        # 这个是能力匹配的，之后可以考虑？
        self.capabilities = {}

        self.already_initialized = False
class Task:
    """
    representation of a task. For details see ER diagram
    """
    def __init__(self):
        self.name = ""
        self.mean = 0.0  # in seconds
        self.deviation = 0.0  # in seconds
        self.taskId = 0
        self.priority = 0
        self.required_resources = []
        self.execution_history = []

    def initialize(self,taskid):
        # if we have historical data, use this to sample the distribution
        self.taskId = taskid

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
            return stats.truncnorm((-0.5) / sigma, 0.5 / sigma, loc=FixedMes.OrderTime[19], scale=sigma).rvs()
        elif i == 20:
            return 0



class RequiredResource(object):
    """
    Meta Class used to describe a requirement for a device which needs the capabilities specified
    in the required_capabilities list.
    """

    def __init__(self):
        self.name = ""
        self.number_required = 0
        self.required_capabilities = []
        self.is_testbed = False
        self.fulfilled_by = []

class Capability(object):
    def __init__(self):
        self.id = ""
        self.name = ""
        self.attributes = []


class Attribute(object):
    def __init__(self):
        self.id = ""
        self.name = ""
        self.value = ""


