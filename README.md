# Piper Arm Controller

A simple and interactive Python interface for controlling the **Piper robotic arm** via the `piper_control` API.

This controller allows you to:
- Set joint positions absolutely or relatively
- Open/close the gripper with precise control
- Interact with the robot from the terminal using simple text commands

---

## 🚀 Installation

### 1. Install CAN utilities (required for communicating with the Piper arm)
```bash
sudo apt install can-utils
```

### 2. Install the `piper_control` Python package
```bash
pip install piper_control
```

---

## 🧠 Overview

This controller script provides the following functionality:

- Move the arm to a **start position**
- Move joints by providing **absolute** or **relative** values (radians or degrees)
- Open or close the **gripper**
- Run an **interactive terminal interface** for manual control

---

## 🧩 Features

- Absolute and relative joint control  
- Degrees and radians support  
- Interactive gripper control (open, close, or partial)  
- Current state feedback after every command  

---

## 🛠 Usage

### 1. Clone or copy the script
Save the code from `PiperArmController` into a file, e.g. `piper_arm_controller.py`.

### 2. Run the controller

```bash
python3 piper_arm_controller.py
```

---

## 🎮 Interactive Terminal Commands

When running, you’ll be able to enter:

### Joint control:
- **Absolute radians:**  
  ```
  1.0 -0.5 0.3 0.2 -1.2 0.8
  ```

- **Absolute degrees:**  
  ```
  45 -30 15 10 -70 45d
  ```

- **Relative radians:**  
  ```
  +0.1 0 -0.2 0 0.3 0
  ```

- **Relative degrees:**  
  ```
  +5 0 -10 0 15 0d
  ```

> Use the prefix `+` to indicate a relative movement and suffix `d` to enter values in degrees.

### Gripper control:
Type `g` and press enter to enter gripper mode:
- `o`: Open gripper fully  
- `c`: Close gripper fully  
- `0.0`–`1.0`: Set gripper position (0 = closed, 1 = open)  
- `b`: Go back to joint control  

### Quit:
Type `q` or `quit` or `exit` at any time to leave the controller.

---

## 📍 Default Start Position

This is the default joint configuration in radians:
```python
[-1.593, 0.634, -0.286, 0, 0.385, -1.85]
```

Use `arm.set_start_position()` in code to return to this pose.

---

## 🧪 Programmatic Example

Here’s how to use the controller from your own script:

```python
from piper_arm_controller import PiperArmController
import numpy as np

arm = PiperArmController()
arm.set_start_position()

# Move arm relative to start
arm.set_relative_angles(np.array([0.1, 0, -0.2, 0, 0.1, 0]))

# Open gripper halfway
arm.set_gripper(0.5)
```

---

## 📦 Dependencies

- `piper_control` (Python package)  
- `can-utils` (Linux CAN communication utilities)  
- Python 3.7+

---

## 👨‍🔧 Troubleshooting

- Make sure the CAN device is available (e.g., `can0`)  
- Ensure Piper is connected and powered on  
- Run with `sudo` if permissions are restricted on `can0`
