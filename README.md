# RespiratoryVision

**RespiratoryVision** is a research-oriented computer-vision prototype for estimating respiratory rate from ordinary RGB video by tracking subtle thoracic motion.

It was built to demonstrate an end-to-end research workflow:

**video -> ROI selection -> OpenCV optical flow -> respiratory signal -> filtering -> rate estimation -> evaluation -> visualization**

The repository is intentionally transparent: the included benchmark uses **synthetic, non-clinical video** with known breathing rates. It is **not a medical device** and must not be used for diagnosis or clinical decision-making.

## Why this project exists

Contactless respiratory monitoring is an active computer-vision and digital-health research area. Camera-based methods can estimate breathing activity from small, periodic movements of the chest/upper torso. RespiratoryVision implements a defensible baseline pipeline and provides an optional PyTorch temporal model for experimentation.

## Key capabilities

- Reads RGB video with **OpenCV**
- Supports relative or interactive thoracic **ROI selection**
- Extracts frame-to-frame motion using **dense optical flow**
- Converts vertical thoracic motion into a temporal respiratory waveform
- Applies detrending and physiologically plausible band-pass filtering
- Estimates respiratory rate using spectral analysis
- Reports confidence and signal-quality diagnostics
- Generates reproducible synthetic respiratory videos with known ground truth
- Includes evaluation scripts, unit tests, documentation, privacy/ethics notes
- Includes an optional **PyTorch 1D CNN** regression experiment on synthetic respiratory signals
- Produces CSV/JSON outputs and publication-style plots

## Pipeline

1. **Video ingestion**
   - Decode frames and preserve frame rate.
2. **ROI selection**
   - Default relative upper-torso ROI or interactive selection.
3. **Preprocessing**
   - Grayscale conversion and Gaussian smoothing.
4. **Motion extraction**
   - Dense Farneback optical flow.
   - Robust median vertical flow within the ROI.
5. **Signal construction**
   - Integrate flow to obtain a displacement-like respiratory waveform.
6. **Signal processing**
   - Linear detrending.
   - Butterworth band-pass filtering (default 6-48 BPM).
7. **Rate estimation**
   - Welch power spectral density.
   - Dominant respiratory-frequency selection.
8. **Quality controls**
   - Spectral peak ratio.
   - Minimum duration and finite-signal checks.
9. **Evaluation**
   - Compare estimated BPM against known synthetic ground truth.

## Research framing

The baseline deliberately starts with an interpretable signal-processing method rather than hiding all behavior inside a neural network. This makes it easier to inspect failure modes and establish a baseline before adding learned models.

The optional PyTorch model in `src/respiratory_vision/model.py` is a small temporal CNN intended only as an experimental extension. It is trained on synthetic waveforms, not clinical data.

## Repository structure

```text
RespiratoryVision/
├── data/sample/
├── docs/
│   ├── ethics_privacy.md
│   ├── literature_review.md
│   ├── methodology.md
│   └── results.md
├── outputs/
├── scripts/
│   ├── evaluate_synthetic.py
│   ├── generate_synthetic_video.py
│   ├── run_pipeline.py
│   └── train_signal_model.py
├── src/respiratory_vision/
│   ├── config.py
│   ├── estimator.py
│   ├── metrics.py
│   ├── model.py
│   ├── motion.py
│   ├── roi.py
│   ├── signal_processing.py
│   ├── synthetic.py
│   └── video_io.py
└── tests/
```


## Limitations

- Default ROI is geometric, not anatomy-aware.
- Motion artifacts, camera movement, loose clothing, occlusion, and lighting can reduce signal quality.
- Synthetic benchmark performance does not imply real-world or clinical performance.
- No pediatric or patient data are included.
- No medical claims are made.

## License

MIT. See `LICENSE`.
