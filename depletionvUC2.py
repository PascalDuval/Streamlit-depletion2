import streamlit as st
import numpy as np
from scipy.stats import beta, poisson
import matplotlib.pyplot as plt

# Section 1: Paramètres Généraux
st.title("Tokenomics Simulation Dashboard")
st.sidebar.header("General Parameters")
periods = st.sidebar.slider("Number of Simulation Periods", min_value=5, max_value=50, value=10, step=1)
target_ratio = st.sidebar.slider("Critical Ratio (Drains/Sources)", min_value=1.0, max_value=3.0, value=1.5, step=0.1)

# Section 2: Configuration des Drains
st.sidebar.header("Drains Configuration")
opex = st.sidebar.slider("OPEX (tokens per period)", min_value=50, max_value=500, value=150, step=10)
burn_rate = st.sidebar.slider("Burn Rate (%)", min_value=0.01, max_value=0.2, value=0.05, step=0.01)
alea_lambda = st.sidebar.slider("Adoption Variability (Poisson λ)", min_value=5, max_value=50, value=15, step=5)
rewards_rate = st.sidebar.slider("Rewards Rate (%)", min_value=0.01, max_value=0.1, value=0.03, step=0.01)

# Section 3: Configuration des Sources
st.sidebar.header("Sources Configuration")
vesting_alpha = st.sidebar.slider("Vesting Alpha (Beta distribution)", min_value=1, max_value=10, value=4, step=1)
vesting_beta = st.sidebar.slider("Vesting Beta (Beta distribution)", min_value=1, max_value=10, value=3, step=1)
minting = st.sidebar.slider("Minting (tokens per period)", min_value=10, max_value=200, value=60, step=10)

# Simulation
cumulative_drains = 0
cumulative_sources = 0
time_series_drains = []
time_series_sources = []
alert_triggered = False

for t in range(periods):
    # Drains
    alea = poisson.rvs(alea_lambda)
    drain = opex + burn_rate * 100 + alea + rewards_rate * 100
    
    # Sources
    vesting = beta.rvs(vesting_alpha, vesting_beta) * 100
    source = vesting + minting
    
    # Update cumulative values
    cumulative_drains += drain
    cumulative_sources += source
    
    time_series_drains.append(cumulative_drains)
    time_series_sources.append(cumulative_sources)
    
    # Check for alert
    if cumulative_drains / cumulative_sources > target_ratio and not alert_triggered:
        alert_triggered = True
        alert_period = t + 1

# Results
st.subheader("Simulation Results")
if alert_triggered:
    st.write(f"🚨 **Alert Triggered** at period {alert_period} (Ratio > {target_ratio})")
else:
    st.write("✅ No Alert Triggered")

st.write(f"**Final Ratio (Drains/Sources):** {cumulative_drains / cumulative_sources:.2f}")

# Graphs
st.subheader("Cumulative Drains vs Sources")
plt.figure(figsize=(10, 6))
plt.plot(range(1, periods + 1), time_series_drains, label="Cumulative Drains")
plt.plot(range(1, periods + 1), time_series_sources, label="Cumulative Sources", linestyle="--")
if alert_triggered:
    plt.axvline(alert_period, color="red", linestyle=":", label=f"Alert Period ({alert_period})")
plt.title("Cumulative Drains vs Sources")
plt.xlabel("Periods")
plt.ylabel("Tokens")
plt.legend()
st.pyplot(plt)
