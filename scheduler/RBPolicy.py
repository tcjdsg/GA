__author__ = 'jules'

from collections import defaultdict

import networkx as nx

from scheduler.scheduler import Scheduler,ScheduledTask
from util.utils import UnfeasibleScheduleException
import copy
"""
This class represents ABPolicies. They are also known as priority lists.
"""
class RBPolicy(Scheduler):

    def __init__(self, job, newAV ):
        super(RBPolicy, self).__init__(job)
        self.tasks = sorted(job.tasks.values(), key=lambda x:x.es)
        self.order_list = copy.copy([task.id for task in self.tasks])

        self.adj = newAV
        self.G = nx.DiGraph()#Create a networkx graph object
        self.G_T = nx.DiGraph()#Create a networkx graph object
        self.pre = defaultdict(lambda: [])
        for i in range(0,len(self.adj)):
            for j in self.adj[i]:
                self.G.add_edge(i,j)
                self.G_T.add_edge(j,i)

        for edges in newAV:
            fromid = edges[0]
            toid = edges[1]
            self.pre[toid].append(fromid)

    def _reschedule(self):
        new_tasks = []
        tasks_to_remove = []
        for task_id in self.order_list:
            if self.choose(self.pre,task_id):
                new_task = self.allocate_resources(self.tasks_to_do[task_id])
                if new_task != None:
                    new_tasks.append(new_task)
                    del self.tasks_to_do[task_id]
                    tasks_to_remove.append(task_id)

        [self.order_list.remove(task) for task in tasks_to_remove]
        if len(new_tasks) > 0:
            return new_tasks


    def allocate_resources(self, task):

        scheduled_task = ScheduledTask(task, self)
        temp_reserved_resources = [0 for _ in range(len(scheduled_task.resourceRequestS))]

        for resourceType in range(len(scheduled_task.resourceRequestS)):
                needNumber = scheduled_task.resourceRequestS[resourceType]
                if needNumber > 0:
                    if (self.resource_pool[resourceType] - needNumber) >= 0:
                        self._temp_allocate(temp_reserved_resources, resourceType, needNumber)
                    else:  # the fix assigned equipment is not available. we can return directly
                        self.no_resource_conflicts += 1
                        return self._cleanup_failed_allocation(temp_reserved_resources)

        scheduled_task.usedResources = temp_reserved_resources
        for type in range(len(temp_reserved_resources)):
            self.currently_assigned_resoruces[type] += temp_reserved_resources[type]
        return scheduled_task

    def _cleanup_failed_allocation(self, already_allocated):
        for resourceType in range(len(already_allocated)):
                needNumber = already_allocated[resourceType]
                self.resource_pool[resourceType] += needNumber
        return None

    def _temp_allocate(self, temp_allocation_pool, resourceType, needNumber):

        temp_allocation_pool[resourceType] += needNumber
        self.resource_pool[resourceType] -= needNumber

    def choose(self,newPre,task_id):
        pre = newPre[task_id]
        for i in pre:
            if i in self.order_list:
                return False
        return True


