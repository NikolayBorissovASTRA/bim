#!/usr/bin/env python3
"""
Excel-driven IFC generation with IDS value validation using ifctester.
This test validates not just the presence of properties, but their actual values
from the Excel pyramid-coordinates sheet.
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

                # Extract all pyramid data from Excel columns
                pyramid_data = {
                    'measurement_date': str(coords.get('measurement_date')),
                    'accuracy_class': str(coords.get('accuracy_class')),
                    'measurement_method': str(coords.get('measurement_method')),
                    'operator': str(coords.get('operator')),
                    'status': str(coords.get('status')),
                    'remarks': str(coords.get('remarks'))
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


def create_ids_xml_with_values(segment_name: str, pyramid_names: List[str], coords_df: pd.DataFrame, output_path: str):
    """Create IDS XML specification with value validation for a specific segment."""

    # Read template
    template_path = Path(__file__).parent.parent / 'templates' / 'ids_validation_with_values.xml'
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    coord_lookup = coords_df.set_index('pyramid_name').to_dict('index')

    # Get data for first pyramid
    first_pyramid = pyramid_names[0]
    first_coords = coord_lookup[first_pyramid]

    # Replace placeholders for first pyramid in template
    xml_content = template.replace('{{TITLE}}', f'Value Validation for {segment_name}')
    xml_content = xml_content.replace('{{DESCRIPTION}}', f'Validates pyramid values in segment {segment_name}')
    xml_content = xml_content.replace('{{DATE}}', datetime.now().strftime('%Y-%m-%d'))
    xml_content = xml_content.replace('{{PYRAMID_NAME}}', first_pyramid)
    xml_content = xml_content.replace('{{BP_E}}', str(first_coords['LV95_X']))
    xml_content = xml_content.replace('{{BP_N}}', str(first_coords['LV95_Y']))
    xml_content = xml_content.replace('{{BP_H}}', str(first_coords['LV95_Z']))
    xml_content = xml_content.replace('{{MEASUREMENT_DATE}}', str(first_coords['measurement_date']))
    xml_content = xml_content.replace('{{ACCURACY_CLASS}}', str(first_coords['accuracy_class']))
    xml_content = xml_content.replace('{{MEASUREMENT_METHOD}}', str(first_coords['measurement_method']))
    xml_content = xml_content.replace('{{OPERATOR}}', str(first_coords['operator']))
    xml_content = xml_content.replace('{{STATUS}}', str(first_coords['status']))
    xml_content = xml_content.replace('{{REMARKS}}', str(first_coords['remarks']))

    # Build additional specs for other pyramids
    additional_specs = []
    for pyramid_name in pyramid_names[1:]:
        if pyramid_name not in coord_lookup:
            continue

        coords = coord_lookup[pyramid_name]

        spec = f'''
    <specification name="{pyramid_name}_check" ifcVersion="IFC4X3_ADD2">
      <applicability>
        <entity>
          <name>
            <simpleValue>IFCVIRTUALELEMENT</simpleValue>
          </name>
        </entity>
        <attribute>
          <name>
            <simpleValue>Name</simpleValue>
          </name>
          <value>
            <simpleValue>{pyramid_name}</simpleValue>
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
          <value>
            <simpleValue>{coords['LV95_X']}</simpleValue>
          </value>
        </property>
        <property cardinality="required" dataType="IFCLENGTHMEASURE">
          <propertySet>
            <simpleValue>ASTRA_Georeferencing</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>BP_N</simpleValue>
          </baseName>
          <value>
            <simpleValue>{coords['LV95_Y']}</simpleValue>
          </value>
        </property>
        <property cardinality="required" dataType="IFCLENGTHMEASURE">
          <propertySet>
            <simpleValue>ASTRA_Georeferencing</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>BP_H</simpleValue>
          </baseName>
          <value>
            <simpleValue>{coords['LV95_Z']}</simpleValue>
          </value>
        </property>
        <property cardinality="required" dataType="IFCLABEL">
          <propertySet>
            <simpleValue>ASTRA_CommonPSet_LoGeoRef</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>measurement_date</simpleValue>
          </baseName>
          <value>
            <simpleValue>{coords['measurement_date']}</simpleValue>
          </value>
        </property>
        <property cardinality="required" dataType="IFCLABEL">
          <propertySet>
            <simpleValue>ASTRA_CommonPSet_LoGeoRef</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>accuracy_class</simpleValue>
          </baseName>
          <value>
            <simpleValue>{coords['accuracy_class']}</simpleValue>
          </value>
        </property>
        <property cardinality="required" dataType="IFCLABEL">
          <propertySet>
            <simpleValue>ASTRA_CommonPSet_LoGeoRef</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>measurement_method</simpleValue>
          </baseName>
          <value>
            <simpleValue>{coords['measurement_method']}</simpleValue>
          </value>
        </property>
        <property cardinality="required" dataType="IFCLABEL">
          <propertySet>
            <simpleValue>ASTRA_CommonPSet_LoGeoRef</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>operator</simpleValue>
          </baseName>
          <value>
            <simpleValue>{coords['operator']}</simpleValue>
          </value>
        </property>
        <property cardinality="required" dataType="IFCLABEL">
          <propertySet>
            <simpleValue>ASTRA_CommonPSet_LoGeoRef</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>status</simpleValue>
          </baseName>
          <value>
            <simpleValue>{coords['status']}</simpleValue>
          </value>
        </property>
        <property cardinality="required" dataType="IFCTEXT">
          <propertySet>
            <simpleValue>ASTRA_CommonPSet_LoGeoRef</simpleValue>
          </propertySet>
          <baseName>
            <simpleValue>remarks</simpleValue>
          </baseName>
          <value>
            <simpleValue>{coords['remarks']}</simpleValue>
          </value>
        </property>
      </requirements>
    </specification>'''
        additional_specs.append(spec)

    xml_content = xml_content.replace('{{ADDITIONAL_SPECS}}', ''.join(additional_specs))

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    print(f"✅ Created IDS XML with value validation for {segment_name}: {output_path}")


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
        report_path = os.path.join(output_dir, f'{segment_name}_value_validation.html')
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
    report.append("IFC VALUE VALIDATION REPORT (IDS + ifctester)")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("This report validates not just property presence, but actual values")
    report.append("from the Excel pyramid-coordinates sheet.\n")

    # Summary
    total_files = len(results)
    passed_files = sum(1 for r in results.values() if r.get('status') == 'PASSED')

    report.append(f"Summary: {passed_files}/{total_files} files passed value validation")
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

    # Statistics
    report.append("\n" + "=" * 80)
    report.append("VALIDATION DETAILS")
    report.append("=" * 80)

    unique_pyramids = models_df['pyramid_name'].nunique()
    total_references = len(models_df)
    report.append(f"Unique pyramids: {unique_pyramids}")
    report.append(f"Total references: {total_references}")
    report.append(f"Segments: {len(results)}")
    report.append("\nEach specification validates:")
    report.append("  - Exact coordinate values (BP_E, BP_N, BP_H)")
    report.append("  - Exact metadata values (measurement_date, accuracy_class, etc.)")

    report_text = "\n".join(report)

    # Write to file
    with open(output_path, 'w') as f:
        f.write(report_text)

    return report_text


def test_excel_ids_value_validation():
    """Main test function with value validation."""

    print("\n" + "=" * 80)
    print("🧪 TEST: Excel-Driven IFC with IDS VALUE Validation (ifctester)")
    print("=" * 80)
    print("This test validates actual property VALUES from Excel\n")

    # Setup paths
    test_dir = Path(__file__).parent
    excel_file = test_dir / "test_data.xlsx"
    output_dir = test_dir.parent / "output" / "excel_ids_value_test"

    if not excel_file.exists():
        print(f"❌ Test data file not found: {excel_file}")
        print("   Run: uv run python generate_test_data.py")
        sys.exit(1)

    # Read Excel data
    print("📖 Reading test data from Excel...")
    models_df = pd.read_excel(excel_file, sheet_name='models')
    coords_df = pd.read_excel(excel_file, sheet_name='pyramid-coordinates')
    print(f"  ✓ Found {len(models_df)} pyramid references")
    print(f"  ✓ Found {len(coords_df)} unique pyramids with metadata")

    # Generate IFC files
    print("\n🏗️ Generating IFC files with all property values...")
    ifc_files = generate_ifc_files(models_df, coords_df, str(output_dir))
    print(f"\n  ✓ Generated {len(ifc_files)} IFC files")

    # Create IDS XML files with value validation (one per segment)
    print("\n📋 Creating IDS XML specifications with VALUE validation...")
    segment_groups = models_df.groupby('segment_model')['pyramid_name'].apply(list).to_dict()
    ids_files = {}

    for segment_name, pyramid_names in segment_groups.items():
        ids_file = output_dir / f"{segment_name}_value_validation.ids"
        create_ids_xml_with_values(segment_name, pyramid_names, coords_df, str(ids_file))
        ids_files[segment_name] = str(ids_file)

    # Validate with ifctester
    print("\n✅ Validating property VALUES with ifctester...")
    results = {}
    for ifc_file in ifc_files:
        segment_name = Path(ifc_file).stem
        ids_file = ids_files.get(segment_name)
        if ids_file:
            result = validate_segment_with_ifctester(ifc_file, ids_file, str(output_dir))
            results[segment_name] = result

    # Generate summary report
    print("\n📄 Generating summary report...")
    report_file = output_dir / "value_validation_summary.txt"
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
    print("✓ 3 IDS XML files created with value validation")

    all_passed = all(r.get('status') == 'PASSED' for r in results.values())
    assert all_passed, "Some IFC files failed value validation"
    print("✓ All IFC files passed IDS value validation")
    print("  (All property values match Excel data exactly)")

    print("\n" + "=" * 80)
    print("🎉 TEST PASSED: Excel workflow with VALUE validation completed!")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = test_excel_ids_value_validation()
