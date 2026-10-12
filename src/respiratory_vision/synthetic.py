from pathlib import Path
import json

import cv2
import numpy as np


def generate_breathing_video(
    output_path: str | Path,
    bpm: float = 18.0,
    duration_seconds: float = 20.0,
    fps: int = 10,
    width: int = 200,
    height: int = 150,
    amplitude_pixels: float = 5.0,
    seed: int = 7,
) -> dict:
    """Generate a non-clinical synthetic torso-motion video with known ground truth."""
    if bpm <= 0 or duration_seconds <= 0 or fps <= 1:
        raise ValueError("bpm, duration_seconds, and fps must be positive.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(seed)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError("Unable to initialize MP4 writer.")

    # Fixed textured torso canvas. Texture ensures optical-flow features.
    torso_w, torso_h = int(width * 0.54), int(height * 0.42)
    torso_x = (width - torso_w) // 2
    torso_y0 = int(height * 0.42)
    texture = rng.integers(70, 190, size=(torso_h, torso_w), dtype=np.uint8)
    texture = cv2.GaussianBlur(texture, (3, 3), 0)
    texture_bgr = cv2.cvtColor(texture, cv2.COLOR_GRAY2BGR)

    n_frames = int(round(duration_seconds * fps))
    hz = bpm / 60.0

    for i in range(n_frames):
        t = i / fps
        # Slowly changing background avoids an unrealistically static scene.
        base = 25 + 3 * np.sin(2 * np.pi * 0.03 * t)
        frame = np.full((height, width, 3), base, dtype=np.uint8)

        dy = int(round(amplitude_pixels * np.sin(2 * np.pi * hz * t)))
        torso_y = torso_y0 + dy

        # Add a subtle chest-like shape and textured region.
        y1, y2 = torso_y, torso_y + torso_h
        x1, x2 = torso_x, torso_x + torso_w
        if 0 <= y1 and y2 <= height:
            frame[y1:y2, x1:x2] = texture_bgr

        # Shoulder/chest boundary gives stable gradients.
        cv2.ellipse(
            frame,
            (width // 2, torso_y + torso_h // 3),
            (torso_w // 2, torso_h // 3),
            0, 180, 360,
            (205, 205, 205),
            2,
        )
        writer.write(frame)

    writer.release()

    metadata = {
        "synthetic": True,
        "clinical": False,
        "ground_truth_bpm": float(bpm),
        "duration_seconds": float(duration_seconds),
        "fps": int(fps),
        "width": int(width),
        "height": int(height),
        "motion_amplitude_pixels": float(amplitude_pixels),
        "seed": int(seed),
    }
    meta_path = output_path.with_suffix(".json")
    meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata
