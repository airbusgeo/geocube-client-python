import time
import warnings
from datetime import datetime
from typing import Union, Dict, List

from geocube import Client, utils, entities
from geocube.pb import operations_pb2, records_pb2


class Consolidater(Client):

    def list_jobs(self, name_like: str = ""):
        """
        List jobs by name
        name_like: pattern of the name. * and ? are supported to match all or any character.
        """
        return self._list_jobs(name_like)

    def job(self, name: str):
        """ Get job by name. Shortcut for ListJobs(name)[0]. Only few logs are loaded. """
        return self._job(name)

    def get_job(self, job_id: Union[str, entities.Job], log_page=0, log_limit=1000):
        """
        Get job by id.
        Logs are loaded by pages, because some big jobs have too many logs to fit in a gRPC response.
        """
        return self._get_job(job_id, log_page, log_limit)

    def wait_job(self, job: entities.Job, wait_secs=15, verbose=True):
        """
        Wait for the job to finish or fail.
        If the execution level is step-by-step, it will automatically continue.
        If verbose=True, the last log is printed every time a state change is detected.
        """
        prev_state = job.state
        while job.state not in ['DONE', 'FAILED', 'DONEBUTUNTIDY']:
            time.sleep(wait_secs)
            job = self.job(job.name)
            if job.state != prev_state:
                prev_state = job.state
                if verbose:
                    print(job.logs[-1])
            if job.waiting:
                job.next()

    def remove_terminated_jobs(self, name_like: str = "", state: str = ""):
        """
        Remove all the jobs from the Geocube given a name pattern (by default, all terminated jobs)
        name_like: pattern of the name. * and ? are supported to match all or any character.
        state: state of the jobs to be removed.
        """
        return self._remove_terminated_jobs(name_like, state)

    def consolidate(self,
                    job_name: str,
                    instance: Union[str, entities.VariableInstance],
                    layout: Union[str, entities.Layout],
                    *,
                    records: Union[List[entities.RecordIdentifiers], None] = None,
                    tags: Union[Dict[str, str], None] = None,
                    from_time: Union[datetime, None] = None,
                    to_time: Union[datetime, None] = None,
                    collapse_on_record: Union[entities.Record, str, None] = None,
                    execution_level: entities.ExecutionLevel = entities.ExecutionLevel.ASYNCHRONOUS):
        return self._consolidate(job_name, instance, layout, records, tags, from_time, to_time,
                                 collapse_on_record, execution_level)

    @utils.catch_rpc_error
    def _list_jobs(self, name_like: str):
        res = self.stub.ListJobs(operations_pb2.ListJobsRequest(name_like=name_like))
        return [entities.Job.from_pb(self.stub, r) for r in res.jobs]

    @utils.catch_rpc_error
    def _job(self, name: str):
        res = self.stub.ListJobs(operations_pb2.ListJobsRequest(name_like=name))
        if len(res.jobs) == 0:
            raise utils.GeocubeError("job", "NOT_FOUND", "with name: " + name)
        return entities.Job.from_pb(self.stub, res.jobs[0])

    @utils.catch_rpc_error
    def _get_job(self, job_id: Union[str, entities.Job], log_page, log_limit):
        res = self.stub.GetJob(operations_pb2.GetJobRequest(id=entities.get_id(job_id),
                                                            log_page=log_page, log_limit=log_limit))
        return entities.Job.from_pb(self.stub, res.job)

    @utils.catch_rpc_error
    def _remove_terminated_jobs(self, name_like: str, state: str):
        self.stub.CleanJobs(operations_pb2.CleanJobsRequest(name_like=name_like, state=state))

    @utils.catch_rpc_error
    def _consolidate(self,
                    job_name: str,
                    instance: Union[str, entities.VariableInstance],
                    layout: Union[str, entities.Layout],
                    records: Union[List[entities.RecordIdentifiers], None],
                    tags: Union[Dict[str, str], None],
                    from_time: Union[datetime, None],
                    to_time: Union[datetime, None],
                    collapse_on_record: Union[entities.Record, str, None],
                    execution_level: entities.ExecutionLevel):
        common = {
            "job_name":              job_name,
            "instance_id":           entities.get_id(instance),
            "layout_name":           entities.get_id(layout),
            "execution_level":       execution_level.value,
            "collapse_on_record_id": entities.get_id(collapse_on_record) if collapse_on_record is not None else "",
        }

        if records is not None:
            req = operations_pb2.ConsolidateRequest(
                **common, records=records_pb2.RecordIdList(ids=entities.get_ids(records)))
            if from_time is not None:
                warnings.warn("from_time is ignored if records is provided as argument to consolidate")
            if to_time is not None:
                warnings.warn("to_time is ignored if records is provided as argument to consolidate")
            if tags is not None:
                warnings.warn("tags is ignored if records is provided as argument to consolidate")
        else:
            from_time_pb = utils.pb_null_timestamp()
            if from_time is not None:
                from_time_pb.FromDatetime(from_time)
            to_time_pb = utils.pb_null_timestamp()
            if to_time is not None:
                to_time_pb.FromDatetime(to_time)
            req = operations_pb2.ConsolidateRequest(**common, filters=records_pb2.RecordFilters(
                tags=tags, from_time=from_time_pb, to_time=to_time_pb
            ))
        return self.get_job(self.stub.Consolidate(req).job_id)