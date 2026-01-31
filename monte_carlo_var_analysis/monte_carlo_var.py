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

def monte_carlo_var_simulation(mu, sigma, confidence_level, sample_sizes, num_trials=50):
    """
    Runs Monte Carlo simulations for various sample sizes to estimate VaR.
    Averages error over `num_trials` to smooth the curve.
    """
    analytical_var = calculate_analytical_var(mu, sigma, confidence_level)
    
    estimated_vars_means = [] # We'll plot the mean estimated VaR just for viz
    avg_errors = []
    
    print(f"Analytical VaR ({(confidence_level)*100}%): {analytical_var:.6f}")
    
    for n in sample_sizes:
        current_n_errors = []
        current_n_vars = []
        
        for _ in range(num_trials):
            # 1. Generate N random returns from N(mu, sigma)
            returns = np.random.normal(mu, sigma, n)
            
            # 2. Estimate VaR
            percentile = (1 - confidence_level) * 100
            estimated_var = np.percentile(returns, percentile)
            
            # 3. Calculate absolute error
            error = abs(estimated_var - analytical_var)
            
            current_n_vars.append(estimated_var)
            current_n_errors.append(error)
        
        # Store averages
        estimated_vars_means.append(np.mean(current_n_vars))
        avg_errors.append(np.mean(current_n_errors))

    return analytical_var, estimated_vars_means, avg_errors

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
    plt.figure(figsize=(12, 15))
    
    # Subplot 1: Convergence of VaR estimate
    plt.subplot(3, 1, 1)
    plt.plot(sample_sizes, estimated_vars, label='MC Estimated VaR', color='blue', alpha=0.7)
    plt.axhline(y=analytical_var, color='red', linestyle='--', label=f'Analytical VaR ({analytical_var:.5f})')
    plt.xscale('log')
    plt.xlabel('Number of Samples (N)')
    plt.ylabel('VaR Limit (Return)')
    plt.title(f'Convergence of Monte Carlo VaR Estimate (Confidence: {confidence_level*100}%)')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    # Subplot 2: Error Scaling (Log-Log Plot)
    plt.subplot(3, 1, 2)
    plt.loglog(sample_sizes, errors, 'o', label='Average Absolute Error', markersize=4, color='green')
    
    # Fit a reference line for O(1/sqrt(N)) => log(Err) ~ -0.5 * log(N) + C
    log_N = np.log(sample_sizes)
    log_Err = np.log(errors)
    slope, intercept = np.polyfit(log_N, log_Err, 1)
    
    plt.plot(sample_sizes, np.exp(intercept) * sample_sizes**slope, 'r--', 
             label=f'Best Fit Line (Slope = {slope:.2f})')
    
    # Theoretical O(1/sqrt(N)) reference
    mid_idx = len(sample_sizes) // 2
    ref_constant = errors[mid_idx] * np.sqrt(sample_sizes[mid_idx])
    plt.plot(sample_sizes, ref_constant / np.sqrt(sample_sizes), 'k:', label='Theoretical $O(1/\sqrt{N})$')

    plt.xlabel('Number of Samples (N)')
    plt.ylabel('Average Absolute Error')
    plt.title(f'Monte Carlo Error Scaling (Averaged over separate trials)')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)

    # Subplot 3: N vs 1/Error^2 (Demonstrating O(1/epsilon^2))
    plt.subplot(3, 1, 3)
    inv_squared_errors = 1.0 / (np.array(errors)**2)
    plt.plot(inv_squared_errors, sample_sizes, 'o', color='purple', label='Samples vs $1/\epsilon^2$', markersize=4)
    
    # Best fit line for this plot (Linear)
    # We expect N ~ k * (1/Error^2)
    # Fit y = m*x + c
    m, c = np.polyfit(inv_squared_errors, sample_sizes, 1)
    plt.plot(inv_squared_errors, m*inv_squared_errors + c, 'r--', label=f'Linear Fit (y={m:.2f}x + {c:.0f})')
    
    plt.xlabel('Inverse Squared Error ($1/\epsilon^2$)')
    plt.ylabel('Number of Samples (N)')
    plt.title('Sample Cost vs Precision ($N \propto 1/\epsilon^2$)')
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    plt.tight_layout()
    plt.savefig('monte_carlo_convergence.png')
    print("Plots saved to monte_carlo_convergence.png")

if __name__ == "__main__":
    main()
