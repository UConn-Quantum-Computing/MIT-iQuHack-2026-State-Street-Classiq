# Monte Carlo Value at Risk (VaR) Analysis

This document explains the methodology and theory behind the Monte Carlo estimation of Value at Risk (VaR) and the analysis of its convergence properties.

## 1. Problem Definition

We model the annual return of an asset, $R$, as a random variable following a Gaussian (Normal) distribution:
$$ R \sim \mathcal{N}(\mu, \sigma^2) $$
Where in our example:
*   $\mu = 15\%$ (Annual Expected Return)
*   $\sigma = 20\%$ (Annual Volatility)

**Value at Risk (VaR)** at a confidence level $\alpha$ (e.g., 95%) is the threshold loss value such that the probability of the loss exceeding this value is $1 - \alpha$. In terms of returns, it is the $(1-\alpha)$-quantile of the return distribution.

$$ P(R < \text{VaR}_{\alpha}) = 1 - \alpha $$

## 2. Analytical Solution

For a Gaussian distribution, the quantile function (inverse CDF) is well-known. The analytical VaR is given by:

$$ \text{VaR}_{\alpha} = \mu + \sigma \cdot \Phi^{-1}(1 - \alpha) $$

Where $\Phi^{-1}$ is the inverse cumulative distribution function (PPF) of the standard normal distribution using `scipy.stats.norm.ppf`.

## 3. Monte Carlo Estimation

Monte Carlo methods estimate the VaR by simulating a large number of random scenarios.

1.  **Generate Samples**: Draw $N$ independent random samples $r_1, r_2, ..., r_N$ from $\mathcal{N}(\mu, \sigma^2)$.
2.  **Sort**: Order the samples from smallest to largest: $r_{(1)} \le r_{(2)} \le ... \le r_{(N)}$.
3.  **Estimate Quantile**: The empirical estimate of the $(1-\alpha)$-percentile corresponds to the sample at the index roughly equal to $N \times (1 - \alpha)$.

$$ \widehat{\text{VaR}}_{\alpha} \approx r_{(\lceil N(1-\alpha) \rceil)} $$

## 4. Convergence and Error Scaling

Monte Carlo estimates are statistical in nature, meaning they have a variance or "error" that depends on the number of samples $N$.

The standard error of a Monte Carlo estimator generally scales with the inverse square root of the number of samples:

$$ \text{Error} \propto \frac{1}{\sqrt{N}} $$

Or standard deviation of the error $\approx \frac{\sigma}{\sqrt{N}}$ (ignoring constants related to the specific quantile estimation).

If we define $\epsilon$ as the error, then:
$$ \epsilon = O\left(\frac{1}{\sqrt{N}}\right) $$
$$ \epsilon^2 = O\left(\frac{1}{N}\right) $$

This implies that to reduce the error by a factor of 10, one needs to increase the sample size by a factor of 100.

### Log-Log Analysis
By taking the logarithm of the error relationship:
$$ \log(\text{Error}) \approx -0.5 \log(N) + C $$

When plotting $\log(\text{Error})$ vs. $\log(N)$, we expect to see a linear trend with a slope of approximately **-0.5**.

## 5. Results

The Python script `monte_carlo_var.py` performs these steps:
1.  Computes the **true** analytical VaR.
2.  Runs Monte Carlo simulations for $N$ ranging from 100 to 1,000,000.
3.  Calculates the difference between the MC estimate and the true value.
4.  Plots the convergence and the error scaling.

The generated plot `monte_carlo_convergence.png` will show:
*   **Top Panel**: The estimated VaR converging to the red dashed analytical line as $N$ increases.
*   **Bottom Panel**: The error decreasing on a log-log scale. The "Best Fit Line" should have a slope close to -0.5, confirming the $O(1/\sqrt{N})$ convergence rate.
