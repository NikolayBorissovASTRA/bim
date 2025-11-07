#!/usr/bin/env python3
"""
Test case for Excel-driven IFC generation with IDS validation.
Tests reading Excel data, generating multiple IFC files, and validating with IDS.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
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

    # Sheet 2: Pyramid Coordinates - LV95 coordinates and metadata for each unique pyramid
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

    # Create Excel file with two sheets
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        pd.DataFrame(models_data).to_excel(writer, sheet_name='models', index=False)
        pd.DataFrame(coordinates_data).to_excel(writer, sheet_name='pyramid-coordinates', index=False)

    print(f"✅ Created test Excel file: {filepath}")
    return models_data, coordinates_data


def read_excel_data(filepath: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Read Excel file and return models and coordinates dataframes."""
    models_df = pd.read_excel(filepath, sheet_name='models')
    coords_df = pd.read_excel(filepath, sheet_name='pyramid-coordinates')
    return models_df, coords_df


def generate_ifc_files(models_df: pd.DataFrame, coords_df: pd.DataFrame, output_dir: str) -> List[str]:
    """Generate IFC files for each segment model."""

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Group pyramids by segment model
    segment_groups = models_df.groupby('segment_model')['pyramid_name'].apply(list).to_dict()

    # Create coordinate lookup
    coord_lookup = coords_df.set_index('pyramid_name').to_dict('index')

    generated_files = []

    for segment_name, pyramid_names in segment_groups.items():
        print(f"\n📦 Generating IFC for segment: {segment_name}")

        # Create IFC file
        generator = IFCLight("../templates")
        generator.create_file(f"Project {segment_name}")

        # Add pyramids
        for pyramid_name in pyramid_names:
            if pyramid_name in coord_lookup:
                coords = coord_lookup[pyramid_name]
                lv95_coords = (coords['LV95_X'], coords['LV95_Y'], coords['LV95_Z'])

                # Extract type from name (e.g., PYR_001_REF -> REF)
                element_type = pyramid_name.split('_')[-1]

                # Extract pyramid-specific data from coordinates sheet
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
                print(f"  ✓ Added pyramid: {pyramid_name} at ({coords['LV95_X']:.2f}, {coords['LV95_Y']:.2f}, {coords['LV95_Z']:.2f})")

        # Save IFC file
        output_file = os.path.join(output_dir, f"{segment_name}.ifc")
        generator.save(output_file)
        generated_files.append(output_file)
        print(f"  ✓ Saved: {output_file}")

    return generated_files


def create_ids_specification(models_df: pd.DataFrame, coords_df: pd.DataFrame) -> Dict:
    """Create IDS (Information Delivery Specification) for validation."""

    # Create IDS structure
    ids_spec = {
        "title": "IFC Pyramid Validation Specification",
        "version": "1.0",
        "description": "Validates pyramids in IFC files against Excel data",
        "specifications": []
    }

    # Group by segment for specifications
    segment_groups = models_df.groupby('segment_model')['pyramid_name'].apply(list).to_dict()
    coord_lookup = coords_df.set_index('pyramid_name').to_dict('index')

    for segment_name, pyramid_names in segment_groups.items():
        segment_spec = {
            "name": f"Validation for {segment_name}",
            "description": f"Validates pyramids in segment {segment_name}",
            "applicability": {
                "entity": "IfcBuildingElementProxy",
                "description": "Applies to all pyramid elements"
            },
            "requirements": []
        }

        # Add requirements for each pyramid
        for pyramid_name in pyramid_names:
            if pyramid_name in coord_lookup:
                coords = coord_lookup[pyramid_name]

                pyramid_req = {
                    "name": f"Pyramid {pyramid_name}",
                    "description": f"Requirements for {pyramid_name}",
                    "facets": [
                        {
                            "type": "property",
                            "propertySet": "Identity",
                            "property": "Name",
                            "value": pyramid_name
                        },
                        {
                            "type": "property",
                            "propertySet": "ASTRA_Georeferencing",
                            "property": "BP_E",
                            "value": coords['LV95_X'],
                            "tolerance": 0.001
                        },
                        {
                            "type": "property",
                            "propertySet": "ASTRA_Georeferencing",
                            "property": "BP_N",
                            "value": coords['LV95_Y'],
                            "tolerance": 0.001
                        },
                        {
                            "type": "property",
                            "propertySet": "ASTRA_Georeferencing",
                            "property": "BP_H",
                            "value": coords['LV95_Z'],
                            "tolerance": 0.001
                        }
                    ]
                }
                segment_spec["requirements"].append(pyramid_req)

        ids_spec["specifications"].append(segment_spec)

    return ids_spec


def validate_ifc_against_ids(ifc_file: str, ids_spec: Dict, segment_name: str) -> Dict:
    """Validate an IFC file against IDS specification."""

    validation_results = {
        "file": ifc_file,
        "segment": segment_name,
        "timestamp": datetime.now().isoformat(),
        "passed": True,
        "validations": []
    }

    # Open IFC file
    ifc = ifcopenshell.open(ifc_file)

    # Get all pyramids
    pyramids = ifc.by_type("IfcBuildingElementProxy")
    pyramid_dict = {p.Name: p for p in pyramids if p.Name}

    # Find the specification for this segment
    segment_spec = None
    for spec in ids_spec["specifications"]:
        if segment_name in spec["name"]:
            segment_spec = spec
            break

    if not segment_spec:
        validation_results["passed"] = False
        validation_results["error"] = f"No specification found for segment {segment_name}"
        return validation_results

    # Validate each requirement
    for requirement in segment_spec["requirements"]:
        pyramid_name = requirement["name"].replace("Pyramid ", "")
        validation_item = {
            "pyramid": pyramid_name,
            "checks": []
        }

        # Check if pyramid exists
        if pyramid_name not in pyramid_dict:
            validation_item["checks"].append({
                "check": "Pyramid exists",
                "passed": False,
                "message": f"Pyramid {pyramid_name} not found in IFC file"
            })
            validation_results["passed"] = False
        else:
            pyramid = pyramid_dict[pyramid_name]
            validation_item["checks"].append({
                "check": "Pyramid exists",
                "passed": True,
                "message": f"Found pyramid {pyramid_name}"
            })

            # Check ASTRA properties
            prop_rels = [rel for rel in ifc.by_type("IfcRelDefinesByProperties")
                        if pyramid in rel.RelatedObjects]

            if prop_rels:
                # Check both property sets
                georef_found = False
                pyramid_data_found = False

                for rel in prop_rels:
                    pset = rel.RelatingPropertyDefinition
                    if pset.Name == "ASTRA_Georeferencing":
                        georef_found = True
                        props = {p.Name: p.NominalValue.wrappedValue for p in pset.HasProperties}

                        # Validate coordinates
                        for facet in requirement["facets"]:
                            if facet.get("propertySet") == "ASTRA_Georeferencing":
                                prop_name = facet["property"]
                                expected_value = facet["value"]
                                tolerance = facet.get("tolerance", 0.001)

                                if prop_name in props:
                                    actual_value = props[prop_name]
                                    if isinstance(actual_value, str):
                                        # For EPSG_Code
                                        passed = str(expected_value) == actual_value
                                    else:
                                        # For numeric values
                                        passed = abs(float(actual_value) - float(expected_value)) <= tolerance

                                    validation_item["checks"].append({
                                        "check": f"Property {prop_name}",
                                        "passed": passed,
                                        "expected": expected_value,
                                        "actual": actual_value,
                                        "message": f"{prop_name}: {'✓' if passed else '✗'} (expected: {expected_value}, actual: {actual_value})"
                                    })

                                    if not passed:
                                        validation_results["passed"] = False

                    elif pset.Name == "ASTRA_CommonPSet_LoGeoRef":
                        pyramid_data_found = True
                        validation_item["checks"].append({
                            "check": "ASTRA_CommonPSet_LoGeoRef property set",
                            "passed": True,
                            "message": "✓ Found ASTRA_CommonPSet_LoGeoRef property set"
                        })

                # Check if both property sets exist
                if not georef_found:
                    validation_item["checks"].append({
                        "check": "ASTRA_Georeferencing property set",
                        "passed": False,
                        "message": "✗ ASTRA_Georeferencing property set not found"
                    })
                    validation_results["passed"] = False

        validation_results["validations"].append(validation_item)

    return validation_results


def generate_validation_report(all_results: List[Dict], models_df: pd.DataFrame) -> str:
    """Generate a comprehensive validation report."""

    report = []
    report.append("=" * 80)
    report.append("IFC VALIDATION REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Summary
    total_passed = sum(1 for r in all_results if r["passed"])
    report.append(f"Summary: {total_passed}/{len(all_results)} files passed validation")
    report.append("-" * 40)

    # Detailed results for each file
    for result in all_results:
        report.append(f"\n📁 File: {os.path.basename(result['file'])}")
        report.append(f"   Segment: {result['segment']}")
        report.append(f"   Status: {'✅ PASSED' if result['passed'] else '❌ FAILED'}")

        if 'validations' in result:
            for validation in result['validations']:
                report.append(f"   \n   Pyramid: {validation['pyramid']}")
                for check in validation['checks']:
                    status = "✓" if check['passed'] else "✗"
                    report.append(f"     {status} {check['check']}: {check.get('message', '')}")

    # Shared pyramids analysis
    report.append("\n" + "=" * 80)
    report.append("SHARED PYRAMIDS ANALYSIS")
    report.append("=" * 80)

    # Find shared pyramids
    segment_groups = models_df.groupby('segment_model')['pyramid_name'].apply(set).to_dict()
    segments = list(segment_groups.keys())

    shared_found = False
    for i, seg1 in enumerate(segments):
        for seg2 in segments[i+1:]:
            shared = segment_groups[seg1] & segment_groups[seg2]
            if shared:
                shared_found = True
                report.append(f"\n✓ {seg1} ∩ {seg2}:")
                for pyramid in shared:
                    report.append(f"  - {pyramid}")

    if not shared_found:
        report.append("\n⚠️ No shared pyramids found between segments")

    # Statistics
    report.append("\n" + "=" * 80)
    report.append("STATISTICS")
    report.append("=" * 80)

    unique_pyramids = models_df['pyramid_name'].nunique()
    total_references = len(models_df)
    report.append(f"Unique pyramids: {unique_pyramids}")
    report.append(f"Total references: {total_references}")
    report.append(f"Average references per pyramid: {total_references/unique_pyramids:.2f}")

    report_text = "\n".join(report)
    return report_text


def test_excel_workflow():
    """Main test function for Excel-driven IFC generation and validation."""

    print("\n" + "=" * 80)
    print("🧪 TEST: Excel-Driven IFC Generation with IDS Validation")
    print("=" * 80)

    # Setup paths
    test_dir = Path(__file__).parent
    excel_file = test_dir / "test_data.xlsx"
    output_dir = test_dir.parent / "output" / "excel_test"

    # Step 1: Create test Excel file
    print("\n📊 Step 1: Creating test Excel file...")
    models_data, coords_data = create_test_excel(str(excel_file))

    # Step 2: Read Excel data
    print("\n📖 Step 2: Reading Excel data...")
    models_df, coords_df = read_excel_data(str(excel_file))
    print(f"  ✓ Found {len(models_df)} pyramid references")
    print(f"  ✓ Found {len(coords_df)} unique pyramids")

    # Step 3: Generate IFC files
    print("\n🏗️ Step 3: Generating IFC files...")
    ifc_files = generate_ifc_files(models_df, coords_df, str(output_dir))
    print(f"\n  ✓ Generated {len(ifc_files)} IFC files")

    # Step 4: Create IDS specification
    print("\n📋 Step 4: Creating IDS specification...")
    ids_spec = create_ids_specification(models_df, coords_df)
    ids_file = output_dir / "validation_spec.json"
    with open(ids_file, 'w') as f:
        json.dump(ids_spec, f, indent=2)
    print(f"  ✓ Created IDS specification with {len(ids_spec['specifications'])} segments")

    # Step 5: Validate IFC files
    print("\n✅ Step 5: Validating IFC files against IDS...")
    all_results = []
    segment_names = models_df['segment_model'].unique()

    for ifc_file, segment_name in zip(ifc_files, segment_names):
        print(f"  Validating {segment_name}...")
        result = validate_ifc_against_ids(ifc_file, ids_spec, segment_name)
        all_results.append(result)
        status = "✅ PASSED" if result["passed"] else "❌ FAILED"
        print(f"    {status}")

    # Step 6: Generate validation report
    print("\n📄 Step 6: Generating validation report...")
    report = generate_validation_report(all_results, models_df)
    report_file = output_dir / "validation_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"  ✓ Report saved to: {report_file}")

    # Print report to console
    print("\n" + report)

    # Final assertions
    print("\n" + "=" * 80)
    print("TEST ASSERTIONS")
    print("=" * 80)

    # Assert all files were created
    assert len(ifc_files) == 3, f"Expected 3 IFC files, got {len(ifc_files)}"
    print("✓ 3 IFC files created")

    # Assert shared pyramids exist
    segment_groups = models_df.groupby('segment_model')['pyramid_name'].apply(set).to_dict()
    shared_a1_b2 = segment_groups['SEGMENT_A1'] & segment_groups['SEGMENT_B2']
    shared_b2_c3 = segment_groups['SEGMENT_B2'] & segment_groups['SEGMENT_C3']

    assert 'PYR_003_CTL' in shared_a1_b2, "PYR_003_CTL should be shared between A1 and B2"
    assert 'PYR_005_BND' in shared_b2_c3, "PYR_005_BND should be shared between B2 and C3"
    print("✓ Shared pyramids validated")

    # Assert all validations passed
    all_passed = all(r["passed"] for r in all_results)
    assert all_passed, "Some IFC files failed validation"
    print("✓ All IFC files passed IDS validation")

    print("\n" + "=" * 80)
    print("🎉 TEST PASSED: Excel workflow completed successfully!")
    print("=" * 80)

    return True


if __name__ == "__main__":
    # Install required packages if needed
    try:
        import pandas
        import openpyxl
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call(["uv", "add", "pandas", "openpyxl"])
        import pandas
        import openpyxl

    # Run test
    success = test_excel_workflow()