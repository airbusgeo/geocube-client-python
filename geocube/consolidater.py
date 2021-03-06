import time
from datetime import datetime
from typing import Union, Dict, List

from geocube import Client, utils, entities
from geocube.pb import operations_pb2, records_pb2


class Consolidater(Client):

    @utils.catch_rpc_error
    def list_jobs(self, name_like: str = ""):
        """
        List jobs by name
        name_like: pattern of the name. * and ? are supported to match all or any character.
        """
        res = self.stub.ListJobs(operations_pb2.ListJobsRequest(name_like=name_like))
        return [entities.Job.from_pb(self.stub, r) for r in res.jobs]

    @utils.catch_rpc_error
    def job(self, name: str):
        """ Get job by name. Shortcut for ListJobs(name)[0]. Only few logs are loaded. """
        res = self.stub.ListJobs(operations_pb2.ListJobsRequest(name_like=name))
        if len(res.jobs) == 0:
            raise utils.GeocubeError("job", "NOT_FOUND", "with name: " + name)
        return entities.Job.from_pb(self.stub, res.jobs[0])

    @utils.catch_rpc_error
    def get_job(self, job_id: Union[str, entities.Job], log_page=0, log_limit=1000):
        """
        Get job by id.
        Logs are loaded by pages, because some big jobs have too many logs to fit in a gRPC response.
        """
        res = self.stub.GetJob(operations_pb2.GetJobRequest(id=entities.get_id(job_id),
                                                            log_page=log_page, log_limit=log_limit))
        return entities.Job.from_pb(self.stub, res.job)

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

    @utils.catch_rpc_error
    def remove_terminated_jobs(self, name_like: str = "", state: str = ""):
        """
        Remove all the jobs from the Geocube given a name pattern (by default, all terminated jobs)
        name_like: pattern of the name. * and ? are supported to match all or any character.
        state: state of the jobs to be removed.
        """
        self.stub.CleanJobs(operations_pb2.CleanJobsRequest(name_like=name_like, state=state))

    @utils.catch_rpc_error
    def consolidate(self,
                    job_name: str,
                    instance: Union[str, entities.VariableInstance],
                    layout: Union[str, entities.Layout],
                    records: Union[List[entities.RecordIdentifiers], None] = None,
                    tags: Union[Dict[str, str], None] = None,
                    from_time: Union[datetime, None] = None,
                    to_time: Union[datetime, None] = None,
                    execution_level: entities.ExecutionLevel = entities.ExecutionLevel.ASYNCHRONOUS):
        common = {
            "job_name":        job_name,
            "instance_id":     entities.get_id(instance),
            "layout_name":     entities.get_id(layout),
            "execution_level": execution_level.value,
        }

        if records is not None:
            req = operations_pb2.ConsolidateRequest(
                **common, records=records_pb2.RecordIdList(ids=entities.get_ids(records)))
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
