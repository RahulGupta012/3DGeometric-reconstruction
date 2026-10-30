
import numpy as np
import open3d as o3d

from src.config import (
    DATASET_NAME,
    # DATA_PATH,
    DEPTH_SCALE,
    FRAME_STEP,
    MAX_DEPTH,
    REDWOOD_PATH,
)


def get_frames():
    if DATASET_NAME == "redwood":
        color_dir = REDWOOD_PATH / "color"
        depth_dir = REDWOOD_PATH / "depth"
        if not color_dir.is_dir() or not depth_dir.is_dir():
            raise FileNotFoundError(
                "Redwood dataset must be extracted into "
                f"{REDWOOD_PATH} with color/ and depth/ directories."
            )

        color_paths = sorted(color_dir.glob("*.jpg"))
        depth_paths = sorted(depth_dir.glob("*.png"))
        if not color_paths or not depth_paths:
            raise FileNotFoundError(
                f"No Redwood color JPGs or depth PNGs found in {REDWOOD_PATH}."
            )
        if [path.stem for path in color_paths] != [
            path.stem for path in depth_paths
        ]:
            raise ValueError(
                f"Redwood color and depth frames do not match in {REDWOOD_PATH}."
            )

        return [
            (str(color_path), str(depth_path))
            for color_path, depth_path in zip(
                color_paths[::FRAME_STEP], depth_paths[::FRAME_STEP]
            )
        ]

    # rgb = np.loadtxt(DATA_PATH / "rgb.txt", dtype=str)
    # depth = np.loadtxt(DATA_PATH / "depth.txt", dtype=str)

    # depth_times = depth[:, 0].astype(float)
    # frames = []

    # for timestamp, rgb_path in rgb[::FRAME_STEP]:
    #     timestamp = float(timestamp)

    #     index = np.argmin(np.abs(depth_times - timestamp))

    #     if abs(depth_times[index] - timestamp) < 0.02:
    #         frames.append((
    #             str(DATA_PATH / rgb_path),
    #             str(DATA_PATH / depth[index, 1]),
    #         ))

    # return frames


def load_rgbd(rgb_path, depth_path, grayscale=False):
    color = o3d.io.read_image(str(rgb_path))
    depth = o3d.io.read_image(str(depth_path))

    return o3d.geometry.RGBDImage.create_from_color_and_depth(
        color,
        depth,
        depth_scale=DEPTH_SCALE,
        depth_trunc=MAX_DEPTH,
        convert_rgb_to_intensity=grayscale
    )
