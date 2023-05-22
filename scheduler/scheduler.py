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
        # list_of_tasks = sorted(job.tasks.values(), key=lambda x: x.id, reverse=True) # sort tasks by priority
        for task in job.tasks.values():
            self.tasks_to_do[task.id] = task
        self.task_buffer = []
        self.currently_running_tasks = []
        self.currently_assigned_resoruces = [0 for _ in range(len(job.resources))]
        self.execution_history = []
        self.tasks_to_do_unmodified = copy.copy(self.tasks_to_do)
        self.no_resource_conflicts = 0
        self.no_tasks_executed = 0

    def has_next(self):
        if len(self.task_buffer) > 0:  # as long as there are entries in the task buffer, return true
            return True

        tasks = self._reschedule()  # if there are none left, try rescheduling
        if tasks is not None:
            self.task_buffer.extend(tasks)

        if len(self.task_buffer) > 0:
            return True
        else:
            return False  # looks like we're currently out of resources

    def get_next(self):
        assert len(self.task_buffer) > 0, "Don't call get_next() when the task_buffer is empty!"
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
        #ORM.Task.__init__(self)
        #self.original_task = task
        self.__dict__ = copy.copy(task.__dict__)  # Copys all values from the task to the current object
        self.original_task = task
        self.usedResources = []
        self.scheduler = scheduler
        self.started = 0
        self.finished = 0
        self.duration = 0
    # callback for marking a Task as completed. This is used to return bound resources to the pool.

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
