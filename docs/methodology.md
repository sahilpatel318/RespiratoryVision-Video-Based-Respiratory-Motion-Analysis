# Methodology

## Research question

Can subtle periodic upper-torso motion in ordinary RGB video provide a usable estimate of respiratory rate under controlled conditions?

## Baseline design

RespiratoryVision uses an interpretable baseline:

1. Decode RGB video using OpenCV.
2. Select an upper-torso region of interest.
3. Convert ROI frames to grayscale and apply light Gaussian smoothing.
4. Compute dense Farneback optical flow between successive frames.
5. Robustly aggregate the vertical flow component.
6. Integrate frame-to-frame flow into a displacement-like motion trace.
7. Detrend the signal.
8. Apply a Butterworth band-pass filter restricted to plausible respiratory frequencies.
9. Estimate dominant frequency using Welch power spectral density.
10. Convert dominant Hz to breaths/minute.

## Why optical flow?

Breathing produces small periodic displacements of the thoracic/abdominal surface. Optical flow provides a direct way to estimate apparent frame-to-frame motion without requiring contact sensors.

## Why start with a non-neural baseline?

An interpretable baseline provides:
- inspectable intermediate signals,
- easier debugging,
- a reference for future learned models,
- clearer error analysis,
- lower risk of reporting opaque model behavior.

## Synthetic benchmark

The repository contains a controlled synthetic video generator. It creates a textured torso-like region with known sinusoidal vertical motion. This is useful for verifying that the pipeline can recover a known periodic signal.

The synthetic benchmark is **engineering validation only**. It does not represent clinical validation.

## Optional learned model

`TemporalCNNRegressor` is a compact PyTorch 1D CNN for estimating respiratory rate from preprocessed temporal signals. The included training script uses synthetic signals only.

A responsible next step would compare:
- deterministic spectral baseline,
- temporal CNN,
- motion-artifact robust variants,

on a legitimate research dataset with synchronized respiratory ground truth.

## Evaluation metrics

For known ground truth:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Mean bias
- Per-sample absolute error

For real research studies, additional analyses should include agreement plots, confidence intervals, subgroup analysis, and motion-artifact stratification.
