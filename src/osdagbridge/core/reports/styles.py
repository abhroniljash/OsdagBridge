"""
Centralized Styling & Theming System for OsdagBridge LaTeX Report Generation.
Single Source of Truth (SSOT) for colors, page geometry, typography, table layouts,
header/footer styling, and programmatic Matplotlib visualization theming.
"""

from __future__ import annotations
import os
from typing import List, Optional, Tuple, Dict, Any

# =============================================================================
# 1. COLOR PALETTE DEFINITIONS (Single Source of Truth)
# =============================================================================

# Primary Brand & Accent Colors
COLOR_OSDAG_GREEN = "#91B014"       # Official Osdag Green
COLOR_DARK_SLATE  = "#2C3E50"       # Deep Slate for titles and headings
COLOR_TEXT_MAIN   = "#2C3E50"       # Charcoal text color
COLOR_PASS        = "#27AE60"       # Emerald Green for passing checks (UR <= 1.0)
COLOR_FAIL        = "#C0392B"       # Strong Red for failing checks (UR > 1.0)
COLOR_WARNING     = "#F39C12"       # Amber for warnings / borderline
COLOR_INFO        = "#2980B9"       # Muted Blue for secondary annotations

# Table Neutral & Surface Colors
COLOR_TABLE_HEADER_BG = "#EAECEE"   # Soft grey-blue for table headers
COLOR_TABLE_ALT_BG    = "#F8F9FA"   # Very subtle grey for alternating rows
COLOR_TABLE_RULE      = "#BDC3C7"   # Clean border rules

# Matplotlib Chart Color Palette
CHART_BAR_PRIMARY   = "#2980B9"     # Blue for steel / general demands
CHART_BAR_SECONDARY = "#91B014"     # Osdag Green
CHART_BAR_CONCRETE  = "#7F8C8D"     # Concrete grey
CHART_BAR_REBAR     = "#D35400"     # Steel rebar rust/orange
CHART_THRESHOLD     = "#E74C3C"     # Bright red dashed threshold (UR = 1.0)
CHART_BG            = "#FFFFFF"
CHART_GRID          = "#E0E0E0"

# LaTeX Color Definitions Block
LATEX_COLOR_DEFINITIONS = r"""
\definecolor{osdagGreen}{HTML}{91B014}
\definecolor{osdagDark}{HTML}{2C3E50}
\definecolor{tableHeaderBg}{HTML}{EAECEE}
\definecolor{tableAltBg}{HTML}{F8F9FA}
\definecolor{passGreen}{HTML}{27AE60}
\definecolor{failRed}{HTML}{C0392B}
\definecolor{chartThreshold}{HTML}{E74C3C}
"""

# =============================================================================
# 2. PAGE GEOMETRY & LAYOUT CONFIGURATION
# =============================================================================

GEOMETRY_CONFIG = {
    "paper": "a4paper",
    "top": "25mm",
    "bottom": "28mm",      # Increased from default 1in to eliminate footer overlap
    "left": "20mm",
    "right": "20mm",
    "headheight": "20pt",   # Sized to fit 2-line header without fancyhdr warning
    "headsep": "12pt",
    "footskip": "16pt",     # Dedicated space to guarantee zero table/text bleed
}

def get_geometry_latex() -> str:
    """Return the LaTeX \\usepackage{geometry} directive with calibrated metrics."""
    return (
        r"\usepackage[a4paper, "
        f"top={GEOMETRY_CONFIG['top']}, "
        f"bottom={GEOMETRY_CONFIG['bottom']}, "
        f"left={GEOMETRY_CONFIG['left']}, "
        f"right={GEOMETRY_CONFIG['right']}, "
        f"headheight={GEOMETRY_CONFIG['headheight']}, "
        f"headsep={GEOMETRY_CONFIG['headsep']}, "
        f"footskip={GEOMETRY_CONFIG['footskip']}]{{geometry}}"
    )

# =============================================================================
# 3. TYPOGRAPHY & TABLE SPACING RULES
# =============================================================================

TYPOGRAPHY_CONFIG = {
    "base_font_size": "12pt",
    "line_stretch": "1.15",
    "tabcolsep": "6pt",            # Horizontal cell padding
    "arraystretch": "1.15",         # Vertical row height factor
    "arrayrulewidth": "0.5pt",      # Table border rule width
    "extrarowheight": "0.8pt",      # Clean top-padding in cells
    "LTpre": "2pt",                 # Longtable space before
    "LTpost": "6pt",                # Longtable space after
    "needspace_table": r"\needspace{6\baselineskip}", # Prevent bottom-bleed / orphan rows
}

def get_spacing_preamble_latex() -> str:
    """Return LaTeX configuration block for document spacing and table padding."""
    return f"""
% Typography and Spacing Configuration (SSOT via styles.py)
\\setstretch{{{TYPOGRAPHY_CONFIG['line_stretch']}}}
\\setlength{{\\tabcolsep}}{{{TYPOGRAPHY_CONFIG['tabcolsep']}}}
\\renewcommand{{\\arraystretch}}{{{TYPOGRAPHY_CONFIG['arraystretch']}}}
\\setlength{{\\arrayrulewidth}}{{{TYPOGRAPHY_CONFIG['arrayrulewidth']}}}
\\setlength{{\\extrarowheight}}{{{TYPOGRAPHY_CONFIG['extrarowheight']}}}
\\setlength{{\\LTpre}}{{{TYPOGRAPHY_CONFIG['LTpre']}}}
\\setlength{{\\LTpost}}{{{TYPOGRAPHY_CONFIG['LTpost']}}}

% Bottom clearance buffer: prevent tables and sections from overflowing into footer
\\BeforeBeginEnvironment{{table}}{{{TYPOGRAPHY_CONFIG['needspace_table']}}}
\\BeforeBeginEnvironment{{longtable}}{{{TYPOGRAPHY_CONFIG['needspace_table']}}}
"""

# =============================================================================
# 4. HEADER & FOOTER THEME (Eliminating Overlap & Warnings)
# =============================================================================

def get_fancyhdr_latex(project_name: str, job_number: str, report_date: str, report_version: str = "Rev 0") -> str:
    """Return calibrated fancyhdr pagestyles guaranteeing clean header/footer clearance."""
    pn = project_name
    jn = job_number
    rd = report_date
    rv = report_version
    return f"""
% Header and Footer Styling (Centralized Theme)
\\fancypagestyle{{main}}{{
  \\fancyhf{{}}
  \\fancyhead[L]{{\\small\\textbf{{{pn}}} $|$ {jn}}}
  \\fancyhead[R]{{\\small {rd} $|$ {rv}}}
  \\fancyfoot[L]{{\\footnotesize Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}
  \\fancyfoot[R]{{\\footnotesize Page \\thepage\\ of \\pageref{{LastPage}}}}
  \\renewcommand{{\\headrule}}{{\\color{{osdagGreen}}\\hrule width\\headwidth height 1pt \\vspace{{2pt}}}}
  \\renewcommand{{\\footrule}}{{%
    \\ifbool{{hasSDonPage}}{{%
      \\vspace{{-12pt}}%
      \\hbox to \\headwidth{{\\textcolor{{black}}{{\\footnotesize\\textit{{* Software default value}}}}\\hfil}}%
      \\vspace{{3pt}}%
    }}{{%
      \\vspace{{0pt}}%
    }}%
    \\color{{osdagGreen}}\\hrule width\\headwidth height 1pt \\vspace{{4pt}}%
  }}
}}

\\fancypagestyle{{plain}}{{
  \\fancyhf{{}}
  \\fancyhead[L]{{\\small\\textbf{{{pn}}} $|$ {jn}}}
  \\fancyhead[R]{{\\small {rd} $|$ {rv}}}
  \\fancyfoot[L]{{\\footnotesize Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}
  \\fancyfoot[R]{{\\footnotesize Page \\thepage\\ of \\pageref{{LastPage}}}}
  \\renewcommand{{\\headrule}}{{\\color{{osdagGreen}}\\hrule width\\headwidth height 1pt \\vspace{{2pt}}}}
  \\renewcommand{{\\footrule}}{{%
    \\ifbool{{hasSDonPage}}{{%
      \\vspace{{-12pt}}%
      \\hbox to \\headwidth{{\\textcolor{{black}}{{\\footnotesize\\textit{{* Software default value}}}}\\hfil}}%
      \\vspace{{3pt}}%
    }}{{%
      \\vspace{{0pt}}%
    }}%
    \\color{{osdagGreen}}\\hrule width\\headwidth height 1pt \\vspace{{4pt}}%
  }}
}}

\\fancypagestyle{{firstpage}}{{
  \\fancyhf{{}}
  \\renewcommand{{\\headrulewidth}}{{0pt}}
  \\fancyfoot[L]{{\\footnotesize Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}
  \\fancyfoot[R]{{\\footnotesize Page \\thepage\\ of \\pageref{{LastPage}}}}
  \\renewcommand{{\\footrule}}{{\\color{{osdagGreen}}\\hrule width\\headwidth height 1pt \\vspace{{4pt}}}}
}}
"""

# =============================================================================
# 5. DYNAMIC LONGTABLE BUILDER (Auto-Repeated Headers Across Page Breaks)
# =============================================================================

def build_longtable_header(
    col_spec: str,
    caption: str,
    header_rows: List[str],
    label: Optional[str] = None,
    continuation_note: str = "(Continued from previous page)",
    include_rowcolor: bool = True
) -> str:
    """
    Constructs a robust, compliant LaTeX LongTable header with:
      - First page caption and headers (\\endfirsthead)
      - Repeated headers on subsequent pages (\\endhead)
      - Bottom transition rule with 'Continued on next page...' (\\endfoot)
      - Final bottom rule (\\endlastfoot)
    """
    label_str = f"\\label{{{label}}}" if label else ""
    cap_line = f"\\caption{{\\textbf{{{caption}}}}}{label_str} \\\\\n\\hline"
    cont_cap_line = f"\\caption[]{{\\textbf{{{caption}}} \\textit{{{continuation_note}}}}} \\\\\n\\hline"

    header_block = "\n".join(header_rows) + r" \\[6pt]" + "\n\\hline"

    return f"""\\begin{{longtable}}{{{col_spec}}}
{cap_line}
{header_block}
\\endfirsthead

{cont_cap_line}
{header_block}
\\endhead

\\hline
\\multicolumn{{{col_spec.count('|') - 1 or 2}}}{{r}}{{\\textit{{\\footnotesize Continued on next page...}}}} \\\\
\\endfoot

\\hline
\\endlastfoot
"""

# =============================================================================
# 6. PROGRAMMATIC DATA VISUALIZATIONS (Matplotlib Engine)
# =============================================================================

def configure_matplotlib_style():
    """Apply unified publication-quality styling to Matplotlib plots."""
    try:
        import os, tempfile
        os.environ.setdefault('MPLCONFIGDIR', tempfile.gettempdir())
        import matplotlib as mpl
        import matplotlib.pyplot as plt

        mpl.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Helvetica', 'Arial']
        mpl.rcParams['font.family'] = 'sans-serif'
        mpl.rcParams['axes.edgecolor'] = COLOR_DARK_SLATE
        mpl.rcParams['axes.linewidth'] = 0.8
        mpl.rcParams['axes.titlesize'] = 11
        mpl.rcParams['axes.labelsize'] = 9.5
        mpl.rcParams['xtick.labelsize'] = 8.5
        mpl.rcParams['ytick.labelsize'] = 8.5
        mpl.rcParams['grid.color'] = CHART_GRID
        mpl.rcParams['grid.linestyle'] = '--'
        mpl.rcParams['grid.linewidth'] = 0.6
        mpl.rcParams['grid.alpha'] = 0.7
        mpl.rcParams['figure.autolayout'] = True
    except Exception:
        pass


def generate_ur_summary_charts(
    girder_checks: List[Tuple[str, float]],
    deck_checks: List[Tuple[str, float]],
    cross_bracing_checks: List[Tuple[str, float]],
    end_diaphragm_checks: List[Tuple[str, float]],
    output_dir: str,
    file_stem: str = "ur_summary"
) -> Dict[str, str]:
    """
    Programmatically generate high-resolution bar charts of Utilization Ratios (UR)
    for all primary structural bridge elements with an explicit red dashed threshold line at UR=1.0.
    
    Returns a dict mapping chart keys to absolute image file paths.
    """
    configure_matplotlib_style()
    import matplotlib.pyplot as plt
    import numpy as np

    os.makedirs(output_dir, exist_ok=True)
    generated_paths = {}

    components = [
        ("Steel Plate Girders", girder_checks, f"{file_stem}_girders.png"),
        ("Concrete Deck Slab", deck_checks, f"{file_stem}_deck.png"),
        ("Cross Bracing Members", cross_bracing_checks, f"{file_stem}_bracing.png"),
        ("End Diaphragm Members", end_diaphragm_checks, f"{file_stem}_diaphragms.png"),
    ]

    for title, items, fname in components:
        if not items:
            continue
        labels = [item[0] for item in items]
        values = [max(0.0, float(item[1])) for item in items]

        fig, ax = plt.subplots(figsize=(6.8, 3.2), dpi=300)
        x = np.arange(len(labels))
        colors = [COLOR_PASS if v <= 1.0 else COLOR_FAIL for v in values]

        bars = ax.bar(x, values, width=0.48, color=colors, edgecolor=COLOR_DARK_SLATE, linewidth=0.7, zorder=3)

        # Threshold Line at UR = 1.0
        ax.axhline(1.0, color=CHART_THRESHOLD, linestyle='--', linewidth=1.4, zorder=4, label='Allowable Threshold (UR = 1.0)')

        # Annotations on top of bars
        max_val = max(values + [1.0])
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f'{height:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=8, fontweight='bold',
                color=COLOR_DARK_SLATE
            )

        ax.set_ylabel('Utilization Ratio (UR = D/C)', fontweight='bold')
        ax.set_title(f'Design Utilization Ratio — {title}', fontweight='bold', pad=10, color=COLOR_DARK_SLATE)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=15, ha='right', fontsize=8.5)
        ax.set_ylim(0, max_val * 1.25)
        ax.grid(axis='y', zorder=0)
        ax.legend(loc='upper right', framealpha=0.9, fontsize=8)

        # Subtle colored status watermark or border
        ax.set_facecolor('#FAFAFA')

        img_path = os.path.join(output_dir, fname)
        plt.tight_layout()
        plt.savefig(img_path, dpi=300, facecolor='white', bbox_inches='tight')
        plt.close(fig)

        key = fname.replace('.png', '')
        generated_paths[key] = img_path.replace('\\', '/')

    return generated_paths


def generate_material_takeoff_charts(
    steel_quantities: Dict[str, float],
    concrete_rebar_quantities: Dict[str, float],
    output_dir: str,
    file_stem: str = "material_takeoff"
) -> Dict[str, str]:
    """
    Programmatically generate publication-quality bar charts summarizing:
      1. Structural Steel tonnage breakdown (Girders, Cross Bracing, End Diaphragms)
      2. Concrete volume (m³) vs. Reinforcement Steel weight (MT)
      
    Returns a dict mapping chart keys to absolute image file paths.
    """
    configure_matplotlib_style()
    import matplotlib.pyplot as plt
    import numpy as np

    os.makedirs(output_dir, exist_ok=True)
    generated_paths = {}

    # 1. Structural Steel Tonnage Breakdown
    if steel_quantities:
        labels = list(steel_quantities.keys())
        values = list(steel_quantities.values())

        fig, ax = plt.subplots(figsize=(6.4, 3.0), dpi=300)
        x = np.arange(len(labels))
        bars = ax.bar(x, values, width=0.45, color=['#2980B9', '#27AE60', '#E67E22'][:len(labels)],
                      edgecolor=COLOR_DARK_SLATE, linewidth=0.7, zorder=3)

        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f'{height:.2f} MT',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=8.5, fontweight='bold',
                color=COLOR_DARK_SLATE
            )

        ax.set_ylabel('Weight (Metric Tonnes)', fontweight='bold')
        ax.set_title('Structural Steel Tonnage Breakdown by Component', fontweight='bold', pad=10, color=COLOR_DARK_SLATE)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=9)
        max_v = max(values) if values else 1.0
        ax.set_ylim(0, max_v * 1.25)
        ax.grid(axis='y', zorder=0)
        ax.set_facecolor('#FAFAFA')

        fname1 = f"{file_stem}_steel_tonnage.png"
        path1 = os.path.join(output_dir, fname1)
        plt.tight_layout()
        plt.savefig(path1, dpi=300, facecolor='white', bbox_inches='tight')
        plt.close(fig)
        generated_paths["steel_tonnage"] = path1.replace('\\', '/')

    # 2. Concrete Volume vs Reinforcement Steel Weight (Dual scale / comparison)
    if concrete_rebar_quantities:
        conc_vol = concrete_rebar_quantities.get("concrete_volume_m3", 0.0)
        rebar_wt = concrete_rebar_quantities.get("rebar_weight_mt", 0.0)

        fig, ax1 = plt.subplots(figsize=(6.0, 3.0), dpi=300)
        categories = ['Concrete Deck (Volume)', 'Reinforcement Steel (Weight)']
        y_vals = [conc_vol, rebar_wt]
        colors = [CHART_BAR_CONCRETE, CHART_BAR_REBAR]

        bars = ax1.bar([0, 1], y_vals, width=0.45, color=colors, edgecolor=COLOR_DARK_SLATE, linewidth=0.7, zorder=3)

        units = ["m³", "MT"]
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax1.annotate(
                f'{height:.2f} {units[i]}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=8.5, fontweight='bold',
                color=COLOR_DARK_SLATE
            )

        ax1.set_ylabel('Magnitude (m³ for Concrete / MT for Rebar)', fontweight='bold')
        ax1.set_title('Concrete Volume vs. Reinforcement Steel Weight', fontweight='bold', pad=10, color=COLOR_DARK_SLATE)
        ax1.set_xticks([0, 1])
        ax1.set_xticklabels(categories, fontsize=9)
        max_y = max(y_vals) if y_vals else 1.0
        ax1.set_ylim(0, max_y * 1.25)
        ax1.grid(axis='y', zorder=0)
        ax1.set_facecolor('#FAFAFA')

        fname2 = f"{file_stem}_concrete_rebar.png"
        path2 = os.path.join(output_dir, fname2)
        plt.tight_layout()
        plt.savefig(path2, dpi=300, facecolor='white', bbox_inches='tight')
        plt.close(fig)
        generated_paths["concrete_rebar"] = path2.replace('\\', '/')

    return generated_paths
