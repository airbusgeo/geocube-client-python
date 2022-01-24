import pickle

from geocube import entities
from geocube.entities.variable import _BaseVariable, Instance


class TestVariable:
    def test_picklable(self):
        v = entities.Variable(_BaseVariable(
            stub=None,
            id="fake",
            name="test",
            unit="no",
            description="for_test",
            dformat=entities.DataFormat.from_user(("f4", 0, 1, -1)),
            bands=["first", "second"],
            palette="palette",
            resampling_alg=entities.Resampling.bilinear),
            instances=[Instance(f"fake_id{i}", f"fake_name{i}", {"fake_metadata": f"{i}"}) for i in range(3)])
        # consolidation params is excluded as client is not defined
        v_from_pickle = pickle.loads(pickle.dumps(v))
        assert str(v_from_pickle) == str(v)

        # assert v_from_pickle == v => does not work...
