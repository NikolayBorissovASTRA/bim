#!/usr/bin/env python3
"""
Simplified Excel-driven IFC generation with IDS validation using ifctester.
Generates IDS XML files and validates IFC files automatically.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List
import pandas as pd
import ifcopenshell
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ifc_light import IFCLight


def create_test_excel(filepath: str):
    """Create test Excel file with segment models and pyramid coordinates."""

    # Sheet 1: Models - defines which pyramids belong to which segment
    models_data = {
        'segment_model': [
            'SEGMENT_A1', 'SEGMENT_A1', 'SEGMENT_A1',
            'SEGMENT_B2', 'SEGMENT_B2', 'SEGMENT_B2',
            'SEGMENT_C3', 'SEGMENT_C3', 'SEGMENT_C3'
        ],
        'pyramid_name': [
            'PYR_001_REF', 'PYR_002_SUR', 'PYR_003_CTL',  # Segment A1
            'PYR_003_CTL', 'PYR_004_MON', 'PYR_005_BND',  # Segment B2 (shares PYR_003_CTL)
            'PYR_005_BND', 'PYR_006_GEO', 'PYR_007_BEN'   # Segment C3 (shares PYR_005_BND)
        ]
    }

    # Sheet 2: Pyramid Coordinates with metadata
    coordinates_data = {
        'pyramid_name': [
            'PYR_001_REF', 'PYR_002_SUR', 'PYR_003_CTL',
            'PYR_004_MON', 'PYR_005_BND', 'PYR_006_GEO', 'PYR_007_BEN'
        ],
        'LV95_X': [
            2679520.05, 2679525.00, 2679530.00,
            2679535.00, 2679540.00, 2679545.00, 2679550.00
        ],
        'LV95_Y': [
            1151703.09, 1151708.00, 1151713.00,
            1151718.00, 1151723.00, 1151728.00, 1151733.00
        ],
        'LV95_Z': [
            500.0, 501.0, 502.0,
            503.0, 504.0, 505.0, 506.0
        ],
        'measurement_date': [
            '2024-01-15', '2024-01-15', '2024-01-16',
            '2024-01-17', '2024-01-17', '2024-01-18', '2024-01-18'
        ],
        'accuracy_class': [
            'I', 'II', 'I',
            'II', 'III', 'I', 'II'
        ],
        'measurement_method': [
            'GNSS_RTK', 'GNSS_RTK', 'Total_Station',
            'GNSS_Static', 'GNSS_RTK', 'Total_Station', 'GNSS_Static'
        ],
        'operator': [
            'Team_A', 'Team_A', 'Team_B',
            'Team_A', 'Team_C', 'Team_B', 'Team_C'
        ],
        'status': [
            'Verified', 'Verified', 'Verified',
            'Preliminary', 'Verified', 'Final', 'Preliminary'
        ],
        'remarks': [
            'Reference point for sector A1',
            'Surface survey point',
            'Control point shared between segments',
            'Monitoring point for deformation',
            'Boundary marker shared point',
            'Geodetic reference marker',
            'Benchmark for elevation'
        ]
    }

    # Create Excel file
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        pd.DataFrame(models_data).to_excel(writer, sheet_name='models', index=False)
        pd.DataFrame(coordinates_data).to_excel(writer, sheet_name='pyramid-coordinates', index=False)

    print(f"✅ Created test Excel file: {filepath}")
    return models_data, coordinates_data


def generate_ifc_files(models_df: pd.DataFrame, coords_df: pd.DataFrame, output_dir: str) -> List[str]:
    """Generate IFC files for each segment model."""

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    segment_groups = models_df.groupby('segment_model')['pyramid_name'].apply(list).to_dict()
    coord_lookup = coords_df.set_index('pyramid_name').to_dict('index')

    generated_files = []

    for segment_name, pyramid_names in segment_groups.items():
        print(f"\n📦 Generating IFC for segment: {segment_name}")

        generator = IFCLight("../templates")
        generator.create_file(f"Project {segment_name}")

        for pyramid_name in pyramid_names:
            if pyramid_name in coord_lookup:
                coords = coord_lookup[pyramid_name]
                lv95_coords = (coords['LV95_X'], coords['LV95_Y'], coords['LV95_Z'])

                element_type = pyramid_name.split('_')[-1]

                pyramid_data = {
                    'measurement_date': coords.get('measurement_date'),
                    'accuracy_class': coords.get('accuracy_class'),
                    'measurement_method': coords.get('measurement_method'),
                    'operator': coords.get('operator'),
                    'status': coords.get('status'),
                    'remarks': coords.get('remarks')
                }

                generator.add_pyramid(
                    lv95_coords=lv95_coords,
                    name=pyramid_name,
                    element_type=element_type if element_type in ['REF', 'SUR', 'CTL', 'MON', 'BND', 'GEO', 'BEN'] else 'REF',
                    sector='TEST',
                    phase='PL',
                    pyramid_data=pyramid_data
                )
                print(f"  ✓ Added pyramid: {pyramid_name}")

        output_file = os.path.join(output_dir, f"{segment_name}.ifc")
        generator.save(output_file)
        generated_files.append(output_file)
        print(f"  ✓ Saved: {output_file}")

    return generated_files


def create_ids_xml_for_segment(segment_name: str, pyramid_names: List[str], coords_df: pd.DataFrame, output_path: str):
    """Create IDS XML specification for a specific segment using template."""

    # Read template
    template_path = Path(__file__).parent.parent / 'templates' / 'ids_validation.xml'
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Create specification blocks for additional pyramids (first one is in template)
    spec_template = '''
    <specification name="{{PYRAMID_NAME}}_check" ifcVersion="IFC4X3_ADD2">
      <applicability>
        <entity>
          <name>
            <simpleValue>IFCBUILDINGELEMENTPROXY</simpleValue>
          </name>
        </entity>
        <attribute>
          <name>
            <simpleValue>Name</simpleValue>
          </name>
          <value>
            <simpleValue>{{PYRAMID_NAME}}</simpleValue>
          </value>
        </attribute>
      </applicability>
      <requirements>
        <property cardinality="required" dataType="IFCLENGTHMEASURE">
          <propertySet>
            <simpleValue>ASTRA_Georeferencing</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>BP_E</simpleValue>
          </baseName>
        </property>
        <property cardinality="required" dataType="IFCLENGTHMEASURE">
          <propertySet>
            <simpleValue>ASTRA_Georeferencing</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>BP_N</simpleValue>
          </baseName>
        </property>
        <property cardinality="required" dataType="IFCLENGTHMEASURE">
          <propertySet>
            <simpleValue>ASTRA_Georeferencing</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>BP_H</simpleValue>
          </baseName>
        </property>
        <property cardinality="required" dataType="IFCLABEL">
          <propertySet>
            <simpleValue>ASTRA_CommonPSet_LoGeoRef</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>status</simpleValue>
          </baseName>
        </property>
      </requirements>
    </specification>'''

    # Build additional specs for pyramids beyond the first
    additional_specs = []
    for pyramid_name in pyramid_names[1:]:
        spec = spec_template.replace('{{PYRAMID_NAME}}', pyramid_name)
        additional_specs.append(spec)

    additional_specs_str = ''.join(additional_specs)

    # Replace placeholders
    xml_content = template.replace('{{TITLE}}', f'Validation for {segment_name}')
    xml_content = xml_content.replace('{{DESCRIPTION}}', f'Validates pyramids in segment {segment_name}')
    xml_content = xml_content.replace('{{DATE}}', datetime.now().strftime('%Y-%m-%d'))
    xml_content = xml_content.replace('{{PYRAMID_NAME}}', pyramid_names[0])  # First pyramid
    xml_content = xml_content.replace('{{ADDITIONAL_SPECS}}', additional_specs_str)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    print(f"✅ Created IDS XML for {segment_name}: {output_path}")


def validate_segment_with_ifctester(ifc_file: str, ids_file: str, output_dir: str) -> Dict:
    """Validate a single IFC file using ifctester and generate report."""

    from ifctester import reporter, ids

    segment_name = Path(ifc_file).stem
    print(f"  Validating {segment_name}...")

    try:
        # Load IDS
        my_ids = ids.open(ids_file)

        # Load IFC
        ifc_model = ifcopenshell.open(ifc_file)

        # Validate
        my_ids.validate(ifc_model)

        # Generate report
        report_path = os.path.join(output_dir, f'{segment_name}_validation.html')
        reporter.Html(my_ids).report()
        reporter.Html(my_ids).to_file(report_path)

        # Get summary
        total_specs = len(my_ids.specifications)
        passed_specs = sum(1 for spec in my_ids.specifications if spec.status)

        result = {
            'file': ifc_file,
            'ids_file': ids_file,
            'total': total_specs,
            'passed': passed_specs,
            'failed': total_specs - passed_specs,
            'status': 'PASSED' if passed_specs == total_specs else 'FAILED',
            'report': report_path
        }

        status = '✅ PASSED' if passed_specs == total_specs else '❌ FAILED'
        print(f"    {status} ({passed_specs}/{total_specs} specifications)")

        return result

    except Exception as e:
        print(f"    ❌ ERROR: {e}")
        return {
            'file': ifc_file,
            'ids_file': ids_file,
            'error': str(e),
            'status': 'ERROR'
        }


def generate_summary_report(results: Dict, models_df: pd.DataFrame, output_path: str):
    """Generate a comprehensive summary report."""

    report = []
    report.append("=" * 80)
    report.append("IFC VALIDATION REPORT (IDS + ifctester)")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Summary
    total_files = len(results)
    passed_files = sum(1 for r in results.values() if r.get('status') == 'PASSED')

    report.append(f"Summary: {passed_files}/{total_files} files passed validation")
    report.append("-" * 80)

    # Results per file
    for segment_name, result in results.items():
        report.append(f"\n📁 Segment: {segment_name}")
        report.append(f"   File: {os.path.basename(result['file'])}")

        if result['status'] == 'ERROR':
            report.append(f"   Status: ❌ ERROR")
            report.append(f"   Error: {result['error']}")
        else:
            status_icon = '✅' if result['status'] == 'PASSED' else '❌'
            report.append(f"   Status: {status_icon} {result['status']}")
            report.append(f"   Specifications: {result['passed']}/{result['total']} passed")
            if 'report' in result:
                report.append(f"   HTML Report: {result['report']}")

    # Shared pyramids analysis
    report.append("\n" + "=" * 80)
    report.append("SHARED PYRAMIDS ANALYSIS")
    report.append("=" * 80)

    segment_groups = models_df.groupby('segment_model')['pyramid_name'].apply(set).to_dict()
    segments = list(segment_groups.keys())

    for i, seg1 in enumerate(segments):
        for seg2 in segments[i+1:]:
            shared = segment_groups[seg1] & segment_groups[seg2]
            if shared:
                report.append(f"\n✓ {seg1} ∩ {seg2}:")
                for pyramid in shared:
                    report.append(f"  - {pyramid}")

    # Statistics
    report.append("\n" + "=" * 80)
    report.append("STATISTICS")
    report.append("=" * 80)

    unique_pyramids = models_df['pyramid_name'].nunique()
    total_references = len(models_df)
    report.append(f"Unique pyramids: {unique_pyramids}")
    report.append(f"Total references: {total_references}")
    report.append(f"Segments: {len(segments)}")

    report_text = "\n".join(report)

    # Write to file
    with open(output_path, 'w') as f:
        f.write(report_text)

    return report_text


def test_excel_ids_validation():
    """Main test function using IDS XML and ifctester."""

    print("\n" + "=" * 80)
    print("🧪 TEST: Excel-Driven IFC with IDS XML Validation (ifctester)")
    print("=" * 80)

    # Setup paths
    test_dir = Path(__file__).parent
    excel_file = test_dir / "test_data.xlsx"
    output_dir = test_dir.parent / "output" / "excel_ids_test"

    # Step 1: Create test Excel
    print("\n📊 Step 1: Creating test Excel file...")
    create_test_excel(str(excel_file))

    # Step 2: Read Excel data
    print("\n📖 Step 2: Reading Excel data...")
    models_df = pd.read_excel(excel_file, sheet_name='models')
    coords_df = pd.read_excel(excel_file, sheet_name='pyramid-coordinates')
    print(f"  ✓ Found {len(models_df)} pyramid references")
    print(f"  ✓ Found {len(coords_df)} unique pyramids")

    # Step 3: Generate IFC files
    print("\n🏗️ Step 3: Generating IFC files...")
    ifc_files = generate_ifc_files(models_df, coords_df, str(output_dir))
    print(f"\n  ✓ Generated {len(ifc_files)} IFC files")

    # Step 4: Create IDS XML files (one per segment)
    print("\n📋 Step 4: Creating IDS XML specifications (one per segment)...")
    segment_groups = models_df.groupby('segment_model')['pyramid_name'].apply(list).to_dict()
    ids_files = {}

    for segment_name, pyramid_names in segment_groups.items():
        ids_file = output_dir / f"{segment_name}_validation.ids"
        create_ids_xml_for_segment(segment_name, pyramid_names, coords_df, str(ids_file))
        ids_files[segment_name] = str(ids_file)

    # Step 5: Validate with ifctester
    print("\n✅ Step 5: Validating with ifctester...")
    results = {}
    for ifc_file in ifc_files:
        segment_name = Path(ifc_file).stem
        ids_file = ids_files.get(segment_name)
        if ids_file:
            result = validate_segment_with_ifctester(ifc_file, ids_file, str(output_dir))
            results[segment_name] = result

    # Step 6: Generate summary report
    print("\n📄 Step 6: Generating summary report...")
    report_file = output_dir / "validation_summary.txt"
    report = generate_summary_report(results, models_df, str(report_file))
    print(f"  ✓ Report saved to: {report_file}")

    # Print report
    print("\n" + report)

    # Final assertions
    print("\n" + "=" * 80)
    print("TEST ASSERTIONS")
    print("=" * 80)

    assert len(ifc_files) == 3, f"Expected 3 IFC files, got {len(ifc_files)}"
    print("✓ 3 IFC files created")

    assert len(ids_files) == 3, f"Expected 3 IDS XML files, got {len(ids_files)}"
    print("✓ 3 IDS XML files created (one per segment)")

    all_passed = all(r.get('status') == 'PASSED' for r in results.values())
    assert all_passed, "Some IFC files failed validation"
    print("✓ All IFC files passed IDS validation")

    print("\n" + "=" * 80)
    print("🎉 TEST PASSED: Excel workflow with IDS validation completed!")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = test_excel_ids_validation()