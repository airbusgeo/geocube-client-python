import os
from typing import List

import affine
import numpy as np
os.environ["GDAL_DISABLE_READDIR_ON_OPEN"] = "EMPTY_DIR"


def timeserie_to_animation(images: List[np.array], gif_name: str, duration=0.2, legend: List[str] = None):
    """
    image = (np.clip(image, 0, 1)*255).astype("uint8")
    """
    import imageio
    from PIL import ImageDraw, Image
    with imageio.get_writer(gif_name, mode='I', duration=duration) as writer:
        for i, image in enumerate(images):
            if legend is not None:
                if image.shape[2] == 1:
                    image = image[:, :, 0]
                    c = 255
                else:
                    c = (255, 255, 255)
                pilim = Image.fromarray(image)
                d = ImageDraw.Draw(pilim)
                d.text((10, 10), legend[i], fill=c)
                image=np.array(pilim)
            writer.append_data(image)


def image_to_geotiff(image: np.ndarray, transform: affine.Affine, projection: str, no_data: float, filename: str):
    import rasterio
    if len(image.shape) == 2:
        image = np.expand_dims(image, 0)
    elif image.shape[0] > 4:
        image = np.moveaxis(image, -1, 0)

    meta = {'driver': 'GTiff',
            'dtype': image.dtype.name,
            'nodata': no_data,
            'count': image.shape[0],
            'height': image.shape[1],
            'width': image.shape[2],
            'crs': projection,
            'transform': transform,
            'tiled': False,
            'interleave': 'band'}

    with rasterio.open(filename, 'w', **meta) as dst:
        dst.write(image)
