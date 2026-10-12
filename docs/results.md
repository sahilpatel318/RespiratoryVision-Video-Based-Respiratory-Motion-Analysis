# Results

This repository includes a reproducible synthetic benchmark and one packaged sample video.

Run:

```bash
python scripts/evaluate_synthetic.py --output outputs/synthetic_benchmark.csv
```

The benchmark generates multiple non-clinical videos with known sinusoidal breathing motion, analyzes them using the exact same OpenCV pipeline, and writes per-video estimates.

The checked-in `outputs/synthetic_benchmark.csv` and `outputs/sample_result.json` were produced by the repository code during packaging.

## Interpretation

Low error on the synthetic benchmark demonstrates that the implementation can recover a controlled periodic thoracic-motion signal.

It does **not** establish performance on:
- children,
- asthma exacerbations,
- clinical respiratory distress,
- spontaneous body motion,
- real patient video.

Those require appropriately governed data and independent validation.
