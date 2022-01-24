from geocube import entities, sdk
from geocube.sdk.geocube_xarray import open_geocube


class TestXArray:
    def test_single_band(self):
        connection_params = sdk.ConnectionParams("127.0.0.1:8080")
        client = connection_params.new_client()
        r = client.list_records(name="S2B_MSIL1C_20190105T103429_N0207_R108_T32VNH_20190105T122413", with_aoi=True)[0]
        tile = entities.Tile.from_record(r, "epsg:32632", 200)
        tile.shape = (tile.shape[0], 10)
        instance = client.variable("NDVI").instance("master")
        collection = sdk.Collection.from_tile(tile, records=[r], instances=[instance])
        ds = open_geocube(collection, connection_params=connection_params, block_size=(256, 256))
        da = ds['NDVI:master']
        assert da[tile.shape[1]-1, ...].compute().shape == (tile.shape[0], 1)
        assert da[::2, 0].compute().shape == (tile.shape[1]//2, 1)
        assert da[:, :].compute().shape == (tile.shape[1], tile.shape[0], 1)

    def test_multiple_bands(self):
        connection_params = sdk.ConnectionParams("127.0.0.1:8080")
        client = connection_params.new_client()
        r = client.list_records(name="S2B_MSIL1C_20190118T104359_N0207_R008_T32UNG_20190118T123528", with_aoi=True)[0]
        tile = entities.Tile.from_record(r, "epsg:32632", 200)
        tile.shape = (tile.shape[0], 256)
        instance = client.variable("RGB").instance("master")
        collection = sdk.Collection.from_tile(tile, records=[r], instances=[instance])
        ds = open_geocube(collection, connection_params=connection_params, block_size=(256, 256))
        da = ds['RGB:master']
        assert da[tile.shape[1]-1, :, :].compute().shape == (tile.shape[0], 3, 1)
        assert da[::2, tile.shape[0]-1].compute().shape == (tile.shape[1]//2, 3, 1)
        assert da[:, :, 1:3].compute().shape == (tile.shape[1], tile.shape[0], 2, 1)
        assert da.argmax().compute().shape == ()
        assert ds.compute()['RGB:master'].shape == (tile.shape[1], tile.shape[0], 3, 1)

    def test_multiple_times(self):
        connection_params = sdk.ConnectionParams("127.0.0.1:8080")
        client = connection_params.new_client()
        rs = client.list_records(tags={'source': 'tutorial'}, with_aoi=True)
        tile = entities.Tile.from_record(rs[0], "epsg:32632", 200)
        tile.shape = (tile.shape[0], 256)
        instance = client.variable("RGB").instance("master")
        collection = sdk.Collection.from_tile(tile, records=rs, instances=[instance])
        ds = open_geocube(collection, connection_params=connection_params, block_size=(256, 256))
        da = ds['RGB:master']
        assert da[tile.shape[1]-1, :, :].compute().shape == (tile.shape[0], 3, 9)
        assert da[::2, tile.shape[0]-1].compute().shape == (tile.shape[1]//2, 3, 9)
        assert da[:, :, 1:3].compute().shape == (tile.shape[1], tile.shape[0], 2, 9)
        assert da[:, :, :, 1:3].compute().shape == (tile.shape[1], tile.shape[0], 3, 2)
        assert da.argmax().compute().shape == ()
        assert ds.compute()['RGB:master'].shape == (tile.shape[1], tile.shape[0], 3, 9)

    def test_multiple_variables(self):
        connection_params = sdk.ConnectionParams("127.0.0.1:8080")
        client = connection_params.new_client()
        rs = client.list_records(tags={'source': 'tutorial'}, with_aoi=True)
        tile = entities.Tile.from_record(rs[0], "epsg:32632", 200)
        tile.shape = (tile.shape[0], 256)
        instances = [client.variable("RGB").instance("master"), client.variable("NDVI").instance("master")]
        collection = sdk.Collection.from_tile(tile, records=rs, instances=instances)
        ds = open_geocube(collection, connection_params=connection_params, block_size=(256, 256))
        da = ds['RGB:master']
        assert da[tile.shape[1]-1, :, :].compute().shape == (tile.shape[0], 3, 10)
        assert da[::2, tile.shape[0]-1].compute().shape == (tile.shape[1]//2, 3, 10)
        assert da[:, :, 1:3].compute().shape == (tile.shape[1], tile.shape[0], 2, 10)
        assert da[:, :, :, 1:3].compute().shape == (tile.shape[1], tile.shape[0], 3, 2)
        assert da.argmax().compute().shape == ()
        assert ds.compute()['RGB:master'].shape == (tile.shape[1], tile.shape[0], 3, 10)
        da = ds['NDVI:master']
        assert da[tile.shape[1]-1, ...].compute().shape == (tile.shape[0], 10)
        assert da[::2, 0].compute().shape == (tile.shape[1]//2, 10)
        assert da[:, :].compute().shape == (tile.shape[1], tile.shape[0], 10)
