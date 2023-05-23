import abc
import copy
import ORM.ORM as ORM
from activity.Activitity import Order
from util.utils import Logger
__author__ = 'jules'


class Scheduler(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, job):
        self.job = job
        # 供给型资源，全局资源
        self.resource_pool = job.resources
        self.tasks_to_do = {}
        # 所有工序
        for task in job.tasks.values():
            self.tasks_to_do[task.id] = task
        self.task_buffer = []
        # 当前运行工序
        self.currently_running_tasks = []
        # 已经分配的资源
        self.currently_assigned_resoruces = [0 for _ in range(len(job.resources))]
        self.execution_history = []
        self.no_resource_conflicts = 0
        self.no_tasks_executed = 0

    def has_next(self):
        if len(self.task_buffer) > 0:
            return True
        #安排新任务
        tasks = self._reschedule()
        if tasks is not None:
            self.task_buffer.extend(tasks)

        if len(self.task_buffer) > 0:
            return True
        else:
            return False
    def get_next(self):
        assert len(self.task_buffer) > 0
        task = self.task_buffer.pop(0)
        self.currently_running_tasks.append(task)
        self.no_tasks_executed +=1
        return task
    def get_execution_history(self):
        return self.execution_history
    def has_work_left(self):
        return len(self.tasks_to_do) > 0

class ScheduledTask(Order):
    def __init__(self, task, scheduler):
        self.__dict__ = copy.copy(task.__dict__)
        self.original_task = task
        self.usedResources = []
        self.scheduler = scheduler
        self.started = 0
        self.finished = 0
        self.duration = 0

    def set_completed(self):
        self.scheduler.currently_running_tasks.remove(self)
        for resourceType in range(len(self.usedResources)):
            needNumber = self.usedResources[resourceType]
            self.scheduler.currently_assigned_resoruces[resourceType] -= needNumber
            self.scheduler.resource_pool[resourceType] += needNumber
        self.scheduler.execution_history.append(self)

    def set_started(self, now):
        self.started = now
    def set_finished(self, now):
        self.finished = now
        self.duration = self.finished - self.started
    @abc.abstractmethod
    def _reschedule(self):
        return None
