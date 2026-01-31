import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def calculate_analytical_var(mu, sigma, confidence_level):
    """
    Calculates the analytical Value at Risk (VaR) for a Gaussian distribution.
    VaR is defined such that P(X < VaR) = 1 - confidence_level (for losses defined as positive?)
    Convention here: Returns are X. We want the cutoff R* such that P(X < R*) = 1 - alpha.
    So VaR is usually expressed as a positive loss, but here we'll return the return threshold.
    """
    # For a return distribution, VaR at alpha (e.g., 95%) usually corresponds to the (1-alpha) quantile.
    # Example: 95% confidence => 5th percentile of returns.
    return stats.norm.ppf(1 - confidence_level, loc=mu, scale=sigma)

def monte_carlo_var_simulation(mu, sigma, confidence_level, sample_sizes):
    """
    Runs Monte Carlo simulations for various sample sizes to estimate VaR.
    """
    analytical_var = calculate_analytical_var(mu, sigma, confidence_level)
    
    estimated_vars = []
    errors = []
    
    # We will repeat the experiment multiple times for each N to get an average error
    # or just do one run per N to show the noisy convergence. One run is standard for this demo.
    
    print(f"Analytical VaR ({(confidence_level)*100}%): {analytical_var:.6f}")
    
    for n in sample_sizes:
        # 1. Generate N random returns from N(mu, sigma)
        returns = np.random.normal(mu, sigma, n)
        
        # 2. Estimate VaR: The (1-alpha) percentile of the empirical distribution
        # percent param in percentile is 0-100
        percentile = (1 - confidence_level) * 100
        estimated_var = np.percentile(returns, percentile)
        
        estimated_vars.append(estimated_var)
        
        # 3. Calculate absolute error
        error = abs(estimated_var - analytical_var)
        errors.append(error)

    return analytical_var, estimated_vars, errors

def main():
    # Parameters
    mu = 0.15        # Annual expected return (15%)
    sigma = 0.20     # Annual volatility (20%)
    confidence_level = 0.95 # 95% confidence
    
    # Sample sizes to test: logarithmic spacing from 100 to 1,000,000
    sample_sizes = np.logspace(2, 6, num=50, dtype=int)
    
    # Run Simulation
    analytical_var, estimated_vars, errors = monte_carlo_var_simulation(mu, sigma, confidence_level, sample_sizes)
    
    # Plotting
    plt.figure(figsize=(12, 10))
    
    # Subplot 1: Convergence of VaR estimate
    plt.subplot(2, 1, 1)
    plt.plot(sample_sizes, estimated_vars, label='MC Estimated VaR', color='blue', alpha=0.7)
    plt.axhline(y=analytical_var, color='red', linestyle='--', label=f'Analytical VaR ({analytical_var:.5f})')
    plt.xscale('log')
    plt.xlabel('Number of Samples (N)')
    plt.ylabel('VaR Limit (Return)')
    plt.title(f'Convergence of Monte Carlo VaR Estimate (Confidence: {confidence_level*100}%)')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    # Subplot 2: Error Scaling (Log-Log Plot)
    plt.subplot(2, 1, 2)
    plt.loglog(sample_sizes, errors, 'o', label='Absolute Error', markersize=4, color='green')
    
    # Fit a reference line for O(1/sqrt(N)) => log(Err) ~ -0.5 * log(N) + C
    # We want to show slope is roughly -0.5
    # Let's fit a line to the log-log data
    log_N = np.log(sample_sizes)
    log_Err = np.log(errors)
    slope, intercept = np.polyfit(log_N, log_Err, 1)
    
    plt.plot(sample_sizes, np.exp(intercept) * sample_sizes**slope, 'r--', 
             label=f'Best Fit Line (Slope = {slope:.2f})')
    
    # Theoretical O(1/sqrt(N)) reference
    # Just anchor it to the middle point for visualization
    mid_idx = len(sample_sizes) // 2
    ref_constant = errors[mid_idx] * np.sqrt(sample_sizes[mid_idx])
    plt.plot(sample_sizes, ref_constant / np.sqrt(sample_sizes), 'k:', label='Theoretical $O(1/\sqrt{N})$')

    plt.xlabel('Number of Samples (N)')
    plt.ylabel('Absolute Error |Estimated - Analytical|')
    plt.title('Monte Carlo Error Scaling')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.tight_layout()
    plt.savefig('monte_carlo_convergence.png')
    print("Plots saved to monte_carlo_convergence.png")

if __name__ == "__main__":
    main()
