import warnings
from datetime import datetime
from typing import List, Union, Dict, Tuple

from geocube import utils, entities, Consolidater
from geocube.pb import admin_pb2, admin_pb2_grpc
from geocube.stub import Stub


class Admin(Consolidater):
    def __init__(self, uri: str, secure: bool = False, api_key: str = "", verbose: bool = True):
        """
        Initialise the connexion to the Geocube Server

        Args:
            uri: of the Geocube Server
            secure: True to use a TLS Connexion
            api_key: (optional) API Key if Geocube Server is secured using a bearer authentication
            verbose: display the version of the Geocube Server
        """
        super().__init__(uri, secure, api_key, verbose)
        self.admin_stub = Stub(admin_pb2_grpc.AdminStub(self._channel))

    def set_timeout(self, timeout_sec: float):
        super().set_timeout(timeout_sec)
        self.admin_stub.timeout = timeout_sec

    def admin_tidy(self, aois: bool = False, records: bool = False, variables: bool = False, instances: bool = False,
                   containers: bool = False, consolidation_params: bool = False, simulate: bool = True):
        """
        Admin function to tidy the Geocube Database.
        Remove all the entities that are not linked to any dataset.
        Should be used with caution when no ingestion or indexation task is in progress.

        Args:
            aois: remove the pending AOI
            records: remove the pending Records
            variables: remove the pending Variables
            instances: remove the pending Instances
            containers: remove the pending Containers
            consolidation_params: remove the pending ConsolidationParams
            simulate: if True no operation is performed. Only the number of entities that would have been deleted
        """
        return self._admin_tidy(aois, records, variables, instances, containers, consolidation_params, simulate)

    def admin_update_datasets(self, instance: Union[str, entities.VariableInstance],
                              records: List[Union[str, entities.Record]],
                              dformat: Union[Dict, Tuple, str], min_out: float, max_out: float,
                              exponent: float, simulate: bool):
        """
        Admin function to update some sensitive information of datasets referenced by an instance and a list of records

        Args:
            instance: select the datasets that are referenced by this instance
            records: select the datasets that are referenced by these records
            dformat: new dataformat
            min_out: new min_out
            max_out: new max_out
            exponent: new exponent
            simulate: if True, no operation is performed. Only display the datasets that would have been updated.
        """
        self._admin_update_datasets(instance, records, dformat, min_out, max_out, exponent, simulate)

    def admin_delete_datasets(self, instances: List[Union[str, entities.VariableInstance]],
                              records: List[Union[str, entities.Record]],
                              file_patterns: List[str] = None,
                              execution_level: entities.ExecutionLevel = entities.ExecutionLevel.STEP_BY_STEP_CRITICAL,
                              job_name: str = None, allow_empty_instances=False, allow_empty_records=False) \
            -> entities.Job:
        """
        Admin function to delete datasets that are referenced by a list of instances and a list of records.
        This function is provided without any guaranties of service continuity.
        In the future, a secured function will be provided to safely delete datasets.

        Args:
            instances: select all the datasets referenced by these instances.
            records: select all the datasets referenced by these records.
            file_patterns: select all the datasets with on of the given file patterns
                (support * and ? for all or any characters and trailing (?i) for case-insensitiveness)
            execution_level: see entities.ExecutionLevel.
            job_name: [optional] gives a name to the job, otherwise, a name will be automatically generated
            allow_empty_instances: [optional] allows instances to be empty.
                @warning It means that the job will delete all the instances for the given records.
            allow_empty_records: [optional] allows records to be empty.
                @warning It means that the job will delete all the records for the given instances.
        """
        return self._admin_delete_datasets(instances, records, file_patterns,  execution_level,
                                           job_name, allow_empty_instances, allow_empty_records)

    @utils.catch_rpc_error
    def _admin_tidy(self, aois: bool, records: bool, variables: bool, instances: bool,
                    containers: bool, consolidation_params: bool, simulate: bool):
        res = self.admin_stub.TidyDB(admin_pb2.TidyDBRequest(
            PendingAOIs=aois, PendingRecords=records, PendingVariables=variables, PendingInstances=instances,
            PendingContainers=containers, PendingParams=consolidation_params, Simulate=simulate
        ))
        if simulate:
            print("Simulation:")

        print("{} aois deleted\n"
              "{} records deleted\n"
              "{} variables deleted\n"
              "{} instances deleted\n"
              "{} containers deleted\n"
              .format(res.NbAOIs, res.NbRecords, res.NbVariables, res.NbInstances, res.NbContainers))

    @utils.catch_rpc_error
    def _admin_update_datasets(self, instance: Union[str, entities.VariableInstance],
                               records: List[Union[str, entities.Record]],
                               dformat: Union[Dict, Tuple, str], min_out: float, max_out: float,
                               exponent: float, simulate: bool):
        res = self.admin_stub.UpdateDatasets(admin_pb2.UpdateDatasetsRequest(
            simulate=simulate, instance_id=entities.get_id(instance),
            record_ids=entities.get_ids(records),
            dformat=entities.DataFormat.from_user(dformat).to_pb(),
            real_min_value=min_out, real_max_value=max_out, exponent=exponent))
        if simulate:
            print("Simulation:")

        for r, count in res.results.items():
            print("{} : {}\n".format(r, count))

    @utils.catch_rpc_error
    def _admin_delete_datasets(self, instances: List[Union[str, entities.VariableInstance]],
                               records: List[Union[str, entities.Record]],
                               file_patterns: List[str],
                               execution_level: entities.ExecutionLevel,
                               job_name: str, allow_empty_instances, allow_empty_records) \
            -> entities.Job:
        if len(records) == 0 and not allow_empty_records:
            raise ValueError("DeleteDataset: records is empty, but it has not been allowed. "
                             "Empty records means that all the datasets for the given instances are about to be "
                             "deleted. If this is what is wanted, please set allow_empty_records=True")
        if len(instances) == 0 and not allow_empty_instances:
            raise ValueError("DeleteDataset: instances is empty, but it has not been allowed. "
                             "Empty instances means that all the datasets for the given records are about to be "
                             "deleted. If this is what is wanted, please set allow_empty_instances=True")

        if file_patterns is not None:
            if isinstance(file_patterns, str):
                file_patterns = [file_patterns]
            assert isinstance(file_patterns, list)

        if len(records) == 0 and len(instances) == 0:
            warnings.warn("this job may be about to delete the whole database")
            if execution_level == entities.ExecutionLevel.ASYNCHRONOUS or \
                    execution_level == entities.ExecutionLevel.SYNCHRONOUS:
                raise ValueError("I cannot allow that in a non-interactive execution_level. "
                                 "Please use execution_level == entities.ExecutionLevel.STEP_BY_STEP_CRITICAL.")

        res = self.admin_stub.DeleteDatasets(admin_pb2.DeleteDatasetsRequest(
            job_name=job_name if job_name is not None else f"Deletion_{datetime.now()}_{len(records)}_records",
            execution_level=execution_level.value,
            instance_ids=entities.get_ids(instances), record_ids=entities.get_ids(records),
            dataset_patterns=file_patterns)
        )

        return entities.Job.from_pb(self.stub, res.job)
