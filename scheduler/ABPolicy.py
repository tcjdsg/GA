__author__ = 'jules'

from scheduler.scheduler import Scheduler, ScheduledTask
from util.utils import UnfeasibleScheduleException
"""
This class represents ABPolicies. They are also known as priority lists.
"""
class ABPolicy(Scheduler):

    def __init__(self, job, order_list = None):
        super(ABPolicy, self).__init__(job)
        if order_list is not None:
            self.order_list = order_list
        else:
            self.order_list = [job.id in self.job.to_run.values()]

    def _reschedule(self):
        new_tasks = []

        for task_id in self.order_list:
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

    def choose(self, newPre, task_id):
        pre = newPre[task_id]
        for i in pre:
            if i in self.order_list:
                return False
        return True

