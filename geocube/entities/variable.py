from __future__ import annotations

import pprint
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Union

import grpc

from geocube.pb import operations_pb2, variables_pb2, geocube_pb2_grpc as geocube_grpc
from geocube import entities, utils


@dataclass
class _BaseVariable:
    stub: Union[geocube_grpc.GeocubeStub, None] = field(hash=False, compare=False)
    id: str
    name: str
    unit: str
    description: str
    dformat: entities.DataFormat
    bands: List[str]
    palette: str
    resampling_alg: entities.Resampling = None
    consolidation_params: entities.ConsolidationParams = None

    def __getstate__(self):
        stub, self.stub = self.stub, None
        d = asdict(self)
        self.stub = stub
        return d

    def __setstate__(self, d):
        self.__dict__ = d
        self.dformat = entities.DataFormat.from_dict(d["dformat"])
        self.resampling_alg = self.resampling_alg
        self.consolidation_params = entities.ConsolidationParams.from_dict(d["consolidation_params"])


class _ProxyVariable:
    def __init__(self, variable: _BaseVariable):
        self._variable = variable

    @property
    def client(self) -> geocube_grpc.GeocubeStub:
        return self._variable.stub

    @property
    def variable_id(self) -> str:
        return self._variable.id

    @property
    def variable_name(self) -> str:
        return self._variable.name

    @variable_name.setter
    def variable_name(self, value):
        self.__setter('name', value)

    @property
    def unit(self) -> str:
        return self._variable.unit

    @property
    def description(self) -> str:
        return self._variable.description

    @property
    def dformat(self) -> entities.DataFormat:
        return self._variable.dformat

    @property
    def bands(self) -> List[str]:
        return self._variable.bands

    @property
    def palette(self) -> str:
        return self._variable.palette

    @property
    def resampling_alg(self) -> entities.Resampling:
        return self._variable.resampling_alg

    @property
    @utils.catch_rpc_error
    def consolidation_params(self) -> entities.ConsolidationParams:
        if self._variable.consolidation_params is None and self.client is not None:
            req = operations_pb2.GetConsolidationParamsRequest(variable_id=self.variable_id)
            try:
                self._variable.consolidation_params = entities.ConsolidationParams.from_pb(
                    self.client.GetConsolidationParams(req).consolidation_params)
            except grpc.RpcError as e:
                e = utils.GeocubeError.from_rpc(e)
                if e.is_not_found():
                    self._variable.consolidation_params = None
                else:
                    raise

        return self._variable.consolidation_params

    @unit.setter
    def unit(self, value):
        self.__setter('unit', value)

    @description.setter
    def description(self, value):
        self.__setter('description', value)

    @resampling_alg.setter
    def resampling_alg(self, value):
        self.__setter('resampling_alg', value)

    @palette.setter
    def palette(self, value):
        self.__setter('palette', value)

    @consolidation_params.setter
    @utils.catch_rpc_error
    def consolidation_params(self, value):
        self._variable.consolidation_params = value
        req = operations_pb2.ConfigConsolidationRequest(variable_id=self.variable_id,
                                                        consolidation_params=self.consolidation_params.to_pb())
        self.client.ConfigConsolidation(req)

    @utils.catch_rpc_error
    def update(self, name: str = None, unit: str = None, description: str = None, palette: str = None,
               resampling_alg: entities.Resampling = entities.Resampling.undefined):
        """
        Some fields of the variable can be updated. All are optional.

        Parameters
        ----------
        name: new name
        unit: new unit
        description: new description
        palette: new palette
        resampling_alg: new resampling_alg
        """
        req = variables_pb2.UpdateVariableRequest(
            id=self.variable_id,
            name=utils.pb_string(name),
            unit=utils.pb_string(unit),
            description=utils.pb_string(description),
            palette=utils.pb_string(palette),
            resampling_alg=resampling_alg.value-1)

        self.client.UpdateVariable(req)

    def __setter(self, attr, new_value):
        old_value = self._variable.__getattribute__(attr)
        if old_value != new_value:
            if old_value is not None:
                self.update(**{attr: new_value})
            self._variable.__setattr__(attr, new_value)

    def __repr__(self):
        return "Variable {} ({})".format(self.variable_name, self.variable_id)

    def __str__(self):
        return "Variable {} ({})\n" \
               "    description      {}\n" \
               "    unit             {}\n" \
               "    dformat          {}\n" \
               "    bands            {}\n" \
               "    palette          {}\n" \
               "    resampling_alg   {}\n".format(self.variable_name, self.variable_id, self.description, self.unit,
                                                  self.dformat, self.bands, self.palette, self.resampling_alg)


@dataclass
class Instance:
    id:       str
    name:     str
    metadata: Dict[str, str]

    @classmethod
    def from_pb(cls, pb):
        return cls(
            id=pb.id,
            name=pb.name,
            metadata={key: value for key, value in pb.metadata.items()}
        )

    def __repr__(self):
        return "Instance {} ({})".format(self.name, self.id)

    def __str__(self):
        return "Instance {} ({})\n" \
               "    metadata\n{}"\
            .format(self.name, self.id, pprint.pformat(self.metadata, indent=7, width=1))


class Variable(_ProxyVariable):
    """
    >>> from geocube import Client
    >>> client = Client('127.0.0.1:8080')
    >>> vs = client.list_variables("test")
    >>> for v in vs:
    ...    v.delete()
    >>> profile = {'dformat': ('f8', -1, 0, 1), \
                   'bands': ['R', 'G', 'B']}
    >>> v = client.create_variable('test/vegetation/NDVI', **profile)
    >>> v2 = client.variable('test/vegetation/NDVI')
    >>> v.id==v2.id
    True
    >>> vi = v.instance('master')
    >>> v.description = "normalize difference vegetation index "
    >>> vi.instance_metadata = {'version': 'v1'}
    >>> vi2 = client.variable('test/vegetation/NDVI').instance('master')
    >>> vi.id == vi2.id
    True
    """
    @classmethod
    def from_pb(cls, stub: geocube_grpc.GeocubeStub, pb: variables_pb2.Variable):
        return cls(_BaseVariable(
            stub=stub,
            id=pb.id,
            name=pb.name,
            unit=pb.unit,
            description=pb.description,
            dformat=entities.DataFormat.from_pb(pb.dformat),
            bands=[b for b in pb.bands],
            palette=pb.palette,
            resampling_alg=entities.pb_resampling[pb.resampling_alg],
        ), {pbi.name: Instance.from_pb(pbi) for pbi in pb.instances})

    def __init__(self, base_variable, instances=None):
        super().__init__(base_variable)
        self.instances = instances if instances is not None else {}

    @property
    def id(self) -> str:
        return self.variable_id

    @property
    def name(self) -> str:
        return self.variable_name

    @utils.catch_rpc_error
    def instance(self, name=None) -> VariableInstance:
        """ Load the given instance

        Parameters
        ----------
        name: of the instance (or if None: the default instance if exists)

        Returns
        -------
        Specialization of the variable
        """
        if name is None:
            if len(self.instances) != 1:
                raise utils.GeocubeError("instance", "NOT EXISTS",
                                         "Default instance does not exist (or more than one instance is defined).")
            return VariableInstance(self, next(iter(self.instances.values())))

        if name not in self.instances:
            raise utils.GeocubeError("instance", "NOT EXISTS",
                                     "Instance does not exist. To instantiate a variable, use instantiate()")

        return VariableInstance(self, self.instances[name])

    @utils.catch_rpc_error
    def instantiate(self, name, metadata: Dict[str, str]) -> VariableInstance:
        """
        Instantiate the variable (create a specialization)
        Parameters
        ----------
        name: of the instance
        metadata: of the instance (e.g. processing parameters, version...) can be empty

        Returns
        -------
        The specialization of this variable
        """
        if name in self.instances:
            if metadata is not None and self.instances[name].metadata != metadata:
                raise utils.GeocubeError("instantiate", "ALREADY EXISTS",
                                         "Use instance({}).metadata = {} to update the metadata".format(name, metadata))
        else:
            req = variables_pb2.InstantiateVariableRequest(
                variable_id=self.id, instance_name=name, instance_metadata=metadata)
            self.instances[name] = Instance.from_pb(self.client.InstantiateVariable(req).instance)

        return VariableInstance(self, self.instances[name])

    @utils.catch_rpc_error
    def delete_instances(self, prefix=''):
        for instance in self.instances.values():
            if instance.name.startswith(prefix):
                req = variables_pb2.DeleteInstanceRequest(id=instance.id)
                self.client.DeleteInstance(req)

    @utils.catch_rpc_error
    def delete(self):
        self.delete_instances('')
        req = variables_pb2.DeleteVariableRequest(id=self.id)
        self.client.DeleteVariable(req)

    def config_consolidation(self, dformat: entities.DataFormat, exponent=1., bands_interleave=False,
                             compression: entities.Compression = entities.Compression.LOSSLESS, overviews_min_size=-1,
                             resampling_alg: entities.Resampling = entities.Resampling.near):
        self.consolidation_params = entities.ConsolidationParams(
            dformat=entities.DataFormat.from_user(dformat), exponent=exponent, bands_interleave=bands_interleave,
            compression=compression, overviews_min_size=overviews_min_size, resampling_alg=resampling_alg)

    def __str__(self):
        return "{}\n" \
               "Instances: {}\n"\
            .format(_ProxyVariable.__str__(self), self.instances)


class VariableInstance(_ProxyVariable, Instance):
    """ VariableInstance is an instantiation of a Variable.

    It inherits from Variable (except for id() and name() that are replaced by variable_id() and variable_name()
    to prevent confusion with id and name of the instance) and from Instance (except for id() and name() that are
    replaced by instance_id() and instance_name())
    """
    def __init__(self, variable: Variable,
                 instance: Instance):
        _ProxyVariable.__init__(self, variable._variable)
        self._instance = instance

    @property
    def instance_id(self) -> str:
        return self._instance.id

    @property
    def instance_name(self) -> str:
        return self._instance.name

    @property
    def metadata(self) -> Dict[str, str]:
        return self._instance.metadata

    @instance_name.setter
    @utils.catch_rpc_error
    def instance_name(self, name):
        if self.instance_name != name:
            req = variables_pb2.UpdateInstanceRequest(id=self.instance_id, name=utils.pb_string(name))
            self.client.UpdateInstance(req)
            self._instance.name = name

    @utils.catch_rpc_error
    def add_metadata(self, key: str, value: str):
        if key not in self.metadata or self.metadata[key] != value:
            req = variables_pb2.UpdateInstanceRequest(id=self.instance_id, add_metadata={key: value})
            self.client.UpdateInstance(req)
            self._instance.metadata[key] = value

    @utils.catch_rpc_error
    def del_metadata(self, key: str):
        if key not in self.metadata:
            req = variables_pb2.UpdateInstanceRequest(id=self.instance_id, del_metadata_keys=[key])
            self.client.UpdateInstance(req)
            del self._instance.metadata[key]

    def __repr__(self):
        return "VariableInstance {}:{} ({})".format(self.variable_name, self.instance_name, self.instance_id)

    def __str__(self):
        return "{}  {}".format(_ProxyVariable.__str__(self), self._instance.__str__())


@dataclass
class ColorPoint:
    val: float
    r:   int
    g:   int
    b:   int
    a:   int


@dataclass
class Palette:
    name: str
    points: List[ColorPoint]
