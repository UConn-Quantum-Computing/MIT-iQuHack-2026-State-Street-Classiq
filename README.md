# Schrödinger's Husky: Value at Risk (VaR) Estimation with Classical Monte Carlo and Iterative Quantum Amplitude Estimation (IQAE)

This repository contains the analysis and implementation for **Value at Risk (VaR)** estimation using **Quantum Amplitude Estimation (IQAE)** and **classical Monte Carlo** methods. It explores the asymptotic scaling advantages of quantum algorithms over classical approaches and also dives into extensions like Interpolation as alternative to Bisection, CVaR, EVaR, and non-Gaussian distributions.

📄 **Read the Full Write-up**: [var_iqae_mc.pdf](var_iqae_mc.pdf) - Contains in-depth mathematical explanations and experimental results.

## 📂 Directory Structure

```plaintext
.
├── iqae-analysis/                # Quantum Amplitude Estimation (IQAE) notebooks
│   ├── iqae_1d_gauss_var_estimation.ipynb  # Main VaR estimation logic
│   ├── iqae_convergence_scaling.ipynb      # Scaling Analysis (O(1/ε))
│   ├── iqae_interpolation.ipynb            # Interpolation search optimization
│   └── iqae_sweep_qubits.ipynb             # Qubit resource analysis
│
├── monte-carlo-analysis/         # Classical baseline comparisons
│   └── monte_carlo_var.py                  # Classical MC simulation script
│
├── extension-var-analysis/       # Advanced risk metrics & methods
│   ├── cvar_analysis.ipynb                 # Conditional VaR (CVaR)
│   ├── evar.ipynb                          # Expectile VaR (EVaR)
│   └── qsp.ipynb                           # Quantum Singular Value Transf. (QSVT/QSP)
│
├── non-gaussian-analysis/        # Real-world distribution tests
│   ├── comparison.ipynb                    # Gaussian vs Non-Gaussian comparison
│   ├── kurtosis_analysis.ipynb             # Impact of Fat Tails (Student-t)
│   └── skewness_analysis.ipynb             # Impact of Skewness (Log-Normal)
│
├── plots/                        # Generated scaling and convergence plots
├── requirements.txt              # Python dependencies
├── var_iqae_mc.pdf               # In-depth explanation & results (PDF)
└── README.md                     # Project documentation
```

## 🚀 Setup Instructions

You can run this project using either **Conda** or a standard **Python Virtual Environment (venv)**.

### Prerequisites
*   Python 3.11+
*   [Classiq SDK Account](https://platform.classiq.io/) (for Quantum Execution)
    > **Note:** Please follow the Classiq Onboarding instructions to set up the SDK on your machine. The `requirements.txt` file in this repository only installs the additional dependencies needed for analysis and plotting.

---

### Option 1: Conda Setup (Recommended)

1.  **Create the environment:**
    ```bash
    conda create -n iquhack python=3.11 -y
    ```
2.  **Activate the environment:**
    ```bash
    conda activate iquhack
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Option 2: Python Venv Setup

1.  **Create a virtual environment:**
    ```bash
    # macOS/Linux
    python3 -m venv .venv
    
    # Windows
    python -m venv .venv
    ```
2.  **Activate the environment:**
    ```bash
    # macOS/Linux
    source .venv/bin/activate
    
    # Windows
    .venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Classiq Authentication

This project uses the **Classiq SDK** for quantum circuit synthesis and execution. You must authenticate to run the notebooks.

1.  **Sign Up / Login:**
    *   Go to the [Classiq Platform Onboarding Page](https://platform.classiq.io/).
    *   Create an account if you don't have one.

2.  **Authenticate Locally:**
    *   Run the following command in your terminal (with your environment activated):
        ```bash
        classiq authenticate
        ```
    *   This will open a browser window. Confirm the code to link your machine to your account.

3.  **Verify Setup:**
    *   Run a quick test in python:
        ```python
        import classiq
        print(classiq.__version__)
        ```

## 📘 Project Guide & Workflows

If you are exploring this repository, we recommend following this path to understand the full analysis.

### 1. Classical Baseline
Start here to understand the problem and the limits of classical computing.
*   **`monte-carlo-analysis/monte_carlo_var.py`**:
    *   **Goal**: Demonstrate the $O(1/\epsilon^2)$ convergence of Classical Monte Carlo.
    *   **What it does**: Simulates asset returns using `numpy` and plots error vs. sample size.
    *   **Takeaway**: High-precision VaR estimation is computationally expensive classically.

### 2. Quantum VaR (IQAE)
The core of the project. Visualizing the Quantum Advantage.
*   **`iqae-analysis/iqae_1d_gauss_var_estimation.ipynb`** (**Main Entry Point**):
    *   **Goal**: Estimate VaR using Quantum Amplitude Estimation.
    *   **What it does**: Implements the full pipeline: State Preparation -> IQAE -> Bisection Search.
    *   **Takeaway**: See the algorithm in action finding the 95% threshold.
*   **`iqae-analysis/iqae_convergence_scaling.ipynb`**:
    *   **Goal**: Prove the Quadratic Speedup ($O(1/\epsilon)$).
    *   **What it does**: Fixes a threshold and varies the target error $\epsilon$, measuring total Oracle Calls.
    *   **Takeaway**: Empirically proves that Quantum Scaling beats Classical Scaling.
*   **`iqae-analysis/iqae_interpolation.ipynb`**:
    *   **Goal**: Optimize the search step.
    *   **What it does**: Replaces the "blind" Bisection search with **Interpolation Search (Secant Method)**.
    *   **Takeaway**: Demonstrates how to use distribution properties (smoothness) to find VaR in fewer quantum iterations.
*   **`iqae-analysis/iqae_sweep_qubits.ipynb`**:
    *   **Goal**: Analyze resource scaling.
    *   **What it does**: Varies the grid size (num qubits) to check circuit depth/width requirements.

### 3. Non-Gaussian Distributions (Real World Risk)
Asset returns are rarely perfectly Gaussian. These notebooks study tail risk.
*   **`non-gaussian-analysis/comparison.ipynb`**:
    *   **Goal**: Compare Gaussian vs. Log-Normal vs. Student-t.
    *   **What it does**: Runs VaR estimation on 3 different distributions side-by-side.
    *   **Takeaway**: Gaussian models often underestimate tail risk.
*   **`non-gaussian-analysis/skewness_analysis.ipynb`**:
    *   **Goal**: Analyze asymmetric risk (Skew).
    *   **What it does**: Focuses on Log-Normal distributions with varying sigma.
*   **`non-gaussian-analysis/kurtosis_analysis.ipynb`**:
    *   **Goal**: Analyze Fat Tails (Kurtosis).
    *   **What it does**: Focuses on Student-t distributions. Shows why "Black Swan" events require accurate tail modeling.

### 4. Extensions (Advanced Metrics)
Going beyond simple VaR.
*   **`extension-var-analysis/cvar_analysis.ipynb`**:
    *   **Goal**: Estimate **Conditional VaR (CVaR)** / Expected Shortfall.
    *   **What it does**: Calculates the *expected probability* of losses exceeding the VaR threshold.
    *   **Why**: Regulators (Basel III) prefer CVaR over VaR.
*   **`extension-var-analysis/evar.ipynb`**:
    *   **Goal**: Estimate **Expectile VaR (EVaR)**.
    *   **What it does**: Computes the expectile by minimizing an asymmetric least squares loss function. Unlike standard VaR, Expectiles account for the magnitude of tail losses and satisfy coherency properties.
*   **`extension-var-analysis/qsp.ipynb`**:
    *   **Goal**: Explore **Quantum Singular Value Transformation (QSP/QSVT)**.
    *   **What it does**: Applies polynomial transformations to the singular values of the operator. Experimental look at next-gen quantum algorithms.
