---
layout: writeup

title: Say My Name
difficulty: Medium
points: 300
categories: [Misc]
tags: []

flag: CYS{Y0UR3_G0DD4MN_R1GHT_ABQKQF!}
---

Say My Name

Author: KuantumKnight

The challenge provides an ONNX model as the main artifact. The flag is not directly present in the model; instead, it is encoded as an input that produces a specific output through an auxiliary branch of the neural network.

Firstly, we inspect the structure of the ONNX model.

The graph contains a shared `Gemm -> Tanh` feature extractor and a normal four-class classification head. There is also an additional fifth logit calculated using a distance from a hidden target representation.

The relevant computation can be represented as:

```text
h(x) = tanh(Ax + b)

d(x) = ||h(x) - target||²

score_4(x) = 18 - 2500*d(x)
```

The useful tensors are stored in the model initializers:

```text
fc1.weight → 48×32 matrix A
fc1.bias   → bias vector b
buffer_0    → hidden target representation
```

The player input is normalized as:

```text
x = raw / 255
```

Since the matrix `A` has full column rank, we can invert the `Tanh` operation using `arctanh` and solve the resulting linear system using least squares.

Starting from:

```text
target = tanh(Ax + b)
```

we apply `arctanh`:

```text
arctanh(target) = Ax + b
```

Therefore:

```text
x = lstsq(A, arctanh(target) - b)
```

After recovering the normalized input, we convert it back into the original byte values:

```text
raw = rint(x * 255).astype(uint8)
```

The following Python script performs the complete inversion:

```python
#!/usr/bin/env python3

from pathlib import Path

import numpy as np
import onnx
from onnx import numpy_helper


ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "player" / "heisenberg.onnx"


def main() -> None:
    model = onnx.load(MODEL)
    tensors = {
        item.name: numpy_helper.to_array(item)
        for item in model.graph.initializer
    }

    matrix = tensors["fc1.weight"].astype(np.float64)
    bias = tensors["fc1.bias"].astype(np.float64)
    target = tensors["buffer_0"].astype(np.float64)

    normalized = np.linalg.lstsq(
        matrix,
        np.arctanh(target) - bias,
        rcond=None,
    )[0]

    raw = np.rint(normalized * 255).astype(np.uint8)
    print(bytes(raw).decode("ascii"))


if __name__ == "__main__":
    main()
```

Running the script recovers the flag:

```text
CYS{Y0UR3_G0DD4MN_R1GHT_ABQKQF!}
```

An alternative approach is to perform gradient ascent on the fifth logit, since maximizing the fifth score minimizes the distance between the generated representation and the hidden target.

The intended solve is therefore:

```text
ONNX model
    ↓
Inspect computation graph
    ↓
Find auxiliary distance branch
    ↓
Extract fc1.weight, fc1.bias and buffer_0
    ↓
Invert Tanh using arctanh
    ↓
Solve Ax + b = arctanh(target)
    ↓
Convert normalized values back to bytes
    ↓
Recover flag
```