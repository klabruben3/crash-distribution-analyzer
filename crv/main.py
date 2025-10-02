import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

data = []  # collected multipliers

def update_plot(data, x_value, tol):
    plt.clf()
    data = np.array(data)

    # --- Fit candidate distributions ---
    fitted_dists = {
        "Exponential": (stats.expon, stats.expon.fit(data)),
        "Lognormal":  (stats.lognorm, stats.lognorm.fit(data, floc=0)),
        "Gamma":      (stats.gamma, stats.gamma.fit(data, floc=0)),
        "Weibull":    (stats.weibull_min, stats.weibull_min.fit(data, floc=0)),
        "Pareto":     (stats.pareto, stats.pareto.fit(data, floc=0)),
    }

    # --- X-axis values ---
    x = np.linspace(min(data), max(data), 400)

    # --- Plot histogram ---
    plt.hist(data, bins=30, density=True, alpha=0.6, color="skyblue", label="Empirical Data")

    # --- Evaluate models ---
    n = len(data)
    model_scores = []
    for name, (dist, params) in fitted_dists.items():
        pdf = dist.pdf(x, *params)
        plt.plot(x, pdf, label=name)

        loglik = np.sum(dist.logpdf(data, *params))
        k = len(params)
        aic = 2*k - 2*loglik
        bic = np.log(n)*k - 2*loglik
        model_scores.append((name, dist, params, loglik, aic, bic))

    plt.legend()
    plt.title("Fitted PDFs vs Data (Crash multipliers)")
    plt.xlabel("Multiplier")
    plt.ylabel("Density")

    # --- Sort models by AIC ---
    model_scores.sort(key=lambda x: x[4])  # x[4] = AIC

    # --- Annotate top 3 models on plot (parameters only) ---
    for i in range(min(3, len(model_scores))):
        name, dist, params, *_ = model_scores[i]
        param_str = ", ".join(f"{p:.3f}" for p in params)
        plt.text(0.95, 0.95 - i*0.08, f"{i+1}. {name}: {param_str}",
                 transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
                 horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.5))

    plt.pause(0.1)

    # --- Print full comparison table ---
    print(f"\nTarget x = {x_value}, tolerance = ±{tol}\n")
    print("Model comparison (better fit = higher loglik, lower AIC/BIC):")
    print(f"{'Name':<12}{'LogLik':>12}{'AIC':>12}{'BIC':>12}")
    for name, dist, params, loglik, aic, bic in model_scores:
        print(f"{name:<12}{loglik:12.2f}{aic:12.2f}{bic:12.2f}")
    print("-" * 60)

    # --- Show interval probabilities for top 3 models ---
    print("Top 3 fits interval probabilities:")
    for i in range(min(3, len(model_scores))):
        name, dist, params, *_ = model_scores[i]
        prob_interval = dist.cdf(x_value + tol, *params) - dist.cdf(x_value - tol, *params)
        print(f"{i+1}. {name}: P({x_value - tol:.2f} ≤ X ≤ {x_value + tol:.2f}) ≈ {prob_interval*100:.2f}%")
    print("-" * 60)


# --- Ask user for initial target multiplier and tolerance ---
while True:
    try:
        x_value = float(input("Enter target multiplier x: "))
        tol = float(input("Enter tolerance (± value): "))
        break
    except ValueError:
        print("Invalid input. Please enter numbers.")

plt.ion()  # interactive mode

print("\nEnter at least 30 multipliers before distributions will be fitted.")
print("Type 'u' to update x/tolerance, 'q' to quit.\n")

# --- Main input loop ---
while True:
    user_input = input("Enter multiplier, 'u' to update x/tolerance, or 'q' to quit: ")

    if user_input.lower() == "q":
        break
    elif user_input.lower() == "u":
        try:
            x_value = float(input("Enter new target x: "))
            tol = float(input("Enter new tolerance (± value): "))
            if len(data) >= 30:
                update_plot(data, x_value, tol)
        except ValueError:
            print("Invalid input. Keeping old values.")
    else:
        try:
            new_val = float(user_input)
            data.append(new_val)
            if len(data) >= 30:
                update_plot(data, x_value, tol)
            else:
                print(f"Collected {len(data)} samples (need {30 - len(data)} more).")
        except ValueError:
            print("Invalid input, enter a number, 'u' or 'q'.")
