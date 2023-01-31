from geocube.entities import Tile


class TestTile:
    @staticmethod
    def assert_tile(tile, shape, transform):
        assert tile.shape == shape
        assert tile.transform.to_gdal() == transform

    def test_bbox(self):
        tile = Tile.from_bbox((0, 10, 5, 20), 4326, resolution=1)
        self.assert_tile(tile, (5, 10), (0.0, 1.0, 0.0, 20.0, 0.0, -1.0))

        tile = Tile.from_bbox((0, 10, 5, 20), 4326, resolution=(1, -1))
        self.assert_tile(tile, (5, 10), (0.0, 1.0, 0.0, 20.0, 0.0, -1.0))

        tile = Tile.from_bbox((0, 10, 5, 20), 4326, resolution=(1, 1))
        self.assert_tile(tile, (5, 10), (0.0, 1.0, 0.0, 10.0, 0.0, 1.0))

        tile = Tile.from_bbox((0, 10, 5, 20), 4326, resolution=5)
        self.assert_tile(tile, (1, 2), (0.0, 5.0, 0.0, 20.0, 0.0, -5.0))

        tile = Tile.from_bbox((0, 10, 5, 20), 4326, resolution=(5, 1))
        self.assert_tile(tile, (1, 10), (0.0, 5.0, 0.0, 10.0, 0.0, 1.0))

        tile = Tile.from_bbox((5, 10, 0, 20), 4326, resolution=(5, 1))
        self.assert_tile(tile, (1, 10), (0.0, 5.0, 0.0, 10.0, 0.0, 1.0))

        tile = Tile.from_bbox((0, 20, 5, 10), 4326, resolution=(5, 1))
        self.assert_tile(tile, (1, 10), (0.0, 5.0, 0.0, 10.0, 0.0, 1.0))
