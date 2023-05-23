__author__ = 'jules'

import copy
from collections import defaultdict

import networkx as nx

from scheduler.scheduler import Scheduler, ScheduledTask
from util.utils import UnfeasibleScheduleException
"""
This class represents ABPolicies. They are also known as priority lists.
"""
class ABPolicy(Scheduler):
    def __init__(self, job, newAV):
        super(ABPolicy, self).__init__(job)
        self.tasks = sorted(job.tasks.values(), key=lambda x:x.es)
        self.order_list = copy.copy([task.id for task in self.tasks])
        self.alreadyC=[]

        self.adj = newAV
        self.G = nx.DiGraph()
        self.G_T = nx.DiGraph()
        self.pre = defaultdict(lambda: [])
        for i in range(0,len(self.adj)):
            for j in self.adj[i]:
                self.G.add_edge(i,j)
                self.G_T.add_edge(j,i)

        # 新的任务网络
        for edges in newAV:
            fromid = edges[0]
            toid = edges[1]
            self.pre[toid].append(fromid)
    def _reschedule(self):
        new_tasks = []

        for task_id in self.order_list:
            # 必须满足紧前工序已完成
            if self.choose(task_id):
               if task_id in self.tasks_to_do.keys():
                 new_task = self.allocate_resources(self.tasks_to_do[task_id])
                 if new_task is not None:
                     new_tasks.append(new_task)
                     del self.tasks_to_do[task_id]
                 else:
                     break

        if len(new_tasks) == 0 and len(self.currently_assigned_resoruces) == 0 and len(self.tasks_to_do) != 0:
            raise UnfeasibleScheduleException()
        return new_tasks
    def allocate_resources(self, task):

        scheduled_task = ScheduledTask(task, self)
        temp_reserved_resources = [0 for _ in range(len(scheduled_task.resourceRequestS))]

        for resourceType in range(len(scheduled_task.resourceRequestS)):
                # 数量
                needNumber = scheduled_task.resourceRequestS[resourceType]
                if needNumber > 0:
                    if (self.resource_pool[resourceType] - needNumber) >= 0:
                        # 试分配资源
                        self._temp_allocate(temp_reserved_resources, resourceType, needNumber)
                    else:
                        self.no_resource_conflicts += 1
                        return self._cleanup_failed_allocation(temp_reserved_resources)
        # 记录
        scheduled_task.usedResources = temp_reserved_resources
        # 记录当前所有已分配资源
        for type in range(len(temp_reserved_resources)):
            self.currently_assigned_resoruces[type] += temp_reserved_resources[type]
        # print(finishtask)
        # print(thisPre)
        return scheduled_task

    def _cleanup_failed_allocation(self, already_allocated):
        for resourceType in range(len(already_allocated)):
                needNumber = already_allocated[resourceType]
                self.resource_pool[resourceType] += needNumber
        return None

    def _temp_allocate(self, temp_allocation_pool, resourceType, needNumber):

        temp_allocation_pool[resourceType] += needNumber
        self.resource_pool[resourceType] -= needNumber

    def choose(self,task_id):
        thisPre = self.pre[task_id]

        # 如果要改成开始-开始，就可以改这里
        # 改成self.current_running_task
        finishtask = [t.id for t in self.execution_history]

        for preorder in thisPre:
            if preorder not in finishtask:
                return False
        return True

