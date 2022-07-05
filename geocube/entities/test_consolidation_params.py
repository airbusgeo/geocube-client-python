from dataclasses import asdict

from geocube import entities


class TestConsolidationParams:
    def test_from_dict(self):
        p = entities.ConsolidationParams(
            dformat=entities.DataFormat.from_user("u1"),
            exponent=1,
            compression=entities.Compression.LOSSLESS,
            overviews_min_size=255)
        d = asdict(p)
        p_from_dict = entities.ConsolidationParams.from_dict(d)
        assert p_from_dict == p

        entities.ConsolidationParams.from_dict(None)
