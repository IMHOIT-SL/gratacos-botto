import numpy as np
import matplotlib.pyplot as plt

# years 1990–2060
t = np.arange(1990, 2061)

# logistic‑style resistance curve (conceptual)
# k controls steepness; x0 is inflection point
k = 0.15
x0 = 2010.0
resistance_score = 100 / (1 + np.exp(-k * (t - x0)))

# manually cap early years closer to observed data (1990–2021)
resistance_score = np.clip(resistance_score, 10, 100)  # start higher than 0
resistance_score[t<=1995] = np.linspace(12, 18, sum(t<=1995))
resistance_score[(t>1995)&(t<=2021)] = np.linspace(18, 65, sum((t>1995)&(t<=2021)))
resistance_score[t>2021] = np.linspace(65, 98, sum(t>2021))

# Plot
plt.figure(figsize=(10, 5))
plt.plot(t, resistance_score, "b-", linewidth=3, label="AMR pressure / superbug inevitability")
plt.axvline(2043, color="red", linestyle="--", label="Critical point (≈2040–2045)")
plt.axhline(95, color="red", linestyle=":", label="Threshold of near‑total ineffectiveness")
plt.xlabel("Year")
plt.ylabel("Resistance pressure index (0–100, normalized)")
plt.title("Rise of Antibiotic Resistance and Forecasted Critical Point")
plt.grid(alpha=0.3)
plt.legend()
plt.show()