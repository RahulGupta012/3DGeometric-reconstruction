import argparse
from pathlib import Path

import cv2


BASE_DIR = Path(__file__).resolve().parents[1]


def create_video(color_dir, output_path, fps):
    if not color_dir.is_dir():
        raise FileNotFoundError(f"Redwood color directory not found: {color_dir}")

    frames = sorted(color_dir.glob("*.jpg"))
    if not frames:
        raise FileNotFoundError(f"No JPG frames found in {color_dir}")

    first_image = cv2.imread(str(frames[0]))
    if first_image is None:
        raise ValueError(f"Could not read image: {frames[0]}")

    height, width = first_image.shape[:2]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    video = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )
    if not video.isOpened():
        raise RuntimeError(f"Could not create video: {output_path}")

    try:
        for frame_path in frames:
            image = cv2.imread(str(frame_path))
            if image is None:
                raise ValueError(f"Could not read image: {frame_path}")
            if image.shape[:2] != (height, width):
                raise ValueError(
                    f"Unexpected image dimensions in {frame_path}: "
                    f"{image.shape[1]}x{image.shape[0]}, expected {width}x{height}"
                )
            video.write(image)
    finally:
        video.release()

    print(f"Total frames: {len(frames)}")
    print(f"Video resolution: {width} x {height}")
    print(f"Video FPS: {fps}")
    print(f"Saved video: {output_path.resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description="Create an MP4 video from the Redwood color frames."
    )
    parser.add_argument(
        "--color-dir",
        type=Path,
        default=BASE_DIR / "RedwoodIndoorLivingRoom1" / "color",
        help="Directory containing the Redwood JPG color frames.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=BASE_DIR / "outputs" / "redwood_dataset_video.mp4",
        help="Path for the generated MP4 video.",
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=30,
        help="Frames per second for the output video.",
    )
    args = parser.parse_args()

    if args.fps <= 0:
        parser.error("--fps must be greater than zero.")

    create_video(args.color_dir, args.output, args.fps)


if __name__ == "__main__":
    main()
