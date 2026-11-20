import os
import sys
import shutil
import subprocess

workspace_root = r"D:\IIT Boumby"
src_path = os.path.join(workspace_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from osdagbridge.core.reports.report_generator import (
    ReportPayload,
    ReportRequest,
    ReportMetadata,
    ReportOptions,
    build_report_payload,
    generate_report
)
from osdagbridge.core.utils.common import (
    KEY_SPAN,
    KEY_CARRIAGEWAY_WIDTH,
    KEY_TS_NO_OF_GIRDERS,
    KEY_TS_GIRDER_SPACING,
    KEY_TS_DECK_OVERHANG,
    KEY_TS_DECK_THICKNESS,
    KEY_DESIGN_MODE,
    KEY_DD_M_ULS_SAG,
    KEY_DD_MU_BOT,
    KEY_DD_M_ULS_HOG,
    KEY_DD_MU_TOP,
    KEY_DD_M_ULS_OH,
    KEY_DD_MU_OH,
    KEY_DD_SHEAR_VED,
    KEY_DD_SHEAR_VRDC,
    KEY_DD_PUNCH_VED,
    KEY_DD_VRD_C_MPA,
    KEY_DD_GAMMA_DL,
    KEY_DD_GAMMA_LL,
    KEY_DD_WK_OH,
    KEY_DD_WK_LIMIT,
)

out_dir = os.path.join(workspace_root, 'deliverables')
os.makedirs(out_dir, exist_ok=True)
os.makedirs(os.path.join(out_dir, 'assets'), exist_ok=True)

logo_src = os.path.join(src_path, 'osdagbridge', 'core', 'data', 'ResourceFiles', 'vectors', 'Osdag Logo.png')
if os.path.exists(logo_src):
    shutil.copy2(logo_src, os.path.join(out_dir, 'assets', 'osdag_logo.png'))

meta = ReportMetadata(
    project_name="Bridge Over Kali River (NH-66)",
    project_location="Karwar, Karnataka, India",
    designer="Bridge Engineering Division",
    client="National Highways Authority of India (NHAI)",
    company="FOSSEE / IIT Bombay",
    group_name="Superstructure Design Group",
    subtitle="Enhanced Report — Detailed Verification",
    job_number="NHAI-BR-2026-084",
    additional_comments="Final Design Verification according to IRC 22:2014 & IS 800:2007 with all visual enhancements",
    logo_path=os.path.join(out_dir, 'assets', 'osdag_logo.png'),
    report_date="2026-11-20",
    reviewer="Chief Bridge Consultant"
)

opts = ReportOptions(
    sections=['project_info', 'inputs', 'loads', 'analysis', 'design_checks', 'drawings', 'quantities', 'design_log'],
    include_figures=True,
    include_toc=True,
    include_pdf=True
)

req = ReportRequest(
    metadata=meta,
    options=opts,
    output_dir=out_dir,
    file_stem='Report_After'
)

# Bridge layout and section inputs
inputs = {
    KEY_SPAN: 30.0,
    KEY_CARRIAGEWAY_WIDTH: 7.5,
    KEY_TS_NO_OF_GIRDERS: 4,
    KEY_TS_GIRDER_SPACING: 2.1,
    KEY_TS_DECK_OVERHANG: 1.05,
    KEY_TS_DECK_THICKNESS: 250.0,
    KEY_DESIGN_MODE: "Optimized",
    "typical_section.overall_bridge_width": 8.4,
    "typical_section.girder_spacing": 2100.0,
    "typical_section.deck_overhang": 1050.0,
    "typical_section.deck_thickness": 250.0,
    "typical_section.no_of_girders": 4,
    "typical_section.crash_barrier_width": 450.0,
    "typical_section.wearing_coat_thickness": 75.0,
    "typical_section.footpath_width": 1500.0,
    "typical_section.cross_slope": 2.5,
    "environmental.wind_speed": 44.0,
    "environmental.seismic_zone": "Zone IV",
    "environmental.temperature_range": "10 deg C to 45 deg C",
    "member_properties.girder_details.section_input.web_depth": 1740.0,
    "member_properties.girder_details.section_input.web_thickness": 16.0,
    "member_properties.girder_details.section_input.top_flange_width": 450.0,
    "member_properties.girder_details.section_input.top_flange_thickness": 30.0,
    "member_properties.girder_details.section_input.bottom_flange_width": 450.0,
    "member_properties.girder_details.section_input.bottom_flange_thickness": 30.0,
    "loads.live_load.vehicle_name": "IRC Class 70R Wheeled + IRC Class A",
    "loads.live_load.total_load_kN": 1000.0,
    "loads.live_load.impact_factor": 1.18,
    "loads.live_load.braking_considered": "Yes",
    "loads.live_load.braking_force_kN": 200.0,
    "loads.live_load.braking_eccentricity_m": 1.20,
    "loads.footpath.intensity": 4.0,
    "loads.footpath.width": 1.5,
    "loads.footpath.total_force_kN": 180.0,
}

# Add girder section keys
for i in range(1, 5):
    inputs[f"member_properties.girder_details.section_properties.depth.G{i}.M1"] = 1800.0
    inputs[f"member_properties.girder_details.section_properties.area.G{i}.M1"] = 548.4
    inputs[f"member_properties.girder_details.section_properties.I_z.G{i}.M1"] = 2850000.0
    inputs[f"member_properties.girder_details.section_properties.mass.G{i}.M1"] = 430.5

output_dict = {
    'overall_design_status': 'PASS',
    'governing_check': 'Bending Stress Check (Girder 1)',
    'overall_utilization_ratio': '0.84',
    'section_designation': 'Plate Girder 1800x450x30x16',
    'design_results': {
        'per_girder': {
            f'G{i}': {
                'checks': [
                    {'check_id': 1, 'dcr': 0.82, 'demand': 4200.0, 'capacity': 5120.0, 'demand_unit': 'kNm', 'capacity_unit': 'kNm'},
                    {'check_id': 2, 'dcr': 0.74, 'demand': 850.0, 'capacity': 1150.0, 'demand_unit': 'kN', 'capacity_unit': 'kN'},
                    {'check_id': 5, 'dcr': 0.65, 'demand': 850.0, 'capacity': 1300.0, 'demand_unit': 'kN', 'capacity_unit': 'kN'},
                    {'check_id': 13, 'dcr': 0.58, 'demand': 28.5, 'capacity': 48.0, 'demand_unit': 'mm', 'capacity_unit': 'mm'},
                    {'check_id': 11, 'dcr': 0.79, 'demand': 245.0, 'capacity': 310.0, 'demand_unit': 'MPa', 'capacity_unit': 'MPa'},
                    {'check_id': 8, 'dcr': 0.45, 'demand': 65.0, 'capacity': 145.0, 'demand_unit': 'MPa', 'capacity_unit': 'MPa'},
                    {'check_id': 16, 'dcr': 0.52, 'demand': 120.0, 'capacity': 230.0, 'demand_unit': 'kN', 'capacity_unit': 'kN'},
                ],
                'per_lc': {
                    'SLS-01 (Frequent)': {
                        'max_dcr': 0.58,
                        'checks': [{'id': 13, 'dcr': 0.58, 'demand': 28.5, 'capacity': 48.0}]
                    }
                }
            } for i in range(1, 5)
        }
    },
    'deck_design_results': {
        KEY_DD_M_ULS_SAG: 145.2, KEY_DD_MU_BOT: 210.0,
        KEY_DD_M_ULS_HOG: 112.5, KEY_DD_MU_TOP: 185.0,
        KEY_DD_M_ULS_OH: 65.0, KEY_DD_MU_OH: 120.0,
        KEY_DD_SHEAR_VED: 95.0, KEY_DD_SHEAR_VRDC: 160.0,
        KEY_DD_PUNCH_VED: 1.15, KEY_DD_VRD_C_MPA: 1.85,
        KEY_DD_GAMMA_DL: 1.35, KEY_DD_GAMMA_LL: 1.5,
        KEY_DD_WK_OH: 0.12, KEY_DD_WK_LIMIT: 0.20
    },
    'crossbracing_forces_dict': {
        'pairs': {
            'G1-G2': {'diag_tension_kN': 142.5, 'diag_compression_kN': -165.2, 'chord_tension_kN': 85.0, 'chord_compression_kN': -92.0},
            'G2-G3': {'diag_tension_kN': 130.0, 'diag_compression_kN': -148.0, 'chord_tension_kN': 78.0, 'chord_compression_kN': -84.0},
            'G3-G4': {'diag_tension_kN': 145.0, 'diag_compression_kN': -168.0, 'chord_tension_kN': 86.0, 'chord_compression_kN': -93.0},
        }
    },
    'crossbracing_design_results': {
        p: {
            'diagonal': {
                'tension': {'section': 'ISA 100x100x10', 'capacity_kN': 245.0, 'efficiency': 0.59, 'slenderness': 142.0},
                'compression': {'section': 'ISA 100x100x10', 'capacity_kN': 210.0, 'efficiency': 0.80, 'slenderness': 142.0}
            },
            'chord': {
                'tension': {'section': 'ISA 75x75x8', 'capacity_kN': 180.0, 'efficiency': 0.48, 'slenderness': 118.0},
                'compression': {'section': 'ISA 75x75x8', 'capacity_kN': 155.0, 'efficiency': 0.60, 'slenderness': 118.0}
            }
        } for p in ['G1-G2', 'G2-G3', 'G3-G4']
    }
}

print('Building payload...')
payload = build_report_payload(req, inputs, output_dict)
print('Generating enhanced report...')
res = generate_report(payload, req)
print('Generate report returned. tex_path:', res.tex_path, 'pdf_path:', res.pdf_path)

tex_file = os.path.join(out_dir, 'Report_After.tex')
pdf_file = os.path.join(out_dir, 'Report_After.pdf')

if not os.path.exists(pdf_file) or os.path.getsize(pdf_file) == 0:
    print('Invoking Tectonic compiler directly...')
    tectonic_exe = os.path.join(workspace_root, 'tectonic_bin', 'tectonic.exe')
    c_res = subprocess.run([tectonic_exe, tex_file, '--outdir', out_dir], capture_output=True, text=True, cwd=out_dir)
    print('Tectonic exit code:', c_res.returncode)
    if c_res.returncode != 0:
        print('STDOUT:', c_res.stdout[:500])
        print('STDERR:', c_res.stderr[-1000:])
    else:
        print('SUCCESS! Report_After.pdf compiled via Tectonic! Size:', os.path.getsize(pdf_file), 'bytes')
else:
    print('SUCCESS! Report_After.pdf generated! Size:', os.path.getsize(pdf_file), 'bytes')
