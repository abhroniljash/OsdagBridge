import sys, os, subprocess, shutil

workspace_root = r'D:\IIT Boumby'
src_path = os.path.join(workspace_root, 'OsdagBridge-dev', 'src')
sys.path.insert(0, src_path)

from osdagbridge.core.bridge_types.plate_girder.defaults import BASIC_INPUT_DICT, solve_extend_basic_input_dict
from osdagbridge.core.utils.common import *
from osdagbridge.core.reports.report_generator import build_report_payload, generate_report, ReportRequest, ReportMetadata, ReportOptions

inputs = dict(BASIC_INPUT_DICT)
inputs[KEY_SPAN] = 30.0
inputs[KEY_CARRIAGEWAY_WIDTH] = 7.5
inputs[KEY_TS_NO_OF_GIRDERS] = 4
inputs[KEY_TS_GIRDER_SPACING] = 2.1
inputs[KEY_TS_DECK_OVERHANG] = 1.05
inputs[KEY_TS_DECK_THICKNESS] = 250.0
inputs[KEY_TS_NO_OF_FOOTPATHS] = 0
inputs[KEY_TS_FOOTPATH_WIDTH] = 0.0
inputs[KEY_INCLUDE_MEDIAN] = 'No'
inputs[KEY_DESIGN_MODE] = 'Optimized'
inputs[KEY_GIRDER] = 'E 350A'

solve_extend_basic_input_dict(inputs)

meta = ReportMetadata(
    project_name='Short-Span Steel Plate Girder Bridge',
    project_location='Mumbai, Maharashtra',
    designer='OsdagBridge Design Team',
    client='Ministry of Road Transport and Highways',
    company='Indian Institute of Technology Bombay',
    job_number='OSDAG-BR-2026-01',
    report_date='November 20, 2026'
)
opts = ReportOptions(
    sections=['loads', 'analysis', 'design_checks', 'drawings'],
    include_figures=True,
    include_toc=True,
    include_pdf=True
)
out_dir = os.path.join(workspace_root, 'deliverables')
os.makedirs(out_dir, exist_ok=True)
os.makedirs(os.path.join(out_dir, 'assets'), exist_ok=True)

logo_src = os.path.join(src_path, 'osdagbridge', 'core', 'data', 'ResourceFiles', 'vectors', 'Osdag Logo.png')
if os.path.exists(logo_src):
    shutil.copy2(logo_src, os.path.join(out_dir, 'assets', 'osdag_logo.png'))

req = ReportRequest(
    metadata=meta,
    options=opts,
    output_dir=out_dir,
    file_stem='Report_Before'
)

# Realistic output_dict
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

payload = build_report_payload(req, inputs, output_dict)
res = generate_report(payload, req)
print('Generate report executed. tex_path:', res.tex_path)

tex_file = os.path.join(out_dir, 'Report_Before.tex')
pdf_file = os.path.join(out_dir, 'Report_Before.pdf')

with open(tex_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_longtable = False
for line in lines:
    if r'\begin{longtable}' in line:
        in_longtable = True
    elif r'\end{longtable}' in line:
        in_longtable = False
    
    if in_longtable and r'\caption{' in line and not line.strip().endswith(r'\\'):
        line = line.rstrip() + r' \\' + '\n'
    new_lines.append(line)

with open(tex_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Updated longtable captions with \\\\ for baseline compilation.')
tectonic_exe = os.path.join(workspace_root, 'tectonic_bin', 'tectonic.exe')
c_res = subprocess.run([tectonic_exe, tex_file, '--outdir', out_dir], capture_output=True, text=True, cwd=out_dir)
print('Tectonic exit code:', c_res.returncode)
if c_res.returncode != 0:
    print('STDOUT:', c_res.stdout[:500])
    print('STDERR:', c_res.stderr[-1000:])
else:
    print('SUCCESS! Report_Before.pdf compiled! Size:', os.path.getsize(pdf_file), 'bytes')
