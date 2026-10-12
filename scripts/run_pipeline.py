import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt

from respiratory_vision import PipelineConfig, RespiratoryEstimator


def main():
    parser = argparse.ArgumentParser(description="Estimate respiratory rate from RGB video.")
    parser.add_argument("--video", required=True)
    parser.add_argument("--output", default="outputs/result.json")
    parser.add_argument("--plot", default="outputs/signal.png")
    parser.add_argument("--interactive-roi", action="store_true")
    parser.add_argument("--min-bpm", type=float, default=6.0)
    parser.add_argument("--max-bpm", type=float, default=48.0)
    args = parser.parse_args()

    config = PipelineConfig(min_bpm=args.min_bpm, max_bpm=args.max_bpm)
    result = RespiratoryEstimator(config).analyze(
        args.video,
        interactive_roi=args.interactive_roi,
    )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    fig = plt.figure(figsize=(9, 4.5))
    ax = fig.add_subplot(111)
    ax.plot(result["timestamps_seconds"], result["filtered_signal"])
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Normalized respiratory motion")
    ax.set_title(
        f"Estimated respiratory rate: {result['estimate']['bpm']:.2f} BPM "
        f"(confidence {result['estimate']['confidence']:.2f})"
    )
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    plot = Path(args.plot)
    plot.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(plot, dpi=160)
    plt.close(fig)

    print(json.dumps({
        "estimated_bpm": result["estimate"]["bpm"],
        "confidence": result["estimate"]["confidence"],
        "result_json": str(out),
        "signal_plot": str(plot),
    }, indent=2))


if __name__ == "__main__":
    main()
