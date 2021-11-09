import time
from datetime import datetime
from typing import Union, Dict, List

from geocube import Client, utils, entities
from geocube.pb import layouts_pb2, operations_pb2, records_pb2


class Consolidater(Client):
    @utils.catch_rpc_error
    def create_layout(self, layout: entities.Layout):
        return self.stub.CreateLayout(layouts_pb2.CreateLayoutRequest(layout=layout.to_pb()))

    @utils.catch_rpc_error
    def list_layouts(self, name_like: str = "") -> List[entities.Layout]:
        res = self.stub.ListLayouts(layouts_pb2.ListLayoutsRequest(name_like=name_like))
        return [entities.Layout.from_pb(layout) for layout in res.layouts]

    @utils.catch_rpc_error
    def delete_layout(self, name: str = ""):
        self.stub.DeleteLayout(layouts_pb2.DeleteLayoutRequest(name=name))

    @utils.catch_rpc_error
    def create_grid(self, grid: entities.Grid):
        return self.stub.CreateGrid(layouts_pb2.CreateGridRequest(grid=grid.to_pb()))

    @utils.catch_rpc_error
    def list_grids(self, name_like: str = "") -> List[entities.Grid]:
        res = self.stub.ListGrids(layouts_pb2.ListGridsRequest(name_like=name_like))
        return [entities.Grid.from_pb(grid) for grid in res.grids]

    @utils.catch_rpc_error
    def delete_grid(self, name: str = ""):
        self.stub.DeleteGrid(layouts_pb2.DeleteGridRequest(name=name))

    @utils.catch_rpc_error
    def list_jobs(self, name_like: str = ""):
        res = self.stub.ListJobs(operations_pb2.ListJobsRequest(name_like=name_like))
        return [entities.Job.from_pb(self.stub, r) for r in res.jobs]

    @utils.catch_rpc_error
    def job(self, name: str = ""):
        res = self.stub.ListJobs(operations_pb2.ListJobsRequest(name_like=name))
        if len(res.jobs) == 0:
            raise utils.GeocubeError("job", "NOT_FOUND", "with name: " + name)
        return entities.Job.from_pb(self.stub, res.jobs[0])

    @utils.catch_rpc_error
    def get_job(self, job_id):
        res = self.stub.GetJob(operations_pb2.GetJobRequest(id=job_id))
        return entities.Job.from_pb(self.stub, res.job)

    def block_until_finish(self, job: entities.Job, wait_secs=15):
        prev_state = job.state
        while job.state not in ['DONE', 'FAILED', 'DONEBUTUNTIDY']:
            time.sleep(wait_secs)
            job = self.job(job.name)
            if job.state != prev_state:
                prev_state = job.state
                print(job.logs[-1])
            if job.waiting:
                job.next()

    @utils.catch_rpc_error
    def clean_terminated_jobs(self, name_like: str = "", state: str = ""):
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
                **common, records=records_pb2.RecordList(ids=entities.get_ids(records)))
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
