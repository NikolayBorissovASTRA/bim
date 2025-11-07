# Shared Pyramids Test Cases Summary

## Test Script: `test_shared_pyramids_cases.py`

This script validates that each segment_model shares at least one pyramid with another segment.

### Test Cases

#### Case 1: Valid - Each segment shares at least one pyramid ✅
- **File**: `test_data_case1_valid.xlsx`
- **Setup**:
  - SEGMENT_A1: PYR_001_REF, PYR_002_SUR, PYR_003_CTL
  - SEGMENT_B2: PYR_003_CTL, PYR_004_MON, PYR_005_BND
  - SEGMENT_C3: PYR_005_BND, PYR_006_GEO, PYR_007_BEN
- **Sharing**:
  - A1 ∩ B2: PYR_003_CTL (1 pyramid)
  - B2 ∩ C3: PYR_005_BND (1 pyramid)
- **Result**: PASSED - All segments have at least one shared pyramid

#### Case 2: Valid - Segments share MULTIPLE pyramids ✅
- **File**: `test_data_case2_multiple.xlsx`
- **Setup**:
  - SEGMENT_A1: PYR_001_REF, PYR_002_SUR, PYR_003_CTL, PYR_004_MON
  - SEGMENT_B2: PYR_003_CTL, PYR_004_MON, PYR_005_BND, PYR_006_GEO
  - SEGMENT_C3: PYR_005_BND, PYR_006_GEO, PYR_007_BEN
- **Sharing**:
  - A1 ∩ B2: PYR_003_CTL, PYR_004_MON (2 pyramids)
  - B2 ∩ C3: PYR_005_BND, PYR_006_GEO (2 pyramids)
- **Result**: PASSED - All segments share multiple pyramids with neighbors

#### Case 3: Invalid - One segment has NO shared pyramids ❌
- **File**: `test_data_case3_invalid.xlsx`
- **Setup**:
  - SEGMENT_A1: PYR_001_REF, PYR_002_SUR, PYR_003_CTL
  - SEGMENT_B2: PYR_003_CTL, PYR_004_MON, PYR_005_BND
  - SEGMENT_C3: PYR_006_GEO, PYR_007_BEN, PYR_008_TMP (isolated)
- **Sharing**:
  - A1 ∩ B2: PYR_003_CTL (1 pyramid)
  - C3: NO shared pyramids with any segment
- **Result**: FAILED (expected) - SEGMENT_C3 has no shared pyramids

### Report Sheet Format

Each test case creates a 'report' sheet with three sections:

**Section 1: Segment pairs WITH sharing**
- `segment_1`: First segment in the sharing pair
- `segment_2`: Second segment in the sharing pair
- `shared_pyramids`: Comma-separated list of pyramid names shared between the two segments
- `count`: Number of pyramids shared between this specific pair

**Section 2: Segments WITHOUT sharing (isolated segments)**
- `segment_1`: Segment name
- `segment_2`: "NO SHARING"
- `shared_pyramids`: "This segment has no shared pyramids with any other segment"
- `count`: 0

**Section 3: Summary row**
- `segment_1`: "SUMMARY"
- `segment_2`: "X segments total, Y have sharing" (segment-level statistics)
- `shared_pyramids`: "N unique pyramids are shared across M segment pairs" (pyramid-level statistics)
- `count`: Total number of unique pyramids that are shared (across all pairs)

**Example (Case 3 - with isolated segment):**
| segment_1  | segment_2                        | shared_pyramids                                             | count |
|------------|----------------------------------|-------------------------------------------------------------|-------|
| SEGMENT_A1 | SEGMENT_B2                       | PYR_003_CTL                                                 | 1     |
| SEGMENT_C3 | NO SHARING                       | This segment has no shared pyramids with any other segment  | 0     |
| SUMMARY    | 3 segments total, 2 have sharing | 1 unique pyramids are shared across 1 segment pairs         | 1     |

This shows:
- 1 segment pair with sharing (A1 ∩ B2)
- 1 isolated segment (C3) with no sharing
- 1 unique pyramid involved in sharing (PYR_003_CTL)

### Running the Tests

```bash
uv run python test_shared_pyramids_cases.py
```

### Validation Logic

- Each segment must share **at least one** pyramid with another segment
- Multiple shared pyramids between segments are allowed and counted
- The test passes if all segments have sharing, fails if any segment is isolated
