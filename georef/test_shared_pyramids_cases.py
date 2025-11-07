#!/usr/bin/env python3
"""
Test cases for shared pyramids validation including:
- Case 1: Valid - all segments share at least one pyramid
- Case 2: Valid - segments share multiple pyramids
- Case 3: Invalid - one segment has no shared pyramids
"""

import sys
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook


def create_test_case_excel(case_name: str, models_data: dict, coords_data: dict) -> Path:
    """Create a test case Excel file."""

    test_file = Path(__file__).parent / f"test_data_{case_name}.xlsx"

    with pd.ExcelWriter(test_file, engine='openpyxl') as writer:
        pd.DataFrame(models_data).to_excel(writer, sheet_name='models', index=False)
        pd.DataFrame(coords_data).to_excel(writer, sheet_name='pyramid-coordinates', index=False)

    return test_file


def test_shared_pyramids(excel_file: Path, expected_pass: bool) -> bool:
    """Test shared pyramids and write report to Excel."""

    models_df = pd.read_excel(excel_file, sheet_name='models')

    # Group pyramids by segment
    segment_groups = models_df.groupby('segment_model')['pyramid_name'].apply(set).to_dict()
    segments = sorted(segment_groups.keys())

    # Build sharing report
    report_data = []
    segment_has_sharing = {segment: False for segment in segments}

    for segment in segments:
        for other_segment in segments:
            if segment < other_segment:  # Avoid duplicate pairs
                shared = segment_groups[segment] & segment_groups[other_segment]
                if shared:
                    segment_has_sharing[segment] = True
                    segment_has_sharing[other_segment] = True
                    report_data.append({
                        'segment_1': segment,
                        'segment_2': other_segment,
                        'shared_pyramids': ', '.join(sorted(shared)),
                        'count': len(shared)
                    })

    # Create report DataFrame
    report_df = pd.DataFrame(report_data)

    # Add rows for segments without sharing
    isolated_segments = []
    for segment, has_sharing in segment_has_sharing.items():
        if not has_sharing:
            isolated_segments.append({
                'segment_1': segment,
                'segment_2': 'NO SHARING',
                'shared_pyramids': 'This segment has no shared pyramids with any other segment',
                'count': 0
            })

    isolated_df = pd.DataFrame(isolated_segments)

    # Calculate summary statistics
    unique_pyramids = models_df['pyramid_name'].nunique()
    total_references = len(models_df)
    segments_with_sharing = sum(segment_has_sharing.values())
    total_shared_pyramids = len(set(models_df[models_df.duplicated('pyramid_name', keep=False)]['pyramid_name']))
    total_sharing_pairs = len(report_data)

    # Add summary row
    summary_data = [{
        'segment_1': 'SUMMARY',
        'segment_2': f'{len(segments)} segments total, {segments_with_sharing} have sharing',
        'shared_pyramids': f'{total_shared_pyramids} unique pyramids are shared across {total_sharing_pairs} segment pairs',
        'count': total_shared_pyramids
    }]
    summary_df = pd.DataFrame(summary_data)

    # Combine all sections: pairs with sharing, isolated segments, summary
    final_report = pd.concat([report_df, isolated_df, summary_df], ignore_index=True)

    # Write to Excel
    with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        final_report.to_excel(writer, sheet_name='report', index=False)

    # Validate all segments have sharing
    all_valid = all(segment_has_sharing.values())

    test_passed = all_valid == expected_pass

    if test_passed:
        status = "✅ PASSED" if all_valid else "✅ PASSED (expected failure)"
        print(f"{status}: {excel_file.name}")
        return True
    else:
        missing = [s for s, has in segment_has_sharing.items() if not has]
        print(f"❌ FAILED: {excel_file.name} - Segments without sharing: {missing}")
        return False


def run_all_test_cases():
    """Run all test cases."""

    print("=" * 80)
    print("🧪 SHARED PYRAMIDS TEST CASES")
    print("=" * 80)

    # Case 1: Valid - Each segment shares at least one pyramid (current test_data.xlsx)
    print("\n📋 Case 1: Valid - Each segment shares at least one pyramid")
    models_1 = {
        'segment_model': [
            'SEGMENT_A1', 'SEGMENT_A1', 'SEGMENT_A1',
            'SEGMENT_B2', 'SEGMENT_B2', 'SEGMENT_B2',
            'SEGMENT_C3', 'SEGMENT_C3', 'SEGMENT_C3'
        ],
        'pyramid_name': [
            'PYR_001_REF', 'PYR_002_SUR', 'PYR_003_CTL',
            'PYR_003_CTL', 'PYR_004_MON', 'PYR_005_BND',
            'PYR_005_BND', 'PYR_006_GEO', 'PYR_007_BEN'
        ]
    }
    coords_1 = {
        'pyramid_name': ['PYR_001_REF', 'PYR_002_SUR', 'PYR_003_CTL', 'PYR_004_MON',
                        'PYR_005_BND', 'PYR_006_GEO', 'PYR_007_BEN'],
        'LV95_X': [2679520.05, 2679525.00, 2679530.00, 2679535.00, 2679540.00, 2679545.00, 2679550.00],
        'LV95_Y': [1151703.09, 1151708.00, 1151713.00, 1151718.00, 1151723.00, 1151728.00, 1151733.00],
        'LV95_Z': [500.0, 501.0, 502.0, 503.0, 504.0, 505.0, 506.0],
        'measurement_date': ['2024-01-15'] * 7,
        'accuracy_class': ['I'] * 7,
        'measurement_method': ['GNSS_RTK'] * 7,
        'operator': ['Team_A'] * 7,
        'status': ['Verified'] * 7,
        'remarks': ['Test pyramid'] * 7
    }
    file_1 = create_test_case_excel('case1_valid', models_1, coords_1)
    result_1 = test_shared_pyramids(file_1, expected_pass=True)

    # Case 2: Valid - Segments share MULTIPLE pyramids
    print("\n📋 Case 2: Valid - Segments share multiple pyramids")
    models_2 = {
        'segment_model': [
            'SEGMENT_A1', 'SEGMENT_A1', 'SEGMENT_A1', 'SEGMENT_A1',
            'SEGMENT_B2', 'SEGMENT_B2', 'SEGMENT_B2', 'SEGMENT_B2',
            'SEGMENT_C3', 'SEGMENT_C3', 'SEGMENT_C3'
        ],
        'pyramid_name': [
            'PYR_001_REF', 'PYR_002_SUR', 'PYR_003_CTL', 'PYR_004_MON',  # A1: 4 pyramids
            'PYR_003_CTL', 'PYR_004_MON', 'PYR_005_BND', 'PYR_006_GEO',  # B2: shares 2 with A1
            'PYR_005_BND', 'PYR_006_GEO', 'PYR_007_BEN'                  # C3: shares 2 with B2
        ]
    }
    coords_2 = {
        'pyramid_name': ['PYR_001_REF', 'PYR_002_SUR', 'PYR_003_CTL', 'PYR_004_MON',
                        'PYR_005_BND', 'PYR_006_GEO', 'PYR_007_BEN'],
        'LV95_X': [2679520.05, 2679525.00, 2679530.00, 2679535.00, 2679540.00, 2679545.00, 2679550.00],
        'LV95_Y': [1151703.09, 1151708.00, 1151713.00, 1151718.00, 1151723.00, 1151728.00, 1151733.00],
        'LV95_Z': [500.0, 501.0, 502.0, 503.0, 504.0, 505.0, 506.0],
        'measurement_date': ['2024-01-15'] * 7,
        'accuracy_class': ['I'] * 7,
        'measurement_method': ['GNSS_RTK'] * 7,
        'operator': ['Team_A'] * 7,
        'status': ['Verified'] * 7,
        'remarks': ['Test pyramid'] * 7
    }
    file_2 = create_test_case_excel('case2_multiple', models_2, coords_2)
    result_2 = test_shared_pyramids(file_2, expected_pass=True)

    # Case 3: Invalid - One segment has NO shared pyramids
    print("\n📋 Case 3: Invalid - One segment has no shared pyramids")
    models_3 = {
        'segment_model': [
            'SEGMENT_A1', 'SEGMENT_A1', 'SEGMENT_A1',
            'SEGMENT_B2', 'SEGMENT_B2', 'SEGMENT_B2',
            'SEGMENT_C3', 'SEGMENT_C3', 'SEGMENT_C3'  # C3 will have no shared pyramids
        ],
        'pyramid_name': [
            'PYR_001_REF', 'PYR_002_SUR', 'PYR_003_CTL',  # A1
            'PYR_003_CTL', 'PYR_004_MON', 'PYR_005_BND',  # B2: shares PYR_003_CTL with A1
            'PYR_006_GEO', 'PYR_007_BEN', 'PYR_008_TMP'   # C3: NO shared pyramids
        ]
    }
    coords_3 = {
        'pyramid_name': ['PYR_001_REF', 'PYR_002_SUR', 'PYR_003_CTL', 'PYR_004_MON',
                        'PYR_005_BND', 'PYR_006_GEO', 'PYR_007_BEN', 'PYR_008_TMP'],
        'LV95_X': [2679520.05, 2679525.00, 2679530.00, 2679535.00, 2679540.00, 2679545.00, 2679550.00, 2679555.00],
        'LV95_Y': [1151703.09, 1151708.00, 1151713.00, 1151718.00, 1151723.00, 1151728.00, 1151733.00, 1151738.00],
        'LV95_Z': [500.0, 501.0, 502.0, 503.0, 504.0, 505.0, 506.0, 507.0],
        'measurement_date': ['2024-01-15'] * 8,
        'accuracy_class': ['I'] * 8,
        'measurement_method': ['GNSS_RTK'] * 8,
        'operator': ['Team_A'] * 8,
        'status': ['Verified'] * 8,
        'remarks': ['Test pyramid'] * 8
    }
    file_3 = create_test_case_excel('case3_invalid', models_3, coords_3)
    result_3 = test_shared_pyramids(file_3, expected_pass=False)

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    all_passed = result_1 and result_2 and result_3

    if all_passed:
        print("✅ ALL TEST CASES PASSED")
        return True
    else:
        print("❌ SOME TEST CASES FAILED")
        sys.exit(1)


if __name__ == "__main__":
    run_all_test_cases()
