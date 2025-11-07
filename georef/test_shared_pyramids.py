#!/usr/bin/env python3
"""
Simple test to verify that each segment_model has at least one shared pyramid_name
with another segment_model. Writes report to 'report' sheet in Excel file.
"""

import sys
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook


def test_shared_pyramids():
    """Test that each segment has at least one shared pyramid with another segment."""

    excel_file = Path(__file__).parent / "test_data.xlsx"
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

    print(f"✅ Report written to sheet 'report' in {excel_file}")

    # Validate all segments have sharing
    all_valid = all(segment_has_sharing.values())

    if all_valid:
        print("✅ PASSED: Each segment has at least one shared pyramid!")
        return True
    else:
        missing = [s for s, has in segment_has_sharing.items() if not has]
        print(f"❌ FAILED: Segments without sharing: {missing}")
        sys.exit(1)


if __name__ == "__main__":
    test_shared_pyramids()
