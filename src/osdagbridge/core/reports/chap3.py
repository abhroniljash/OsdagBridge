# =============================================================================
# Chapter 3: Loads and Load Combinations
# Refactored for OsdagBridge Report Generator:
#   - Distinct Vehicle Live Loads table (Table 3.3) matching required multi-level schema
#   - Distinct Footpath Live Load table (Table 3.4)
#   - PyLaTeX LongTable with repeated headers (\endfirsthead, \endhead, \endfoot, \endlastfoot)
#   - Consumes styles and formatting rules from styles.py (SSOT)
# =============================================================================

from osdagbridge.core.utils.common import (
    KEY_CB_LOAD,
    KEY_LL_CUSTOM_VEHICLES,
    KEY_LL_ECCENTRICITY,
    KEY_LL_FOOTPATH_PRESSURE_MODE,
    KEY_LL_FOOTPATH_PRESSURE_VALUE,
    KEY_LL_IRC_70R_BOGIE,
    KEY_LL_IRC_70R_TRACKED,
    KEY_LL_IRC_70R_WHEELED,
    KEY_LL_IRC_AA_TRACKED,
    KEY_LL_IRC_AA_WHEELED,
    KEY_LL_IRC_CLASS_A,
    KEY_LL_IRC_CLASS_FATIGUE,
    KEY_LL_IRC_CLASS_SV,
    KEY_BL_IRC_CLASS_SV,
    KEY_MATERIAL_DECK_DENSITY,
    KEY_MATERIAL_GIRDER_DENSITY,
    KEY_PL_SELF_WEIGHT_FACTOR,
    KEY_RL_LOAD_VALUE,
    KEY_SL_DAMPING,
    KEY_SL_DEAD_LOAD_MODE,
    KEY_SL_DEAD_LOAD_VALUE,
    KEY_SL_HORIZONTAL_COEFF,
    KEY_SL_IMPORTANCE_FACTOR,
    KEY_SL_LIVE_LOAD_MODE,
    KEY_SL_LIVE_LOAD_VALUE,
    KEY_SL_SEISMIC_ZONE,
    KEY_SL_SOIL_TYPE,
    KEY_SL_SPECTRAL_COEFF,
    KEY_SL_TIME_PERIOD,
    KEY_SL_VERTICAL_COEFF,
    KEY_SL_ZONE_FACTOR,
    KEY_SPAN,
    KEY_TL_BRIDGE_TEMP_MAX,
    KEY_TL_BRIDGE_TEMP_MIN,
    KEY_TL_HIGHEST_MAX_TEMP,
    KEY_TL_LOWEST_MIN_TEMP,
    KEY_TL_TEMP_FALL,
    KEY_TL_TEMP_RISE,
    KEY_TS_FOOTPATH_WIDTH,
    KEY_TS_NO_OF_FOOTPATHS,
    KEY_WC_LD_LANE_TABLE_COUNT,
    KEY_WC_MATERIAL,
    KEY_WC_THICKNESS,
    KEY_WL_AVG_EXPOSED_HEIGHT,
    KEY_WL_BASIC_WIND_SPEED,
    KEY_WL_HOURLY_MEAN_WIND,
    KEY_WL_HOURLY_WIND_PRESSURE,
    KEY_WL_LONGITUDINAL_WIND_FORCE,
    KEY_WL_TERRAIN_TYPE,
    KEY_WL_TRANSVERSE_WIND_FORCE,
    KEY_WL_VERTICAL_WIND_FORCE
)

from osdagbridge.core.reports.report_utils import _tex, _render_value
from osdagbridge.core.reports.styles import build_longtable_header
from osdagbridge.core.utils.codes.irc6_2017 import IRC6_2017


def ch3_loads(input_dict):
    span_val = input_dict.get(KEY_SPAN)
    span_m = float(span_val) if span_val not in (None, "") else 30.0
    lanes_val = input_dict.get(KEY_WC_LD_LANE_TABLE_COUNT)
    lanes_int = int(lanes_val) if lanes_val not in (None, "") else 2

    # Global eccentricity from Loading Tab (default 1.2 m above carriageway surface)
    ecc_str = str(input_dict.get(KEY_LL_ECCENTRICITY) or "1.2").strip()
    if not ecc_str.endswith("m"):
        ecc_display = f"{ecc_str} m"
    else:
        ecc_display = ecc_str

    # Calculate standard braking loads per IRC 6 Cl. 211
    try:
        braking_force_t = IRC6_2017.cl_211_2_braking_force(lanes_int)
        braking_force_kN = braking_force_t * 9.80665
        braking_val_str = f"{braking_force_kN:.2f}"
    except Exception:
        braking_val_str = "200.00"

    # Compute Impact Factors
    try:
        im_a = 1.0 + IRC6_2017.cl_208_2_impact_factor(span_m)
        im_a_str = f"{im_a:.3f}"
    except Exception:
        im_a_str = "1.150"

    try:
        im_heavy = 1.0 + IRC6_2017.cl_208_3_impact_factor(span_m)
        im_heavy_str = f"{im_heavy:.3f}"
    except Exception:
        im_heavy_str = "1.100"

    # Build Vehicle Live Load rows based dynamically on UI selection
    vehicle_rows = []

    # 1. Class A
    if input_dict.get(KEY_LL_IRC_CLASS_A, True):
        vehicle_rows.append(
            r"Class A & 554.0 & " + im_a_str + r" & Yes & " + braking_val_str + r" & " + ecc_display + r" \\[4pt]" + "\n\\hline"
        )

    # 2. Class 70R (Wheeled)
    if input_dict.get(KEY_LL_IRC_70R_WHEELED, True):
        vehicle_rows.append(
            r"Class 70R (Wheeled) & 1000.0 & " + im_heavy_str + r" & Yes & " + braking_val_str + r" & " + ecc_display + r" \\[4pt]" + "\n\\hline"
        )

    # 3. Class 70R (Tracked)
    if input_dict.get(KEY_LL_IRC_70R_TRACKED, True):
        vehicle_rows.append(
            r"Class 70R (Tracked) & 700.0 & " + im_heavy_str + r" & Yes & " + braking_val_str + r" & " + ecc_display + r" \\[4pt]" + "\n\\hline"
        )

    # 4. Class AA (Wheeled)
    if input_dict.get(KEY_LL_IRC_AA_WHEELED, False):
        vehicle_rows.append(
            r"Class AA (Wheeled) & 400.0 & " + im_heavy_str + r" & Yes & 80.00 & " + ecc_display + r" \\[4pt]" + "\n\\hline"
        )

    # 5. Class AA (Tracked)
    if input_dict.get(KEY_LL_IRC_AA_TRACKED, False):
        vehicle_rows.append(
            r"Class AA (Tracked) & 700.0 & " + im_heavy_str + r" & Yes & 140.00 & " + ecc_display + r" \\[4pt]" + "\n\\hline"
        )

    # 6. Class SV (Special Vehicle per IRC 6 Annexure B)
    if input_dict.get(KEY_LL_IRC_CLASS_SV, True):
        sv_braking_considered = "Yes" if input_dict.get(KEY_BL_IRC_CLASS_SV, False) else "No"
        sv_braking_val = f"{3850.0 * 0.2:.2f}" if sv_braking_considered == "Yes" else "---"
        sv_braking_ecc = ecc_display if sv_braking_considered == "Yes" else "---"
        vehicle_rows.append(
            r"Class SV & 3850.0 & 1.000\sdstar & " + sv_braking_considered + r" & " + sv_braking_val + r" & " + sv_braking_ecc + r" \\[4pt]" + "\n\\hline"
        )

    # 7. Class 70R (Bogie)
    if input_dict.get(KEY_LL_IRC_70R_BOGIE, False):
        vehicle_rows.append(
            r"Class 70R (Bogie) & 400.0 & " + im_heavy_str + r" & Yes & 80.00 & " + ecc_display + r" \\[4pt]" + "\n\\hline"
        )

    # 8. Class Fatigue
    if input_dict.get(KEY_LL_IRC_CLASS_FATIGUE, True):
        vehicle_rows.append(
            r"Class Fatigue & 390.0 & 1.000 & No & --- & --- \\[4pt]" + "\n\\hline"
        )

    # Custom vehicles from UI
    custom = input_dict.get(KEY_LL_CUSTOM_VEHICLES)
    if custom and isinstance(custom, list):
        for c in custom:
            if isinstance(c, dict) and c.get('name'):
                c_name = _tex(c['name'])
                c_load = f"{float(c.get('total_load', 500)):.1f}"
                vehicle_rows.append(
                    f"{c_name} & {c_load} & 1.000 & Yes & 100.00 & {ecc_display} \\\\[4pt]\n\\hline"
                )

    if not vehicle_rows:
        vehicle_rows.append(r"Class A & 554.0 & " + im_a_str + r" & Yes & " + braking_val_str + r" & " + ecc_display + r" \\[4pt]" + "\n\\hline")

    vehicle_rows_tex = "\n".join(vehicle_rows)

    # ─────────────────────────────────────────────────────────────────────────
    # Footpath Live Load Analysis & Dedicated Table
    # ─────────────────────────────────────────────────────────────────────────
    n_footpaths = int(input_dict.get(KEY_TS_NO_OF_FOOTPATHS, 0) or 0)
    fp_width = float(input_dict.get(KEY_TS_FOOTPATH_WIDTH, 0.0) or 0.0)
    fp_mode = str(input_dict.get(KEY_LL_FOOTPATH_PRESSURE_MODE, "As per IRC 6")).strip()
    fp_user_val = input_dict.get(KEY_LL_FOOTPATH_PRESSURE_VALUE)

    if n_footpaths > 0:
        if fp_mode.lower() in ("as per irc 6", "as per irc6", "automatic"):
            try:
                fp_intensity = IRC6_2017.cl_206_1_footway_load()
            except Exception:
                fp_intensity = 4.0
            fp_intensity_str = f"{fp_intensity:.3f} kN/m\\textsuperscript{{2}}"
            fp_clause_str = "IRC 6:2017 Cl. 206.1"
        elif fp_user_val not in (None, ""):
            fp_intensity_str = f"{float(fp_user_val):.3f} kN/m\\textsuperscript{{2}}"
            fp_clause_str = "User Input"
        else:
            fp_intensity_str = "4.000 kN/m\\textsuperscript{2}"
            fp_clause_str = "IRC 6 Cl. 206 Default"
        
        fp_total_area = n_footpaths * fp_width * span_m
        fp_total_load = fp_total_area * (float(fp_user_val) if (fp_user_val not in (None, "") and fp_mode.lower() != "as per irc 6") else 4.0)
        fp_total_load_str = f"{fp_total_load:.2f} kN"
        fp_status_str = f"Provided ({n_footpaths} No., Width = {fp_width:.2f} m)"
    else:
        fp_status_str = "Not Provided (No Footpath on Deck)"
        fp_intensity_str = "N/A"
        fp_clause_str = "IRC 6 Cl. 206"
        fp_total_load_str = "N/A"

    # Wind Load parameters
    vz_val = input_dict.get(KEY_WL_HOURLY_MEAN_WIND)
    pz_val = input_dict.get(KEY_WL_HOURLY_WIND_PRESSURE)
    if not vz_val or not pz_val:
        try:
            _vb = input_dict.get(KEY_WL_BASIC_WIND_SPEED) or input_dict.get('wind_speed') or 44.0
            _h = input_dict.get(KEY_WL_AVG_EXPOSED_HEIGHT) or 10.0
            _ter = {
                "Plain Terrain": "plain",
                "Terrain with Obstructions": "obstructed",
            }.get(str(input_dict.get(KEY_WL_TERRAIN_TYPE, "")).strip(), "plain")
            _res = IRC6_2017.table_12(float(_h), _ter, float(_vb))
            if not vz_val:
                vz_val = _res.get("Vz")
            if not pz_val:
                pz_val = _res.get("Pz")
        except Exception:
            pass
    vz_str = f"{float(vz_val):.2f} m/s" if vz_val not in (None, "") else "N/A"
    pz_str = f"{float(pz_val):.2f} N/m\\textsuperscript{{2}}" if pz_val not in (None, "") else "N/A"

    # Seismic parameters
    sl_zone_factor = input_dict.get(KEY_SL_ZONE_FACTOR)
    sl_spectral = input_dict.get(KEY_SL_SPECTRAL_COEFF)
    sl_ah = input_dict.get(KEY_SL_HORIZONTAL_COEFF)
    sl_av = input_dict.get(KEY_SL_VERTICAL_COEFF)
    if not sl_ah or not sl_zone_factor:
        try:
            _zone = input_dict.get(KEY_SL_SEISMIC_ZONE) or input_dict.get('seismic_zone') or "IV"
            _zmap = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V"}
            _z = str(_zone).strip().upper()
            if _z.isdigit():
                _z = _zmap.get(_z, "IV")
            _smap = {"Type I – Rocky or Hard": 1, "Type II – Medium Soil": 2, "Type III – Soft Soil": 3}
            _st = _smap.get(str(input_dict.get(KEY_SL_SOIL_TYPE, "")), 1)
            _tp = input_dict.get(KEY_SL_TIME_PERIOD) or 0.5
            _damp = input_dict.get(KEY_SL_DAMPING) or 2.0
            _res = IRC6_2017.cl_218_5_1(zone=f"Zone {_z}", soil_type=_st, dead_load_kN=100.0,
                                        live_load_kN=50.0, period_T=float(_tp),
                                        damping_percent=float(_damp))
            if not sl_zone_factor:
                sl_zone_factor = _res.get("Z")
            if not sl_spectral:
                sl_spectral = _res.get("Sa_g_adjusted")
            if not sl_ah:
                sl_ah = _res.get("Ah")
            if not sl_av:
                sl_av = round(_res.get("Ah", 0) * 2 / 3, 4)
        except Exception:
            pass

    # Temperature parameters
    tl_temp_min = tl_temp_max = tl_rise = tl_fall = "N/A"
    try:
        _tmax = input_dict.get(KEY_TL_HIGHEST_MAX_TEMP) or input_dict.get('shade_temp_max') or 42.0
        _tmin = input_dict.get(KEY_TL_LOWEST_MIN_TEMP) or input_dict.get('shade_temp_min') or 8.0
        if _tmax and _tmin:
            _res = IRC6_2017.cl_215_2_effective_bridge_temperature(float(_tmax), float(_tmin), 'metallic', False)
            _bt_min = _res.get('T_min', 0)
            _bt_max = _res.get('T_max', 0)
            _mean = (_bt_max + _bt_min) / 2.0
            tl_temp_min = f"{_bt_min:.2f}"
            tl_temp_max = f"{_bt_max:.2f}"
            tl_rise = f"{_bt_max - _mean:.2f}"
            tl_fall = f"{_mean - _bt_min:.2f}"
    except Exception:
        pass

    # Load Combinations
    _LOAD_LABEL_MAP = {
        'dead_load': 'DL',
        'surfacing': 'SIDL',
        'live_load': 'LL',
        'wind_load': 'WL',
        'thermal_load': 'TL',
        'vehicle_collision': 'VC',
        'barge_impact': 'BI',
        'floating_bodies': 'FB',
        'seismic': 'EQ',
    }

    def _fmt_factors(factors):
        parts = []
        for load, val in factors.items():
            label = _LOAD_LABEL_MAP.get(load, load.upper())
            if isinstance(val, dict):
                add = val.get('adding')
                rel = val.get('relieving')
                add_s = f"{add:.2f}" if add is not None else '--'
                rel_s = f"{rel:.2f}" if rel is not None else '--'
                parts.append(f"{label}({add_s}/{rel_s})")
            else:
                if val is None:
                    continue
                parts.append(f"{label}({val:.2f})")
        return ' + '.join(parts)

    uls_combos = IRC6_2017.uls_load_combinations()
    sls_combos = IRC6_2017.sls_load_combinations()
    lc_rows = []
    for i, combo in enumerate(uls_combos, start=1):
        cases = _fmt_factors(combo['factors'])
        lc_rows.append(f"ULS-{i:02d} & {cases} \\\\[4pt]\n\\hline")
    for i, combo in enumerate(sls_combos, start=1):
        cases = _fmt_factors(combo['factors'])
        lc_rows.append(f"SLS-{i:02d} & {cases} \\\\[4pt]\n\\hline")
    lc_rows_str = "\n".join(lc_rows)

    return r"""
\chapter{Loads and Load Combinations}
\label{ch:loads}

This section summarizes all permanent, transient, environmental, and accidental load cases applied to the bridge structure. All loads and combinations adhere to IRC 6:2017 specifications.

\vspace{0.5em}
\begin{longtable}{|L{6.0cm}|p{9.5cm}|}
\caption{\textbf{Dead Load --- Self Weight}} \label{tab:dead-load} \\
\hline
\textbf{Parameter} & \textbf{Design Value} \\[4pt]
\hline
\endfirsthead
\caption[]{\textbf{Dead Load --- Self Weight} \textit{(Continued)}} \\
\hline
\textbf{Parameter} & \textbf{Design Value} \\[4pt]
\hline
\endhead
\hline
\multicolumn{2}{|r|}{\textit{\small Continued on next page...}} \\
\hline
\endfoot
\hline
\endlastfoot
\textnormal{Structural Steel Density} & """ + (_render_value(input_dict, KEY_MATERIAL_GIRDER_DENSITY, r' kN/m\textsuperscript{3}')) + r""" \\[5pt]
\hline
\textnormal{Concrete Deck Slab Density} & """ + (_render_value(input_dict, KEY_MATERIAL_DECK_DENSITY, r' kN/m\textsuperscript{3}')) + r""" \\[5pt]
\hline
\textnormal{Self-Weight Amplification Factor} & """ + (_render_value(input_dict, KEY_PL_SELF_WEIGHT_FACTOR)) + r""" \\[5pt]
\hline
\end{longtable}

\vspace{0.8em}
\begin{longtable}{|L{6.0cm}|p{9.5cm}|}
\caption{\textbf{Dead Load for Surfacing \& Superimposed Dead Loads (SIDL)}} \label{tab:sidl} \\
\hline
\textbf{Parameter} & \textbf{Design Value} \\[4pt]
\hline
\endfirsthead
\caption[]{\textbf{Dead Load for Surfacing \& SIDL} \textit{(Continued)}} \\
\hline
\textbf{Parameter} & \textbf{Design Value} \\[4pt]
\hline
\endhead
\hline
\multicolumn{2}{|r|}{\textit{\small Continued on next page...}} \\
\hline
\endfoot
\hline
\endlastfoot
\textnormal{Wearing Course Material \& Thickness} & """ + (_render_value(input_dict, KEY_WC_MATERIAL)) + r""" x """ + (_render_value(input_dict, KEY_WC_THICKNESS, ' mm')) + r""" \\[5pt]
\hline
\textnormal{Crash Barrier Load} & """ + (_render_value(input_dict, KEY_CB_LOAD, ' kN/m per barrier')) + r""" \\[5pt]
\hline
\textnormal{Railing Load} & """ + (_render_value(input_dict, KEY_RL_LOAD_VALUE, r' kN/m\sdstar')) + r""" \\[5pt]
\hline
\end{longtable}

\vspace{0.8em}
% ── Table 3.3: Refactored Live Loads Table (Multi-level header matching requirements) ──
\begin{longtable}{|L{3.2cm}|C{2.4cm}|C{2.3cm}|C{2.0cm}|C{2.4cm}|C{2.2cm}|}
\caption{\textbf{Vehicle Live Loads (LL) --- per IRC 6:2017}} \label{tab:live-loads} \\
\hline
\multirow{2}{*}{\textbf{Vehicle}} & \multirow{2}{*}{\textbf{Total Load (kN)}} & \multirow{2}{*}{\textbf{Impact Factor}} & \multicolumn{3}{c|}{\textbf{Braking Load}} \\
\cline{4-6}
& & & \textbf{Considered?} & \textbf{Value (kN)} & \textbf{Eccentricity} \\[4pt]
\hline
\endfirsthead
\caption[]{\textbf{Vehicle Live Loads (LL)} \textit{(Continued)}} \\
\hline
\multirow{2}{*}{\textbf{Vehicle}} & \multirow{2}{*}{\textbf{Total Load (kN)}} & \multirow{2}{*}{\textbf{Impact Factor}} & \multicolumn{3}{c|}{\textbf{Braking Load}} \\
\cline{4-6}
& & & \textbf{Considered?} & \textbf{Value (kN)} & \textbf{Eccentricity} \\[4pt]
\hline
\endhead
\hline
\multicolumn{6}{|r|}{\textit{\small Continued on next page...}} \\
\hline
\endfoot
\hline
\endlastfoot
""" + vehicle_rows_tex + r"""
\end{longtable}
\noindent\textit{Note: Live load models reflect configurations active in the Loading Tab. Braking forces are evaluated per IRC 6:2017 Cl. 211 with application point at the specified eccentricity above road level.}

\vspace{0.8em}
% ── Table 3.4: Distinct Footpath / Pedestrian Live Load Table ──
\begin{longtable}{|L{6.0cm}|p{9.5cm}|}
\caption{\textbf{Footway / Footpath Live Load (per IRC 6:2017 Cl. 206)}} \label{tab:footway-load} \\
\hline
\textbf{Parameter} & \textbf{Design Specification} \\[4pt]
\hline
\endfirsthead
\caption[]{\textbf{Footway / Footpath Live Load} \textit{(Continued)}} \\
\hline
\textbf{Parameter} & \textbf{Design Specification} \\[4pt]
\hline
\endhead
\hline
\multicolumn{2}{|r|}{\textit{\small Continued on next page...}} \\
\hline
\endfoot
\hline
\endlastfoot
\textnormal{Footpath Provision} & """ + fp_status_str + r""" \\[5pt]
\hline
\textnormal{Design Mode} & """ + fp_mode + r""" \\[5pt]
\hline
\textnormal{Standard Reference Clause} & """ + fp_clause_str + r""" \\[5pt]
\hline
\textnormal{Applied Live Load Intensity} & """ + fp_intensity_str + r""" \\[5pt]
\hline
\textnormal{Total Footway Design Live Load} & """ + fp_total_load_str + r""" \\[5pt]
\hline
\end{longtable}

\vspace{0.8em}
\begin{longtable}{|L{6.0cm}|p{9.5cm}|}
\caption{\textbf{Wind Load (WL) --- per IRC 6:2017}} \label{tab:wind-load} \\
\hline
\textbf{Parameter} & \textbf{Design Value} \\[4pt]
\hline
\endfirsthead
\caption[]{\textbf{Wind Load (WL)} \textit{(Continued)}} \\
\hline
\textbf{Parameter} & \textbf{Design Value} \\[4pt]
\hline
\endhead
\hline
\multicolumn{2}{|r|}{\textit{\small Continued on next page...}} \\
\hline
\endfoot
\hline
\endlastfoot
\textnormal{Basic Wind Speed, $V_b$} & """ + (_render_value(input_dict, 'wind_speed', ' m/s')) + r""" [Project Location] \\[5pt]
\hline
\textnormal{Terrain Type} & """ + (_render_value(input_dict, KEY_WL_TERRAIN_TYPE)) + r""" \\[5pt]
\hline
\textnormal{Average Exposed Height, $H$} & """ + (_render_value(input_dict, KEY_WL_AVG_EXPOSED_HEIGHT, ' m')) + r""" \\[5pt]
\hline
\textnormal{Hourly Mean Wind Speed, $V_z$} & """ + vz_str + r""" \\[5pt]
\hline
\textnormal{Hourly Wind Pressure, $P_z$} & """ + pz_str + r""" \\[5pt]
\hline
\textnormal{Transverse Wind Force} & """ + (_render_value(input_dict, KEY_WL_TRANSVERSE_WIND_FORCE, ' kN')) + r""" \\[5pt]
\hline
\textnormal{Longitudinal Wind Force} & """ + (_render_value(input_dict, KEY_WL_LONGITUDINAL_WIND_FORCE, ' kN')) + r""" \\[5pt]
\hline
\textnormal{Vertical Wind Force} & """ + (_render_value(input_dict, KEY_WL_VERTICAL_WIND_FORCE, ' kN')) + r""" \\[5pt]
\hline
\end{longtable}

\vspace{0.8em}
\begin{longtable}{|L{6.0cm}|p{9.5cm}|}
\caption{\textbf{Earthquake Load (EL) --- per IRC 6:2017 Cl. 218}} \label{tab:seismic-load} \\
\hline
\textbf{Parameter} & \textbf{Design Value} \\[4pt]
\hline
\endfirsthead
\caption[]{\textbf{Earthquake Load (EL)} \textit{(Continued)}} \\
\hline
\textbf{Parameter} & \textbf{Design Value} \\[4pt]
\hline
\endhead
\hline
\multicolumn{2}{|r|}{\textit{\small Continued on next page...}} \\
\hline
\endfoot
\hline
\endlastfoot
\textnormal{Seismic Zone} & """ + (_render_value(input_dict, 'seismic_zone')) + r""" \\[5pt]
\hline
\textnormal{Zone Factor, $Z$} & """ + (_render_value(input_dict, KEY_SL_ZONE_FACTOR)) + r""" \\[5pt]
\hline
\textnormal{Importance Factor, $I$} & """ + (_render_value(input_dict, KEY_SL_IMPORTANCE_FACTOR)) + r""" \\[5pt]
\hline
\textnormal{Soil Sub-grade Type} & """ + (_render_value(input_dict, KEY_SL_SOIL_TYPE)) + r""" \\[5pt]
\hline
\textnormal{Spectral Amplification, $S_a/g$} & """ + (_render_value(input_dict, KEY_SL_SPECTRAL_COEFF)) + r""" \\[5pt]
\hline
\textnormal{Horizontal Seismic Coefficient, $A_h$} & """ + (_render_value(input_dict, KEY_SL_HORIZONTAL_COEFF)) + r""" \\[5pt]
\hline
\textnormal{Vertical Seismic Coefficient, $A_v$} & """ + (_render_value(input_dict, KEY_SL_VERTICAL_COEFF)) + r""" \\[5pt]
\hline
\end{longtable}

\vspace{0.8em}
\begin{longtable}{|L{6.0cm}|p{9.5cm}|}
\caption{\textbf{Thermal Load (TL) --- per IRC 6:2017 Cl. 215}} \label{tab:temp-load} \\
\hline
\textbf{Parameter} & \textbf{Design Value} \\[4pt]
\hline
\endfirsthead
\caption[]{\textbf{Thermal Load (TL)} \textit{(Continued)}} \\
\hline
\textbf{Parameter} & \textbf{Design Value} \\[4pt]
\hline
\endhead
\hline
\multicolumn{2}{|r|}{\textit{\small Continued on next page...}} \\
\hline
\endfoot
\hline
\endlastfoot
\textnormal{Maximum Shade Temperature} & """ + (_render_value(input_dict, 'shade_temp_max', r' $^\circ$C')) + r""" \\[5pt]
\hline
\textnormal{Minimum Shade Temperature} & """ + (_render_value(input_dict, 'shade_temp_min', r' $^\circ$C')) + r""" \\[5pt]
\hline
\textnormal{Effective Bridge Temp. Range} & """ + tl_temp_min + r""" to """ + tl_temp_max + r""" $^\circ$C \\[5pt]
\hline
\textnormal{Design Temperature Rise / Fall} & +""" + tl_rise + r""" $^\circ$C / \textminus{}""" + tl_fall + r""" $^\circ$C \\[5pt]
\hline
\end{longtable}

\vspace{0.8em}
\begin{longtable}{|C{3.5cm}|p{12.0cm}|}
\caption{\textbf{Load Combinations Evaluated (ULS \& SLS)}} \label{tab:combos} \\
\hline
\textbf{Combination ID} & \textbf{Governing Load Expression} \\[4pt]
\hline
\endfirsthead
\caption[]{\textbf{Load Combinations Evaluated} \textit{(Continued)}} \\
\hline
\textbf{Combination ID} & \textbf{Governing Load Expression} \\[4pt]
\hline
\endhead
\hline
\multicolumn{2}{|r|}{\textit{\small Continued on next page...}} \\
\hline
\endfoot
\hline
\endlastfoot
""" + lc_rows_str + r"""
\end{longtable}
\noindent\textit{Note: Standard load combinations are generated in accordance with IRC 6:2017 Annexure B Table B.1 (ULS) and Table B.2 (SLS).}
"""
