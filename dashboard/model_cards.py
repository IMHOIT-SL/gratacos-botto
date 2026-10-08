"""
Model cards: the equation behind every chart, and what each term means.

Each chart gets a collapsible card under it:
  * model / statistical charts: the equation (MathJax), the same equation with
    the actual numbers ("live" where the page has controls), a term picker that
    explains one term at a time (option B), and the full terms table (option A);
  * data-only charts: a data card (what the numbers are, years, method,
    sources with links) instead of an equation.

All prose is English and goes through the i18n catalog like the rest of the
app. Equations use symbols only, so they read the same in both languages;
equations with numbers are rendered twice (decimal point / decimal comma) and
CSS shows the one matching <html lang>, set by assets/i18n.js.
"""

from dash import html, dcc, callback, Input, Output, State, MATCH

from i18n import translated

PAPER = "https://doi.org/10.5281/zenodo.21898960"
MURRAY = "https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext"
TAI = "https://doi.org/10.1016/j.ijantimicag.2025.107636"
ONEILL = "https://amr-review.org/sites/default/files/160518_Final%20paper_with%20cover.pdf"
GRAM = "https://www.cidrap.umn.edu/antimicrobial-stewardship/study-forecasts-more-39-million-deaths-antimicrobial-resistance-2050"
GLASS = "https://www.who.int/publications/i/item/9789240062702"
EARS = "https://www.ecdc.europa.eu/en/antimicrobial-resistance/surveillance-and-disease-data/data-ecdc"
CDC = "https://www.cdc.gov/antimicrobial-resistance/data-research/threats/index.html"
NARMS = "https://www.cdc.gov/narms/index.html"
MAGIORAKOS = "https://www.clinicalmicrobiologyandinfection.com/article/S1198-743X(14)61632-3/fulltext"
PUBMED = "https://pubmed.ncbi.nlm.nih.gov/?term=antibiotic+resistance"
UNIVDATOS = "https://univdatos.com/reports/antibiotic-resistance-market"
KIM2023 = "https://pubmed.ncbi.nlm.nih.gov/37250043/"
BOX_JENKINS = "https://otexts.com/fpp3/seasonal-arima.html"

# Shared terms of the paper's super-exponential model
_T_Y = dict(key="y", sym="y(τ)", name="Resistance pressure index",
            what="Composite index of resistance pressure in year τ: 0 = no resistance, 100 = first-line antibiotics fully ineffective.",
            value="0-100", source="Composite index defined in the paper", control="It is what the curve draws.")
_T_TAU = dict(key="tau", sym="τ", name="Time",
              what="Years elapsed since 1990: τ = year − 1990 (for example, 2025 is τ = 35 and 2047 is τ = 57).",
              value="1990 → 0", source="Origin of the model", control="-")
_T_K = dict(key="K", sym="K", name="Ceiling",
            what="Upper limit of the index. Resistance cannot exceed 100 %, so the curve flattens as it approaches K.",
            value="100", source="By construction of the index", control="-")
_T_A = dict(key="A", sym="A", name="Starting point",
            what="Sets the 1990 value: with A = 88/12 the curve starts exactly at 12, the observed anchor for 1990.",
            value="7.333", source="Observed anchor 1990 = 12", control="-")
_T_R = dict(key="r", sym="r", name="Base rate",
            what="How fast resistance grows at the start, per year. In 1990, with the index at 12, it means growth close to 6 % per year (r × (1 − 12/100) ≈ 0.062).",
            value="0.0705", source="Calibrated by hand to the paper's milestones (70 in 2025, about 90 in 2040, about 96 in 2047)",
            control="Scenario Lab: Stewardship multiplies it by (1 − s).")
_T_B = dict(key="b", sym="b", name="Acceleration",
            what="How much the growth rate itself increases every year. It is the paper's central thesis ('the rate of increasing resistance is itself growing'), written as the b·τ² term.",
            value="0.000305", source="Calibrated with r to the same milestones",
            control="Scenario Lab: New antibiotics multiplies it by (1 − p).")
_T_REFF = dict(key="reff", sym="r_ef(τ)", name="Effective rate",
               what="The real growth rate of the exponent in year τ (its derivative): r + 2bτ. Because b > 0 it rises every year, which is why the curve runs ahead of a common logistic.",
               value="0.0705 → 0.1053 (1990 → 2047)", source="Derived from r and b", control="Scenario Lab: both sliders lower it.")
_T_95 = dict(key="thr", sym="95", name="Critical inefficacy threshold",
             what="Index value at which first-line antibiotics become largely ineffective for hospital-acquired Gram-negative infections.",
             value="95", source="Paper (window 2040-2047)", control="The year it is crossed is solved exactly (quadratic formula).")


CARDS = {
    # ------------------------------------------------------------------ Overview
    "trajectory": dict(
        kind="model", title="Super-exponential generalized logistic",
        intro="The curve is a logistic whose exponent has a time-squared term, so the growth rate itself grows. Every coefficient is fixed by hand from published milestones: nothing is fitted and nothing is random.",
        equations=[r"$$y(\tau)=\dfrac{K}{1+A\,e^{-(r\tau+b\tau^{2})}}\qquad r_{\mathrm{ef}}(\tau)=r+2b\tau\qquad y(\tau\pm3)$$"],
        numeric=(r"$$y(\tau)=\dfrac{100}{1+7.333\,e^{-(0.0705\,\tau+0.000305\,\tau^{2})}}\qquad y_{\mathrm{ref}}(\tau)=\dfrac{100}{1+7.333\,e^{-0.0811\,\tau}}$$",),
        terms=[_T_Y, _T_TAU, _T_K, _T_A, _T_R, _T_B, _T_REFF,
               dict(key="band", sym="±3", name="Uncertainty band",
                    what="The same curve shifted 3 years earlier and later, matching the paper's 'fourteen years (±3)'. It is not a statistical confidence interval.",
                    value="± 3 years", source="Paper, Abstract", control="-"),
               dict(key="ref", sym="r'", name="Reference logistic",
                    what="A common logistic (constant rate, b = 0) through the same 1990 and 2025 points, drawn for comparison. It reaches the threshold in 2051, four years after the super-exponential model.",
                    value="0.0811", source="Solved from y(1990) = 12 and y(2025) = 70", control="-"),
               _T_95],
        sources=[("Prieto Gratacós & Botto, Br J Med Health Res 2026", PAPER)],
    ),
    "mortality": dict(
        kind="data", title="Published mortality projections",
        what="Deaths per year due to antimicrobial resistance, in thousands. Two quantities: attributable deaths (caused directly by the resistant infection) and associated deaths (people who died with a resistant infection). The dashed line is a third, more conservative methodology.",
        years="2019 (observed) and projections to 2050",
        method="Values are taken from the published studies and plotted as given; between their milestones the bars use the published projections. The app does not model mortality.",
        sources=[("Murray et al., Lancet 2022 (2019 baseline)", MURRAY), ("GRAM Project (CIDRAP)", GRAM),
                 ("O'Neill Review on AMR (2016)", ONEILL), ("Tai et al., IJAA 2025", TAI)],
    ),
    "validation": dict(
        kind="model", title="Historical back-validation (out-of-sample)",
        intro="To test the model honestly, its two free coefficients are recomputed using only the 2010 and 2015 anchors, then the resulting curve predicts the 2019, 2021 and 2025 observations it never saw.",
        equations=[r"$$r\,\tau_i+b\,\tau_i^{2}=\ln\!\left(\dfrac{A}{K/v_i-1}\right),\qquad i\in\{2010,\,2015\}$$",
                   r"$$\mathrm{MAE}=\dfrac{1}{n}\sum_{j}\left|y_j-\hat y_j\right|$$"],
        numeric=(r"$$r=0.0567,\qquad b=0.0006,\qquad \mathrm{MAE}=3.8$$",),
        terms=[dict(key="vi", sym="vᵢ", name="Calibration anchors",
                    what="The observed index in 2010 (35) and 2015 (45). Two equations with two unknowns give r and b exactly (a 2 × 2 linear system), so this is a closed-form derivation, not a fit.",
                    value="35, 45", source="Lancet GBD anchors", control="-"),
               dict(key="r2", sym="r, b", name="Recomputed coefficients",
                    what="The base rate and acceleration obtained from the pre-2016 anchors only. K and A are unchanged.",
                    value="0.0567 / 0.0006", source="Solved from the two anchors", control="-"),
               dict(key="yj", sym="yⱼ, ŷⱼ", name="Observed and predicted",
                    what="The held-out observations (2019, 2021, 2025) and what the pre-2016 curve predicts for them.",
                    value="58, 63, 70", source="Murray 2022, Lancet GBD, CIDRAP/GRAM", control="-"),
               dict(key="mae", sym="MAE", name="Mean absolute error",
                    what="The average distance between observed and predicted values, in index points. Under 4 points, and the model errs on the conservative side.",
                    value="3.8", source="Computed in the app", control="-")],
        sources=[("Prieto Gratacós & Botto, Br J Med Health Res 2026 (Limitations)", PAPER)],
    ),
    "carbapenem": dict(
        kind="data", title="Carbapenem-resistance deaths to 2035",
        what="Deaths per year (thousands) from three carbapenem-resistant groups: Enterobacterales (CRE), A. baumannii (CRAB) and P. aeruginosa (CRPA), stacked.",
        years="2010-2035",
        method="Anchored to the 2019 baseline of Murray et al. and to the escalation through 2035 reported by Tai et al.; the split by pathogen approximates the GBD breakdown. Values are fixed anchor points, not a fitted model.",
        sources=[("Murray et al., Lancet 2022", MURRAY), ("Tai et al., IJAA 2025", TAI)],
    ),
    # ------------------------------------------------------------- Scenario Lab
    "scenario": dict(
        kind="model", title="The paper's model with your interventions",
        intro="Before the start year the curve is exactly the paper's. From the start year on, your two levers scale the base rate and the acceleration. The exponent is continuous, so the curve bends without jumping.",
        equations=[r"$$y(\tau)=\dfrac{K}{1+A\,e^{-g(\tau)}}$$",
                   r"$$g(\tau)=\begin{cases} r\tau+b\tau^{2} & \tau<\tau_s\\ g(\tau_s)+r(1-s)(\tau-\tau_s)+b(1-p)(\tau^{2}-\tau_s^{2}) & \tau\ge\tau_s\end{cases}$$",
                   r"$$g^{*}=\ln\!\dfrac{95\,A}{K-95}\qquad g(\tau)=g^{*}\;\Rightarrow\;\tau_{95}$$"],
        live=True,
        terms=[_T_Y, _T_R, _T_B,
               dict(key="s", sym="s", name="Stewardship",
                    what="The fraction by which your scenario lowers the base rate r from the start year (prudent prescribing, diagnostics, infection control).",
                    value="0-100 %", source="Your assumption: the paper does not quantify any intervention", control="Slider 1"),
               dict(key="p", sym="p", name="New antibiotics",
                    what="The fraction by which your scenario lowers the acceleration b from the start year (new drug classes, pipeline investment).",
                    value="0-100 %", source="Your assumption", control="Slider 2"),
               dict(key="ts", sym="τₛ", name="Start year",
                    what="The year the intervention begins, counted from 1990. Before it, the curve follows the paper.",
                    value="2026-2045", source="Your assumption", control="Slider 3"),
               dict(key="gstar", sym="g*", name="Threshold exponent",
                    what="The value of the exponent at which the index equals 95. Setting g(τ) = g* gives a quadratic equation in τ whose positive root is the exact threshold year.",
                    value="4.937", source="Derived from K, A and 95", control="-"),
               _T_K, _T_A, _T_TAU],
        sources=[("Model: Prieto Gratacós & Botto, Br J Med Health Res 2026", PAPER)],
    ),
    "rate": dict(
        kind="model", title="Effective rate of resistance growth",
        intro="The yearly growth rate of the exponent. In the paper's model it never stops rising; your levers lower its level (stewardship) and its slope (new antibiotics).",
        equations=[r"$$r_{\mathrm{ef}}(\tau)=\begin{cases} r+2b\tau & \tau<\tau_s\\ r(1-s)+2b(1-p)\,\tau & \tau\ge\tau_s\end{cases}$$"],
        live=True,
        terms=[_T_REFF, _T_R, _T_B,
               dict(key="s", sym="s", name="Stewardship", what="Lowers the level of the line (the r part).",
                    value="0-100 %", source="Your assumption", control="Slider 1"),
               dict(key="p", sym="p", name="New antibiotics", what="Lowers the slope of the line (the 2bτ part).",
                    value="0-100 %", source="Your assumption", control="Slider 2")],
        sources=[("Prieto Gratacós & Botto, Br J Med Health Res 2026 (Discussion)", PAPER)],
    ),
    # ---------------------------------------------------------------- Pathogens
    "heatmap": dict(
        kind="data", title="Resistance by pathogen and antibiotic class",
        what="Percentage of resistant isolates for each pathogen and antibiotic class (approximate global medians). Grey cells are intrinsic resistance or not applicable. Row labels add the WHO priority and the strongest MDR/XDR/PDR phenotype documented in the paper's references.",
        years="Recent surveillance reports (2019-2023)",
        method="Medians read from the surveillance reports; phenotypes per Magiorakos 2012. The what-if panel changes values only in your session:",
        equations=[r"$$v'=\min\!\left(100,\;\max\!\left(0,\;\mathrm{round}\big(v\,(1+\Delta)\big)\right)\right)$$"],
        terms=[dict(key="v", sym="v", name="Literature value", what="The published % resistant for the cell.",
                    value="0-100 %", source="WHO GLASS, EARS-Net, CDC", control="-"),
               dict(key="d", sym="Δ", name="Relative change", what="The bulk change you choose, as a fraction of each literature value (for example +25 % turns 40 into 50).",
                    value="-50 % to +100 %", source="Your assumption", control="Bulk change slider"),
               dict(key="vp", sym="v'", name="Scenario value", what="The new value, rounded and kept between 0 and 100. Intrinsic-resistance cells are never changed.",
                    value="0-100 %", source="-", control="-")],
        sources=[("WHO GLASS Report 2022", GLASS), ("ECDC EARS-Net", EARS), ("CDC AR Threats Report", CDC),
                 ("Murray et al., Lancet 2022", MURRAY), ("Magiorakos et al., Clin Microbiol Infect 2012", MAGIORAKOS)],
    ),
    "regional": dict(
        kind="data", title="Resistance by WHO region",
        what="Resistance rates (%) for four key pathogen-drug combinations in the six WHO regions.",
        years="WHO GLASS 2022 reporting",
        method="Values read from the WHO GLASS report and plotted as given; no model.",
        sources=[("WHO GLASS Report 2022", GLASS)],
    ),
    "trends": dict(
        kind="data", title="25-year trends of key phenotypes",
        what="Resistance (%) over time for MRSA, 3GC-resistant E. coli and carbapenem-resistant K. pneumoniae.",
        years="2000-2025",
        method="Trajectories follow the published surveillance series; points between report years are interpolated for display.",
        sources=[("ECDC EARS-Net", EARS), ("WHO GLASS Report 2022", GLASS), ("CDC NARMS", NARMS)],
    ),
    # -------------------------------------------------------------- Time Series
    "sarima": dict(
        kind="stat", title="Seasonal ARIMA forecast",
        intro="A standard statistical model for monthly series with a yearly season. It is fitted to a synthetic series built to resemble published trends (openly harmonised monthly series per pathogen do not exist), with a fixed random seed so every run is identical.",
        equations=[r"$$(1-\phi B)(1-\Phi B^{12})(1-B)(1-B^{12})\,y_t=(1+\theta B)\,\varepsilon_t$$",
                   r"$$y_t=T(t)+a_1\sin\dfrac{2\pi t}{12}+a_2\sin\dfrac{4\pi t}{12}+\varepsilon_t,\qquad \varepsilon_t\sim\mathcal{N}(0,\sigma^{2})$$"],
        terms=[dict(key="yt", sym="yₜ", name="Monthly value", what="Percentage of resistant isolates in month t.",
                    value="%", source="Synthetic series (seed 42)", control="Pathogen selector"),
               dict(key="B", sym="B", name="Backshift operator", what="Shifts the series one month back: B·yₜ = yₜ₋₁. B¹² goes back one year.",
                    value="-", source="Box-Jenkins notation", control="-"),
               dict(key="d", sym="(1−B)(1−B¹²)", name="Differencing", what="Works with month-to-month and year-to-year changes instead of raw levels, which removes trend and season before modelling.",
                    value="d = 1, D = 1", source="Model order (1,1,1)(1,1,0,12)", control="-"),
               dict(key="phi", sym="φ, Φ", name="Autoregressive terms", what="How much last month (φ) and the same month last year (Φ) carry into the current change.",
                    value="estimated", source="Maximum likelihood (statsmodels)", control="-"),
               dict(key="theta", sym="θ", name="Moving-average term", what="How much last month's forecast error carries into this month.",
                    value="estimated", source="Maximum likelihood (statsmodels)", control="-"),
               dict(key="T", sym="T(t)", name="Trend of the synthetic series", what="The long-term shape given to each synthetic series: a rise and decline for MRSA, a steady rise for 3GC-R E. coli, an accelerating rise for CRE K. pneumoniae. The sine terms add the yearly season.",
                    value="per pathogen", source="Synthetic generator (data/timeseries_data.py)", control="Pathogen selector"),
               dict(key="eps", sym="εₜ", name="Noise", what="The random part the model cannot explain. In the synthetic series it is generated with a fixed seed (42).",
                    value="σ = 0.8-1.2", source="Synthetic generator", control="-"),
               dict(key="ci", sym="95 % CI", name="95 % confidence interval", what="The band where the future value should fall 95 times out of 100 if the model is right. It widens with the horizon.",
                    value="-", source="Model forecast variance", control="Horizon selector")],
        sources=[("Kim et al. 2023 (SARIMA for AMR)", KIM2023), ("Seasonal ARIMA (Hyndman & Athanasopoulos)", BOX_JENKINS)],
    ),
    "ts_scenario": dict(
        kind="model", title="Intervention on the forecast trend",
        intro="The intervention keeps the seasonal pattern and cuts only the monthly trend, from the start month on. The trend is measured with year-over-year changes, which cancel the season. Computed from the forecast already shown: no refit, nothing random.",
        equations=[r"$$m=\dfrac{1}{12}\cdot\overline{\left(\hat y_t-y_{t-12}\right)}$$",
                   r"$$\hat y'_t=\hat y_t-s\cdot\max(m,0)\cdot\max(t-t_0+1,\,0)$$"],
        live=True,
        terms=[dict(key="m", sym="m", name="Monthly trend", what="Average year-over-year change of the forecast, divided by 12, in percentage points per month. If it is negative (resistance already falling), there is nothing to slow and both lines coincide.",
                    value="pp per month", source="Computed from the forecast", control="-"),
               dict(key="yhat", sym="ŷₜ", name="Business as usual", what="The SARIMA forecast for month t.",
                    value="%", source="SARIMA", control="-"),
               dict(key="s", sym="s", name="Trend reduction", what="The share of the monthly trend your intervention removes.",
                    value="0-100 %", source="Your assumption", control="Trend reduction slider"),
               dict(key="t0", sym="t₀", name="Start month", what="The forecast month in which the intervention begins.",
                    value="now, +6, +12, +24", source="Your assumption", control="Start selector"),
               dict(key="yprime", sym="ŷ'ₜ", name="Intervention", what="The forecast with the trend reduced from t₀ on. The 95 % band, if shown, is the business-as-usual band shifted with it.",
                    value="%", source="-", control="-")],
        sources=[("Forecast: SARIMAX(1,1,1)(1,1,0,12)", BOX_JENKINS)],
    ),
    "diagnostics": dict(
        kind="stat", title="Residuals and information criteria",
        intro="Checks of how well the model fits. Residuals should look like random noise around zero; AIC and BIC compare models (lower is better).",
        equations=[r"$$e_t=y_t-\hat y_t\qquad \mathrm{AIC}=2k-2\ln L\qquad \mathrm{BIC}=k\ln n-2\ln L$$"],
        terms=[dict(key="e", sym="eₜ", name="Residual", what="Observed minus fitted value for month t.", value="pp", source="-", control="-"),
               dict(key="k", sym="k", name="Number of parameters", what="How many coefficients the model estimates; AIC and BIC penalise more of them.", value="-", source="-", control="-"),
               dict(key="L", sym="L", name="Likelihood", what="How probable the observed data are under the fitted model.", value="-", source="statsmodels", control="-"),
               dict(key="n", sym="n", name="Observations", what="Number of months in the series.", value="312", source="2000-2025", control="-")],
        sources=[("Seasonal ARIMA (Hyndman & Athanasopoulos)", BOX_JENKINS)],
    ),
    "correlogram": dict(
        kind="stat", title="Autocorrelation (ACF) and partial autocorrelation (PACF)",
        intro="How much the series resembles itself k months earlier. Bars outside the bands are significant; a spike at lag 12 confirms the yearly season.",
        equations=[r"$$\rho_k=\dfrac{\sum_t (y_t-\bar y)(y_{t-k}-\bar y)}{\sum_t (y_t-\bar y)^{2}}$$"],
        numeric=(r"$$\pm\dfrac{1.96}{\sqrt{n}}$$",),
        terms=[dict(key="rho", sym="ρₖ", name="Autocorrelation at lag k", what="Correlation between the series and itself shifted k months.", value="-1 to 1", source="-", control="-"),
               dict(key="lag", sym="k", name="Lag", what="Number of months of shift.", value="0-36", source="-", control="-"),
               dict(key="band", sym="±1.96/√n", name="Significance bands", what="Bars beyond these lines are unlikely to be chance (95 % level); n is the number of months.", value="-", source="-", control="-"),
               dict(key="pacf", sym="PACF", name="Partial autocorrelation", what="The same correlation after removing the effect of the intermediate lags; it suggests how many autoregressive terms are needed.", value="-1 to 1", source="-", control="-")],
        sources=[("Seasonal ARIMA (Hyndman & Athanasopoulos)", BOX_JENKINS)],
    ),
    # ----------------------------------------------------------------- Industry
    "pubmed": dict(
        kind="model", title="Publications on antibiotic resistance",
        intro="Yearly PubMed results for 'antibiotic resistance', approximated with a closed-form exponential that matches the published search (about 250,000 results up to 2025).",
        equations=[r"$$N(y)=N_0\,e^{g\,(y-1990)}$$"],
        numeric=(r"$$N(y)=500\,e^{0.115\,(y-1990)}$$",),
        terms=[dict(key="N", sym="N(y)", name="Papers in year y", what="Number of PubMed results published that year.", value="-", source="PubMed search", control="-"),
               dict(key="N0", sym="N₀", name="1990 level", what="Approximate number of papers in 1990.", value="500", source="Matched to the PubMed histogram", control="-"),
               dict(key="g", sym="g", name="Growth rate", what="Yearly growth of publications: about 12 % per year (e^0.115 ≈ 1.12).", value="0.115", source="Matched to the PubMed histogram", control="-")],
        sources=[("PubMed search 'antibiotic resistance'", PUBMED)],
    ),
    "market": dict(
        kind="model", title="Antibiotic-resistance market",
        intro="Market size compounded at the growth rate published by Univdatos from its 2023 base.",
        equations=[r"$$M(y)=M_{2023}\,(1+c)^{\,y-2023}$$"],
        numeric=(r"$$M(y)=5.5\,(1.054)^{\,y-2023}$$",),
        terms=[dict(key="M", sym="M(y)", name="Market size", what="Revenue of the antibiotic-resistance market in year y, in billions of US dollars.", value="USD bn", source="Univdatos", control="-"),
               dict(key="M0", sym="M₂₀₂₃", name="Base year size", what="Market size in 2023.", value="5.5", source="Univdatos", control="-"),
               dict(key="c", sym="c", name="CAGR", what="Compound annual growth rate: the market grows 5.4 % per year.", value="0.054", source="Univdatos (2024-2032 report)", control="-")],
        sources=[("Univdatos, Antibiotic Resistance Market", UNIVDATOS)],
    ),
    "classes": dict(
        kind="model", title="Market by drug class",
        intro="Each drug class receives its share of the total market in 2023 and 2032.",
        equations=[r"$$M_c(y)=s_c(y)\cdot M(y)$$"],
        terms=[dict(key="Mc", sym="M_c(y)", name="Class market", what="Revenue of drug class c in year y, in billions of US dollars.", value="USD bn", source="-", control="-"),
               dict(key="share", sym="s_c(y)", name="Class share", what="Percentage of the market for each class (oxazolidinones, lipoglycopeptides, tetracyclines, others), read from the Univdatos figure.", value="30 / 26 / 24 / 20 % (2023)", source="Univdatos", control="-"),
               dict(key="M", sym="M(y)", name="Total market", what="From the market chart.", value="USD bn", source="Univdatos", control="-")],
        sources=[("Univdatos, Antibiotic Resistance Market", UNIVDATOS)],
    ),
    "divergence": dict(
        kind="model", title="Awareness vs effectiveness",
        intro="Two indices that start at 1 in 1990: collective awareness (cumulative papers) and therapeutic effectiveness (what resistance leaves). One multiplies, the other shrinks.",
        equations=[r"$$C(y)=\dfrac{\sum_{x\le y}N(x)}{N(1990)}\qquad E(y)=\dfrac{100-y(\tau)}{100-y(0)}$$"],
        terms=[dict(key="C", sym="C(y)", name="Awareness index", what="Cumulative PubMed publications up to year y, relative to 1990.", value="1 → about 500", source="PubMed model", control="-"),
               dict(key="E", sym="E(y)", name="Effectiveness index", what="What resistance leaves (100 minus the index), relative to 1990.", value="1 → about 0.34", source="Super-exponential model", control="-"),
               dict(key="log", sym="log", name="Log scale", what="The vertical axis is logarithmic so both indices fit in one chart.", value="-", source="-", control="-")],
        sources=[("PubMed", PUBMED), ("Prieto Gratacós & Botto, Br J Med Health Res 2026", PAPER)],
    ),
    # ------------------------------------------------------------- Data sources
    "coverage": dict(
        kind="data", title="Time coverage of each source",
        what="The years each surveillance or burden source covers.",
        years="1990-2025",
        method="Taken from each source's documentation; bars show the first and last year with data.",
        sources=[("WHO GLASS", GLASS), ("ECDC EARS-Net", EARS), ("CDC AR Threats Report", CDC), ("Murray et al., Lancet 2022", MURRAY)],
    ),
}

KIND_LABEL = {"model": "Model", "stat": "Statistical model", "data": "Data"}


def _md(tex):
    return dcc.Markdown(tex, mathjax=True, className="mc-eq")


def _numeric_block(tex_en):
    """Same equation with numbers, in both decimal styles; CSS shows one."""
    tex_es = tex_en.replace(".", "{,}")
    return html.Div([
        html.Div(_md(tex_en), className="only-en"),
        html.Div(_md(tex_es), className="only-es"),
    ], className="mc-numeric")


def _terms_table(terms):
    return html.Div(html.Table([
        html.Thead(html.Tr([html.Th("Symbol"), html.Th("What it is"), html.Th("Value"),
                            html.Th("Where it comes from"), html.Th("What the control does")])),
        html.Tbody([html.Tr([
            html.Td(t["sym"], className="mc-sym"), html.Td(t["what"]), html.Td(t["value"], className="mc-num"),
            html.Td(t["source"]), html.Td(t["control"]),
        ]) for t in terms]),
    ], className="mc-table"), className="mc-table-box")


def _term_picker(key, terms):
    return html.Div([
        html.Div("Pick a term to see what it means:", className="mc-pick-label"),
        dcc.RadioItems(
            id={"type": "mc-term", "card": key},
            options=[{"label": t["sym"], "value": t["key"]} for t in terms],
            value=terms[0]["key"], inline=True, className="mc-chips",
            inputClassName="mc-chip-input", labelClassName="mc-chip",
        ),
        html.Div(id={"type": "mc-help", "card": key}, className="mc-help"),
    ])


def _sources(sources):
    parts = [html.Span("Sources: ", className="source-label")]
    for i, (label, url) in enumerate(sources):
        if i:
            parts.append(" · ")
        parts.append(html.A(label, href=url, target="_blank"))
    return html.Div(parts, className="mc-sources")


def model_card(key, open=False):
    """Collapsible card with the equation and terms of chart `key`."""
    c = CARDS[key]
    kind = c["kind"]
    summary_label = "Data behind this chart" if kind == "data" else "Equation and terms of this chart"
    body = [html.Div([html.Span(KIND_LABEL[kind], className=f"mc-kind mc-kind-{kind}"),
                      html.Span(c["title"], className="mc-title")], className="mc-head")]
    if kind == "data":
        body.append(html.Dl([
            html.Dt("What the numbers are"), html.Dd(c["what"]),
            html.Dt("Years"), html.Dd(c["years"]),
            html.Dt("How they were obtained"), html.Dd(c["method"]),
        ], className="mc-data"))
        for tex in c.get("equations", []):
            body.append(_md(tex))
        if c.get("terms"):
            body.append(_terms_table(c["terms"]))
    else:
        body.append(html.P(c["intro"], className="mc-intro"))
        body.append(html.Div([_md(t) for t in c["equations"]], className="mc-eqs"))
        if c.get("live"):
            body.append(html.Div([
                html.Div("With the current values:", className="mc-pick-label"),
                html.Div(id={"type": "mc-live", "card": key}, className="mc-numeric"),
            ]))
        for tex in c.get("numeric", ()):
            body.append(html.Div([html.Div("With the paper's values:", className="mc-pick-label"),
                                  _numeric_block(tex)]))
        body.append(_term_picker(key, c["terms"]))
        body.append(html.Details([html.Summary("All terms in a table", className="mc-table-toggle"),
                                  _terms_table(c["terms"])], className="mc-table-details", open=True))
    body.append(_sources(c["sources"]))
    return html.Details([
        html.Summary([html.Span("ƒ(x)" if kind != "data" else "ⓘ", className="mc-badge"),
                      html.Span(summary_label, className="mc-summary-text")], className="mc-summary"),
        html.Div(body, className="mc-body"),
    ], className="model-card", open=open)


def live_equation(tex_en, lang):
    """Live equation (scenario pages) in the visitor's decimal style."""
    tex = tex_en.replace("$$$$", "$$\n\n$$")
    return _md(tex.replace(".", "{,}") if lang == "es" else tex)


@callback(Output({"type": "mc-help", "card": MATCH}, "children"),
          Input({"type": "mc-term", "card": MATCH}, "value"),
          State({"type": "mc-term", "card": MATCH}, "id"))
@translated
def show_term(term_key, ident):
    terms = CARDS[ident["card"]]["terms"]
    t = next((t for t in terms if t["key"] == term_key), terms[0])
    rows = [html.Div([html.Span(t["sym"], className="mc-help-sym"), html.Span(t["name"], className="mc-help-name")],
                     className="mc-help-head"),
            html.P(t["what"])]
    meta = []
    if t["value"] not in ("-", ""):
        meta.append([html.Span("Value: ", className="mc-help-k"), html.Span(t["value"], className="mc-num")])
    if t["source"] not in ("-", ""):
        meta.append([html.Span("Source: ", className="mc-help-k"), t["source"]])
    if t["control"] not in ("-", ""):
        meta.append([html.Span("Control: ", className="mc-help-k"), t["control"]])
    if meta:
        parts = []
        for i, m in enumerate(meta):
            if i:
                parts.append(html.Span(" · ", className="mc-help-sep"))
            parts.extend(m)
        rows.append(html.P(parts, className="mc-help-meta"))
    return rows
