import warnings
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

import parse
from shapely import geometry
import geopandas as gpd

from geocube import utils
from geocube.pb import operations_pb2, geocube_pb2_grpc as geocube_grpc


class ExecutionLevel(Enum):
    SYNCHRONOUS = 0            # Job is done synchronously
    ASYNCHRONOUS = 1           # Job is done asynchronously, but without any pause
    STEP_BY_STEP_CRITICAL = 2  # Job is done asynchronously, step-by-step, pausing at every critical steps
    STEP_BY_STEP_MAJOR = 3     # Job is done asynchronously, step-by-step, pausing at every major steps
    STEP_BY_STEP_ALL = 4       # Job is done asynchronously, step-by-step, pausing at every steps


@dataclass
class Task:
    nb_containers: int
    nb_records: int
    nb_datasets: int
    coordinates: geometry.LinearRing


@dataclass
class Job:
    _stub:            geocube_grpc.GeocubeStub
    id:               str
    name:             str
    type:             str
    state:            str
    creation_time:    datetime
    last_update_time: datetime
    logs:             List[str]
    active_tasks:     int
    failed_tasks:     int
    execution_level:  ExecutionLevel
    waiting:          bool

    @classmethod
    def from_pb(cls, stub: geocube_grpc.GeocubeStub, pb_job: operations_pb2.Job):
        return Job(
            _stub=stub,
            id=pb_job.id,
            name=pb_job.name,
            type=pb_job.type,
            state=pb_job.state,
            creation_time=pb_job.creation_time.ToDatetime(),
            last_update_time=pb_job.last_update_time.ToDatetime(),
            logs=pb_job.logs,
            active_tasks=pb_job.active_tasks,
            failed_tasks=pb_job.failed_tasks,
            execution_level=pb_job.execution_level,
            waiting=pb_job.waiting,
        )

    @utils.catch_rpc_error
    def retry(self, force: bool = False):
        """
        Retry a failed job

        Parameters
        ----------
        force: TO BE USED CAUTIOUSLY: retry the current state of the job, whatever the state.
        It can be unpredictable. Should only be used if the job is stuck in a pending state.

        """
        self._stub.RetryJob(operations_pb2.RetryJobRequest(id=self.id, force_any_state=force))

    @utils.catch_rpc_error
    def cancel(self, force: bool = False):
        """ Cancel the job if possible
        force: TO BE USED CAUTIOUSLY: cancel the current state of the job, whatever the state.
        It can be unpredictable. Should only be used if the job is stuck in a pending state."""
        self._stub.CancelJob(operations_pb2.CancelJobRequest(id=self.id, force_any_state=force))

    @utils.catch_rpc_error
    def next(self):
        """ Start the next step (must be in "waiting" state) """
        if not self.waiting:
            raise Exception("Job must be in waiting state")
        self._stub.ContinueJob(operations_pb2.ContinueJobRequest(id=self.id))

    @utils.catch_rpc_error
    def refresh(self, log_page=0, log_limit=1000):
        """ Reload a job from server (inplace operation) """
        res = self._stub.GetJob(operations_pb2.GetJobRequest(id=self.id, log_page=log_page, log_limit=log_limit))
        self.__dict__ = Job.from_pb(self._stub, res.job).__dict__
        return self

    def tasks_from_logs(self) -> List[Task]:
        tasks = []
        for i, log in enumerate(self.logs):
            log_task = parse.search("Prepare {container:d} container(s) with {records:d} record(s) "
                                    "and {datasets:d} dataset(s) (geographic: {coordinates})", log)
            if log_task is not None:
                if i < 3:
                    warnings.warn("tasks_from_logs might have missed tasks. Please, reload job with more logs")
                # Parse coordinates
                coordinates = parse.findall("{lon:f} {lat:f}", log_task['coordinates'])
                coordinates = geometry.LinearRing([[p['lon'], p['lat']] for p in coordinates])

                tasks.append(Task(log_task['container'], log_task['records'], log_task['datasets'], coordinates))
        return tasks

    def deletion_job_from_logs(self) -> str:
        for log in self.logs:
            deletion_job = parse.search("Create a deletion job to delete {nb_datasets:d} dataset(s): {name:S}", log)
            if deletion_job is not None:
                return deletion_job["name"]
        return ""

    def plot_tasks(self):
        tasks = self.tasks_from_logs()
        if len(tasks) == 0:
            raise ValueError("Tasks not found from logs. Cannot display")
        base = utils.plot_aoi(gpd.GeoSeries([task.coordinates for task in tasks]))
        for task in tasks:
            center = task.coordinates.centroid
            base.text(center.x, center.y, f"{task.nb_records} rec\n{task.nb_datasets} ds", ha='center', va='center')
        base.set_title(f"Job '{self.name}'\n"
                       f"{len(tasks)} cells ({self.active_tasks} active tasks - {self.failed_tasks} failed)")
        return base

    def __repr__(self):
        return "Job {} ({})".format(self.name, self.id)

    def __str__(self):
        if len(self.logs) > 20:
            logs = f"[+{len(self.logs)-20}...]\n"+("      \n".join(self.logs[-20:]))
        else:
            logs = "      \n".join(self.logs)
        return "Job {} ({})\n" \
               "    type         {}\n" \
               "    state        {} {}\n" \
               "    creation     {}\n" \
               "    last_update  {}\n"\
               "    active_tasks {}\n"\
               "    failed_tasks {}\n"\
               "    execution    {}\n"\
               "    logs\n{}\n".format(self.name, self.id, self.type, self.state,
                                       "(waiting for user action)" if self.waiting else "",
                                       self.creation_time, self.last_update_time, self.active_tasks, self.failed_tasks,
                                       self.execution_level, logs)
