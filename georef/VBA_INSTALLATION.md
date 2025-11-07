# VBA Shared Pyramids Validator - Installation Guide

## Overview

This VBA script provides the same functionality as the Python implementation (`test_shared_pyramids.py`) but runs directly inside Excel without requiring Python.

## Features

- ✅ Validates that each segment shares at least one pyramid with another segment
- ✅ Generates report in 'report' sheet with same format as Python version
- ✅ Shows segment pairs with sharing
- ✅ Highlights isolated segments (with NO sharing) in red
- ✅ Provides summary statistics
- ✅ Color-coded visual feedback

## Installation Steps

### 1. Enable Developer Tab in Excel

**For Excel on Windows:**
1. Click `File` → `Options`
2. Click `Customize Ribbon`
3. Check `Developer` in the right panel
4. Click `OK`

**For Excel on Mac:**
1. Click `Excel` → `Preferences`
2. Click `Ribbon & Toolbar`
3. In the `Customize the Ribbon` section, check `Developer`
4. Click `Save`

### 2. Open VBA Editor

1. Open your Excel file (e.g., `test_data.xlsx`)
2. Press `Alt + F11` (Windows) or `Fn + Option + F11` (Mac)
3. The VBA Editor window will open

### 3. Insert the VBA Code

1. In the VBA Editor, click `Insert` → `Module`
2. A new module window will appear
3. Open the file `SharedPyramidsValidator.vba` in a text editor
4. Copy all the code
5. Paste it into the module window

### 4. Save the Excel File with Macros

1. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac)
2. If prompted, save as **Excel Macro-Enabled Workbook (*.xlsm)**
3. Choose a filename (e.g., `test_data.xlsm`)

## Usage

### Running the Validation

**Method 1: Using Macros Dialog**
1. Press `Alt + F8` (Windows) or `Fn + Option + F8` (Mac)
2. Select `ValidateSharedPyramids` from the list
3. Click `Run`

**Method 2: From VBA Editor**
1. Press `Alt + F11` to open VBA Editor
2. Place cursor anywhere in the `ValidateSharedPyramids` subroutine
3. Press `F5` or click the ▶ Run button

**Method 3: Add a Button (Recommended)**
1. Go to `Developer` tab
2. Click `Insert` → `Button (Form Control)`
3. Draw a button on your worksheet
4. In the dialog, select `ValidateSharedPyramids`
5. Click `OK`
6. Right-click the button → `Edit Text` → Type "Validate Shared Pyramids"
7. Now you can click the button to run validation

### Understanding the Results

The script will:
1. Read data from the `models` sheet
2. Create/replace the `report` sheet
3. Show a message box with validation result

**Success Message:**
```
✓ PASSED: Each segment has at least one shared pyramid!

Report written to 'report' sheet
```

**Failure Message:**
```
✗ FAILED: X segment(s) have no shared pyramids!

See 'report' sheet for details (isolated segments highlighted in red)
```

## Report Format

The `report` sheet contains three sections:

### Section 1: Segment Pairs with Sharing
| segment_1  | segment_2  | shared_pyramids           | count |
|------------|------------|---------------------------|-------|
| SEGMENT_A1 | SEGMENT_B2 | PYR_003_CTL, PYR_004_MON  | 2     |

### Section 2: Isolated Segments (highlighted in red)
| segment_1  | segment_2  | shared_pyramids                                    | count |
|------------|------------|----------------------------------------------------|-------|
| SEGMENT_C3 | NO SHARING | This segment has no shared pyramids with any other segment | 0     |

### Section 3: Summary (highlighted in blue)
| segment_1 | segment_2                     | shared_pyramids                                  | count |
|-----------|-------------------------------|--------------------------------------------------|-------|
| SUMMARY   | 3 segments total, 3 have sharing | 4 unique pyramids are shared across 2 segment pairs | 4     |

## Requirements

- Excel file must have a sheet named `models`
- The `models` sheet must have columns:
  - Column A: `segment_model`
  - Column B: `pyramid_name`
- Header row should be in row 1

## Troubleshooting

### Macro Security Warning
If you see a security warning when opening the file:
1. Click `Enable Content` or `Enable Macros`
2. Or adjust Trust Center settings:
   - `File` → `Options` → `Trust Center` → `Trust Center Settings`
   - Select `Macro Settings`
   - Choose `Enable all macros` (for development) or add file location to trusted locations

### "Sheet 'models' not found" Error
- Ensure your Excel file has a sheet named exactly `models` (case-sensitive)
- Check that data starts from row 2 (row 1 is header)

### Script Runs but No Report Generated
- Check that the `models` sheet has data
- Ensure columns A and B contain segment_model and pyramid_name respectively

## Comparison with Python Version

| Feature | Python | VBA |
|---------|--------|-----|
| Same validation logic | ✅ | ✅ |
| Same report format | ✅ | ✅ |
| Shows isolated segments | ✅ | ✅ |
| Color highlighting | ❌ | ✅ (Red for isolated, blue for summary) |
| Requires installation | ✅ Python + packages | ❌ Built into Excel |
| Cross-platform | ✅ | ⚠️ (Excel required) |

## Advantages of VBA Version

1. **No external dependencies** - Works directly in Excel
2. **Visual feedback** - Color-coded report (red for issues, blue for summary)
3. **Interactive** - Button-based execution
4. **Immediate results** - Opens report sheet automatically
5. **User-friendly** - Message boxes with clear pass/fail status

## Testing

Test the VBA script with the provided test cases:
1. Use `test_data_case1_valid.xlsx` - Should pass ✅
2. Use `test_data_case2_multiple.xlsx` - Should pass ✅
3. Use `test_data_case3_invalid.xlsx` - Should fail ❌ (SEGMENT_C3 isolated)

## License

This script is part of the IFC Light Version project and follows the same licensing terms.
