"""Train the optional PyTorch temporal CNN on synthetic respiratory waveforms.

This is an experimentation scaffold, not a clinical model.
"""

import argparse
import math

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from respiratory_vision.model import TemporalCNNRegressor


def make_dataset(n: int, samples: int, fps: float, seed: int):
    rng = np.random.default_rng(seed)
    x = np.zeros((n, samples), dtype=np.float32)
    y = np.zeros(n, dtype=np.float32)
    t = np.arange(samples) / fps

    for i in range(n):
        bpm = rng.uniform(8.0, 36.0)
        hz = bpm / 60.0
        phase = rng.uniform(0, 2 * math.pi)
        fundamental = np.sin(2 * math.pi * hz * t + phase)
        harmonic = 0.2 * np.sin(4 * math.pi * hz * t + phase / 2)
        drift = 0.15 * np.sin(2 * math.pi * rng.uniform(0.01, 0.05) * t)
        noise = rng.normal(0, 0.18, size=samples)
        sig = fundamental + harmonic + drift + noise
        sig = (sig - sig.mean()) / (sig.std() + 1e-6)
        x[i] = sig.astype(np.float32)
        y[i] = bpm

    return torch.from_numpy(x[:, None, :]), torch.from_numpy(y)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--output", default="outputs/temporal_cnn.pt")
    args = parser.parse_args()

    torch.manual_seed(7)
    x_train, y_train = make_dataset(1400, 300, 15.0, seed=7)
    x_val, y_val = make_dataset(300, 300, 15.0, seed=8)

    loader = DataLoader(TensorDataset(x_train, y_train), batch_size=64, shuffle=True)
    model = TemporalCNNRegressor()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.L1Loss()

    for epoch in range(args.epochs):
        model.train()
        for xb, yb in loader:
            optimizer.zero_grad()
            pred = model(xb)
            loss = loss_fn(pred, yb)
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            val_mae = torch.mean(torch.abs(model(x_val) - y_val)).item()
        print(f"epoch={epoch+1:02d} validation_MAE={val_mae:.3f} BPM")

    torch.save(model.state_dict(), args.output)
    print(f"Saved model to {args.output}")


if __name__ == "__main__":
    main()
