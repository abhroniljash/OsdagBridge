"""Chapter 7 — Material Take-off & Quantity Summary.

Includes:
- Repeated table headers across page breaks (\\endfirsthead, \\endhead, \\endfoot, \\endlastfoot)
- Bill of Materials (BOM) for steel, concrete, rebar, studs, barriers
- Programmatic bar charts for Structural Steel Tonnage breakdown and Concrete Volume vs. Rebar Weight
"""
from __future__ import annotations
import os
from typing import Optional, Dict


def ch7_quantities(input_dict: dict, fig_paths: Optional[Dict[str, str]] = None) -> str:
    """Generate Chapter 7: Material Take-off & Quantity Summary LaTeX source."""
    fig_paths = fig_paths or {}

    # Check for pre-generated charts or paths
    steel_chart = fig_paths.get("material_steel_tonnage") or fig_paths.get("steel_tonnage")
    concrete_chart = fig_paths.get("material_concrete_rebar") or fig_paths.get("concrete_rebar")

    fig_block = ""
    if steel_chart and concrete_chart:
        fig_block = r"""
\vspace{1.5em}
\section{Material Quantity Visualizations}
\label{sec:material-visualizations}
The figures below present graphical summaries of the quantified material take-off for the bridge superstructure. Figure~\ref{fig:steel-tonnage} depicts the tonnage breakdown across the primary structural steel components, while Figure~\ref{fig:concrete-rebar} compares the concrete deck volume against the total reinforcement steel weight.

\begin{figure}[H]
\centering
\begin{subfigure}[b]{0.48\textwidth}
  \centering
  \includegraphics[width=\linewidth]{""" + steel_chart.replace('\\', '/') + r"""}
  \caption{Structural Steel Tonnage by Component}
  \label{fig:steel-tonnage}
\end{subfigure}
\hfill
\begin{subfigure}[b]{0.48\textwidth}
  \centering
  \includegraphics[width=\linewidth]{""" + concrete_chart.replace('\\', '/') + r"""}
  \caption{Concrete Volume vs. Rebar Weight}
  \label{fig:concrete-rebar}
\end{subfigure}
\caption{\textbf{Superstructure Material Take-Off and Weight Distribution}}
\label{fig:material-takeoff-summary}
\end{figure}
"""

    return r"""
\chapter{Material Take-off \& Quantity Summary}
\label{ch:material-takeoff}

This chapter details the structural material quantities estimated for the bridge superstructure based on the final design geometry and component selections. Quantities include structural steel plate girders, bracing systems, concrete deck slab, reinforcement bars, and shear stud connectors.

\vspace{0.8em}
\begingroup
\setlength{\tabcolsep}{3.5pt}
\begin{longtable}{|C{1.0cm}|L{3.8cm}|C{2.6cm}|C{1.8cm}|C{1.8cm}|C{1.8cm}|C{1.8cm}|}
\caption{\textbf{Bill of Materials (Steel, Concrete, and Reinforcement Quantities)}}\label{tab:bom} \\
\hline
\textbf{S.N.} & \textbf{Item Description} & \textbf{Volume} & \textbf{Quantity} & \textbf{Total Volume} & \textbf{Weight (MT)} & \textbf{Total Weight (MT)} \\[6pt]
\hline
\endfirsthead

\caption[]{\textbf{Bill of Materials (Steel, Concrete, and Reinforcement Quantities)} \textit{(Continued from previous page)}} \\
\hline
\textbf{S.N.} & \textbf{Item Description} & \textbf{Volume} & \textbf{Quantity} & \textbf{Total Volume} & \textbf{Weight (MT)} & \textbf{Total Weight (MT)} \\[6pt]
\hline
\endhead

\hline
\multicolumn{7}{r}{\textit{\footnotesize Continued on next page...}} \\
\endfoot

\hline
\endlastfoot

1 & Structural Steel (IS 2062) for Girders & """ + str(input_dict.get("steel_girders_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("steel_girders_qty", "N.A.")) + r""" & """ + str(input_dict.get("steel_girders_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("steel_girders_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("steel_girders_wt_total", "N.A.")) + r""" \\[6pt]
\hline
2(a) & Cross Bracing - Top Chord & """ + str(input_dict.get("bracing_top_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("bracing_top_qty", "N.A.")) + r""" & """ + str(input_dict.get("bracing_top_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("bracing_top_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("bracing_top_wt_total", "N.A.")) + r""" \\[6pt]
\hline
2(b) & Cross Bracing - Bottom Chord & """ + str(input_dict.get("bracing_bot_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("bracing_bot_qty", "N.A.")) + r""" & """ + str(input_dict.get("bracing_bot_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("bracing_bot_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("bracing_bot_wt_total", "N.A.")) + r""" \\[6pt]
\hline
2(c) & Cross Bracing - Diagonal Chord & """ + str(input_dict.get("bracing_diag_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("bracing_diag_qty", "N.A.")) + r""" & """ + str(input_dict.get("bracing_diag_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("bracing_diag_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("bracing_diag_wt_total", "N.A.")) + r""" \\[6pt]
\hline
3 & Concrete (M40) for Deck Slab & """ + str(input_dict.get("concrete_deck_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("concrete_deck_qty", "N.A.")) + r""" & """ + str(input_dict.get("concrete_deck_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("concrete_deck_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("concrete_deck_wt_total", "N.A.")) + r""" \\[6pt]
\hline
4 & Reinforcement Steel (Fe 500) & """ + str(input_dict.get("rebar_deck_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("rebar_deck_qty", "N.A.")) + r""" & """ + str(input_dict.get("rebar_deck_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("rebar_deck_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("rebar_deck_wt_total", "N.A.")) + r""" \\[6pt]
\hline
5 & Shear Stud Connectors & """ + str(input_dict.get("shear_studs_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("shear_studs_qty", "N.A.")) + r""" & """ + str(input_dict.get("shear_studs_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("shear_studs_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("shear_studs_wt_total", "N.A.")) + r""" \\[6pt]
\hline
6 & Crash Barrier & """ + str(input_dict.get("crash_barrier_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("crash_barrier_qty", "N.A.")) + r""" & """ + str(input_dict.get("crash_barrier_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("crash_barrier_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("crash_barrier_wt_total", "N.A.")) + r""" \\[6pt]
\hline
\end{longtable}
\endgroup
""" + fig_block
