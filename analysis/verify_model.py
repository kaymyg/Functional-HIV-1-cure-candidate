import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

# ---------------- 5-state model (as supplied) ----------------
def m5(t, y, p):
    Cp, Ct, B, Poff, Tex = y
    dCp = -(p['k10'] + p['k12']) * Cp + p['k21'] * Ct
    dCt = p['k12'] * Cp - p['k21'] * Ct - p['k_elim_t'] * Ct
    dB = p['k_rel'] * np.exp(-0.1 * t) - p['deg_b'] * B
    koff = p['koff_max'] * (B / (p['EC50_brec'] + B))
    dPoff = koff * (1.0 - Poff) - p['kon'] * Poff
    taz = Ct / (p['EC50_taz'] + Ct)
    dTex = -p['gamma_exhaust'] * taz * Tex + p['baseline_exhaust'] * (1.0 - Tex)
    return [dCp, dCt, dB, dPoff, dTex]

base = dict(k10=.15, k12=.30, k21=.20, k_elim_t=.1, k_rel=2.5, deg_b=1.2,
            kon=.02, koff_max=5.0, EC50_brec=.5, EC50_taz=1.2,
            gamma_exhaust=.8, baseline_exhaust=.05)

def run5(k_rel=2.5, brec0=10.0, cp0=0.0, koff_max=5.0, ec50=0.5):
    p = dict(base, k_rel=k_rel, koff_max=koff_max, EC50_brec=ec50)
    s = solve_ivp(lambda t, y: m5(t, y, p), (0, 30), [cp0, 0, brec0, .05, .85],
                  t_eval=np.linspace(0, 30, 300), method='RK45')
    return s

print("=" * 72)
print("TEST 1  Does P_off actually depend on anything? (5-state model)")
print("=" * 72)
print(f"{'k_rel':>8} {'Brec0':>8} {'koff_max':>9} {'EC50':>6} | {'final P_off %':>13}")
for k_rel in [0.5, 2.5, 5.0]:
    for brec0 in [2.0, 10.0, 40.0]:
        s = run5(k_rel=k_rel, brec0=brec0)
        print(f"{k_rel:>8.2f} {brec0:>8.1f} {5.0:>9.1f} {0.5:>6.2f} | {s.y[3,-1]*100:>13.3f}")
# extreme stress: collapse the drug almost entirely
s = run5(k_rel=0.05, brec0=0.1, koff_max=2.0, ec50=1.2)
print(f"\n  Near-null dose (k_rel=0.05, Brec0=0.1, koff_max=2, EC50=1.2): "
      f"P_off = {s.y[3,-1]*100:.3f}%")

print("\n" + "=" * 72)
print("TEST 2  Cmax in the Pareto / optimizer scripts")
print("=" * 72)
for taz in [0.5, 2.0, 8.0, 10.0]:
    s = run5(cp0=taz * 0.5)
    print(f"  taz_dose={taz:>5.1f} -> y0[0]={taz*0.5:>5.2f}, "
          f"Cmax={np.max(s.y[0]):>5.2f} mg/L, toxicity threshold=5.0 "
          f"-> penalty {'ACTIVE' if np.max(s.y[0])>5 else 'never fires'}")

# ---------------- 8-state sanctuary model ----------------
def m8(t, y, params):
    Cp, Ct, Cl, Cm, B, Pl, Pm, Tex = y
    k10, k12, k21, k_lymph, k_macro, k_elim_t = params
    ph = 1.2 + 0.8 * np.exp(-0.05 * t)
    k_rel = 2.0 * ph
    dCp = -(k10 + k12 + k_lymph + k_macro) * Cp + k21 * Ct
    dCt = k12 * Cp - k21 * Ct - k_elim_t * Ct
    dCl = k_lymph * Cp - 0.2 * Cl
    dCm = k_macro * Cp - 0.15 * Cm
    dB = k_rel * np.exp(-0.1 * t) - 1.2 * B
    sat = B / (0.5 + B)
    dPl = 5.0 * sat * (1 - Pl) - 0.02 * Pl
    dPm = 5.0 * 0.7 * sat * (1 - Pm) - 0.02 * Pm
    taz = (Cl + Ct) / (1.2 + (Cl + Ct))
    dTex = -0.8 * taz * Tex + 0.05 * (1 - Tex)
    return [dCp, dCt, dCl, dCm, dB, dPl, dPm, dTex]

def score(kl, km):
    s = solve_ivp(lambda t, y: m8(t, y, [.15, .25, .20, kl, km, .1]), (0, 30),
                  [2, 0, 0, 0, 15, .05, .02, .85],
                  t_eval=np.linspace(0, 30, 100), method='RK45')
    return 0.6 * s.y[5, -1] * 100 + 0.4 * s.y[6, -1] * 100

print("\n" + "=" * 72)
print("TEST 3  Does the 'eradication score' depend on k_lymph / k_macro?")
print("=" * 72)
print(f"{'k_lymph':>9} {'k_macro':>9} | {'weighted score %':>18}")
pts = [(.02, .02), (.05, .05), (.10, .08), (.15, .15), (.25, .25), (.35, .35)]
vals = []
for kl, km in pts:
    v = score(kl, km)
    vals.append(v)
    print(f"{kl:>9.2f} {km:>9.2f} | {v:>18.10f}")
print(f"\n  TOTAL SPREAD across the entire searched domain: "
      f"{max(vals)-min(vals):.3e} percentage points")

print("\n" + "=" * 72)
print("TEST 4  What the optimizer therefore reports")
print("=" * 72)
best, mc = None, np.inf
for x0 in [[.05, .05], [.15, .15], [.25, .25], [.10, .20]]:
    r = minimize(lambda x: -score(x[0], x[1]), x0, method='L-BFGS-B',
                 bounds=[(.02, .35), (.02, .35)], options={'ftol': 1e-8})
    print(f"  start {x0} -> optimum ({r.x[0]:.4f}, {r.x[1]:.4f}), "
          f"score {-r.fun:.6f}%, nit={r.nit}")
    if r.fun < mc:
        mc, best = r.fun, r
print(f"\n  'Optimal lymphatic-to-peripheral ratio' reported = "
      f"{(best.x[0]+best.x[1])/0.25:.4f}")
print("  ...which is just the starting guess, unchanged.")
