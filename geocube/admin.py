from typing import List, Union, Dict, Tuple

from geocube import Client, utils, entities
from geocube.pb import admin_pb2, admin_pb2_grpc


class Admin(Client):
    def __init__(self, uri: str, secure: bool = False, api_key: str = "", verbose: bool = True):
        """
        Initialise the connexion to the Geocube Server

        Parameters
        ----------
        uri: of the Geocube Server
        secure: True to use a TLS Connexion
        api_key: (optional) API Key if Geocube Server is secured using a bearer authentication
        verbose: display the version of the Geocube Server
        """
        super().__init__(uri, secure, api_key, verbose)
        self.admin_stub = admin_pb2_grpc.AdminStub(self._channel)

    @utils.catch_rpc_error
    def admin_tidy(self, aois: bool = False, records: bool = False, variables: bool = False, instances: bool = False,
                   containers: bool = False, consolidation_params: bool = False, simulate: bool = True):
        """
        Admin function to tidy the Geocube Database.
        Remove all the entities that are not linked to any dataset.
        Should be used with caution when no ingestion or indexation task is in progress.

        Parameters
        ----------
        aois: remove the pending AOI
        records: remove the pending Records
        variables: remove the pending Variables
        instances: remove the pending Instances
        containers: remove the pending Containers
        consolidation_params: remove the pending ConsolidationParams
        simulate: if True no operation is performed. Only the number of entities that would have been deleted
        """
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
    def admin_update_datasets(self, instance: Union[str, entities.VariableInstance],
                              records: List[Union[str, entities.Record]],
                              dformat: Union[Dict, Tuple, str], min_out: float, max_out: float,
                              exponent: float, simulate: bool):
        """
        Admin function to update some sensitive information of datasets referenced by an instance and a list of records

        Parameters
        ----------
        instance: select the datasets that are referenced by this instance
        records:select the datasets that are referenced by these records
        dformat: new dataformat
        min_out: new min_out
        max_out: new max_out
        exponent: new exponent
        simulate: if True, no operation is performed. Only display the datasets that would have been updated.
        """
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
    def admin_delete_datasets(self, instances: List[Union[str, entities.VariableInstance]],
                              records: List[Union[str, entities.Record]],
                              execution_level: entities.ExecutionLevel = entities.ExecutionLevel.SYNCHRONOUS)\
            -> entities.Job:
        """
        Admin function to delete datasets that are referenced by a list of instances and a list of records.
        This function is provided without any guaranties of service continuity.
        In the future, a secured function will be provided to safely delete datasets.

        Parameters
        ----------
        instances: select all the datasets referenced by these instances.
        records:select all the datasets referenced by these records.
        execution_level: see entities.ExecutionLevel.
        """
        res = self.admin_stub.DeleteDatasets(admin_pb2.DeleteDatasetsRequest(
            execution_level=execution_level.value,
            instance_ids=entities.get_ids(instances), record_ids=entities.get_ids(records)))

        return entities.Job.from_pb(self.stub, res.job)
