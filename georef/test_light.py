#!/usr/bin/env python3
"""
Test suite for the lightweight IFC4X3_ADD2 pyramid generator.
Verifies core functionality with minimal code.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ifc_light import IFCLight


def test_basic_creation():
    """Test basic IFC file creation with templates."""
    print("\n🧪 Test 1: Basic IFC file creation")

    generator = IFCLight("../templates")
    generator.create_file("Test Project")

    # Verify schema
    schema = getattr(generator.ifc, 'schema_identifier', generator.ifc.schema)
    assert "IFC4X3" in schema, f"Schema should be IFC4X3_ADD2, got {schema}"
    print(f"  ✓ Schema: {schema}")

    # Verify project exists
    projects = generator.ifc.by_type("IfcProject")
    assert len(projects) == 1, "Should have exactly one project"
    assert projects[0].Name == "Test Project"
    print("  ✓ Project created: Test Project")

    # Verify units
    units = generator.ifc.by_type("IfcSIUnit")
    assert len(units) == 4, "Should have 4 units"
    print("  ✓ Units configured: Length, Area, Volume, Angle")

    # Verify CRS
    crs = generator.ifc.by_type("IfcProjectedCRS")
    assert len(crs) == 1, "Should have CRS"
    assert "2056" in crs[0].Name, "Should be Swiss LV95"
    print("  ✓ CRS: Swiss LV95 (EPSG:2056)")

    return True


def test_coordinate_transformation():
    """Test LV95 to local coordinate transformation."""
    print("\n🧪 Test 2: Coordinate transformation")

    generator = IFCLight("../templates")

    # Test transformation
    lv95_coords = (2679520.05, 1151703.09, 447.3)  # Reference point
    local = generator._transform_coordinates(lv95_coords)

    # Should be near origin (reference point)
    assert abs(local[0]) < 0.001, f"X should be ~0, got {local[0]}"
    assert abs(local[1]) < 0.001, f"Y should be ~0, got {local[1]}"
    assert abs(local[2]) < 0.001, f"Z should be ~0, got {local[2]}"
    print(f"  ✓ Reference point transforms to origin: ({local[0]:.3f}, {local[1]:.3f}, {local[2]:.3f})")

    # Test offset point
    lv95_offset = (2679530.05, 1151713.09, 450.3)
    local_offset = generator._transform_coordinates(lv95_offset)
    print(f"  ✓ Offset point: LV95({lv95_offset[0]:.2f}, {lv95_offset[1]:.2f}) → Local({local_offset[0]:.2f}, {local_offset[1]:.2f})")

    return True


def test_pyramid_creation():
    """Test pyramid creation with all features."""
    print("\n🧪 Test 3: Pyramid creation")

    generator = IFCLight("../templates")
    generator.create_file()

    # Add pyramid with naming convention
    pyramid = generator.add_pyramid(
        lv95_coords=(2679525.0, 1151708.0, 500.0),
        element_type="REF",
        sector="S01",
        phase="PL"
    )

    assert pyramid is not None, "Pyramid should be created"
    assert pyramid.Name == "A1_REF_S01_001_PL", f"Name should follow convention, got {pyramid.Name}"
    print(f"  ✓ Pyramid created: {pyramid.Name}")

    # Verify geometry
    assert pyramid.Representation is not None, "Should have representation"
    shapes = pyramid.Representation.Representations
    assert len(shapes) > 0, "Should have shape representations"
    print("  ✓ Geometry: Tessellated face set")

    # Verify it's in spatial structure
    containments = generator.ifc.by_type("IfcRelContainedInSpatialStructure")
    assert len(containments) > 0, "Should have spatial containment"
    contained = any(pyramid in rel.RelatedElements for rel in containments)
    assert contained, "Pyramid should be contained in site"
    print("  ✓ Spatial structure: Contained in site")

    return True


def test_properties():
    """Test ASTRA property sets."""
    print("\n🧪 Test 4: Property sets")

    generator = IFCLight("../templates")
    generator.create_file()

    lv95_coords = (2679530.0, 1151713.0, 502.0)
    pyramid = generator.add_pyramid(
        lv95_coords=lv95_coords,
        element_type="SUR",
        sector="S02"
    )

    # Find property sets
    prop_rels = generator.ifc.by_type("IfcRelDefinesByProperties")
    pyramid_props = [rel for rel in prop_rels if pyramid in rel.RelatedObjects]
    assert len(pyramid_props) > 0, "Pyramid should have properties"

    # Check ASTRA properties
    astra_pset = pyramid_props[0].RelatingPropertyDefinition
    assert astra_pset.Name == "ASTRA_Georeferencing"
    print("  ✓ ASTRA property set attached")

    # Verify property values
    props_dict = {p.Name: p.NominalValue.wrappedValue for p in astra_pset.HasProperties}
    assert abs(props_dict['BP_E'] - lv95_coords[0]) < 0.001, "BP_E should match"
    assert abs(props_dict['BP_N'] - lv95_coords[1]) < 0.001, "BP_N should match"
    assert abs(props_dict['BP_H'] - lv95_coords[2]) < 0.001, "BP_H should match"
    print(f"  ✓ Coordinates: E={props_dict['BP_E']:.2f}, N={props_dict['BP_N']:.2f}, H={props_dict['BP_H']:.2f}")
    print(f"  ✓ EPSG Code: {props_dict['EPSG_Code']}")

    return True


def test_template_pyramids():
    """Test creating pyramids from YAML template."""
    print("\n🧪 Test 5: Template-based pyramid creation")

    generator = IFCLight("../templates")
    generator.create_file()

    # Add pyramids from template
    generator.add_pyramids_from_template()

    pyramids = generator.ifc.by_type("IfcBuildingElementProxy")
    assert len(pyramids) == 3, f"Should have 3 pyramids from template, got {len(pyramids)}"
    print(f"  ✓ Created {len(pyramids)} pyramids from template")

    # Verify names
    names = [p.Name for p in pyramids]
    assert "A1_REF_S01_001_PL" in names
    assert "A1_SUR_S02_001_PL" in names
    assert "A1_CTL_TUN_001_CO" in names

    for name in names:
        print(f"  ✓ {name}")

    return True


def test_pyramid_dimensions():
    """Test that pyramids have correct 1m × 1m × 1m dimensions."""
    print("\n🧪 Test 6: Pyramid dimensions validation")

    generator = IFCLight("../templates")
    generator.create_file()

    # Add a pyramid
    pyramid = generator.add_pyramid(
        lv95_coords=(2679520.05, 1151703.09, 500.0),
        element_type="BEN",
        sector="BR01"
    )

    # Get the tessellated face set
    shape_rep = pyramid.Representation.Representations[0]
    face_set = shape_rep.Items[0]

    # Verify it's a triangulated face set
    assert face_set.is_a("IfcTriangulatedFaceSet"), "Should be triangulated"
    assert face_set.Closed == True, "Mesh should be closed"
    print("  ✓ Closed triangulated mesh")

    # Check vertices
    vertices = face_set.Coordinates.CoordList
    assert len(vertices) == 5, f"Should have 5 vertices, got {len(vertices)}"

    # Verify dimensions (apex at origin, base at -1m)
    apex = vertices[0]
    assert apex == (0.0, 0.0, 0.0), f"Apex should be at origin, got {apex}"

    # Check base vertices are at z=-1 and form 1m × 1m square
    for i in range(1, 5):
        assert abs(vertices[i][2] - (-1.0)) < 0.001, f"Base vertex {i} should be at z=-1"
        assert abs(vertices[i][0]) == 0.5, f"Base vertex {i} X should be ±0.5"
        assert abs(vertices[i][1]) == 0.5, f"Base vertex {i} Y should be ±0.5"

    print("  ✓ Dimensions: 1m × 1m × 1m")
    print("  ✓ Apex at (0,0,0), base at z=-1m")

    return True


def test_full_workflow():
    """Test complete workflow from creation to saving."""
    print("\n🧪 Test 7: Full workflow test")

    # Clean up any existing file
    output_file = "../output/test_light.ifc"
    if os.path.exists(output_file):
        os.remove(output_file)

    # Create and populate
    generator = IFCLight("../templates")
    generator.create_file("Swiss Highway A1")

    # Add multiple pyramids
    pyramids_added = []
    test_data = [
        ((2679520.05, 1151703.09, 500.0), "REF", "S01", "PL"),
        ((2679530.00, 1151713.00, 502.0), "SUR", "S02", "PL"),
        ((2679515.00, 1151698.00, 498.0), "CTL", "TUN", "CO"),
        ((2679525.00, 1151708.00, 501.0), "MON", "BR01", "OP"),
    ]

    for coords, typ, sector, phase in test_data:
        pyramid = generator.add_pyramid(
            lv95_coords=coords,
            element_type=typ,
            sector=sector,
            phase=phase
        )
        pyramids_added.append(pyramid)

    print(f"  ✓ Added {len(pyramids_added)} pyramids")

    # Save file
    generator.save(output_file)
    assert os.path.exists(output_file), "File should be saved"
    print(f"  ✓ Saved to {output_file}")

    # Reload and verify
    loaded = ifcopenshell.open(output_file)
    schema = getattr(loaded, 'schema_identifier', loaded.schema)
    assert "IFC4X3" in schema, f"Schema should contain IFC4X3, got {schema}"
    loaded_pyramids = loaded.by_type("IfcBuildingElementProxy")
    assert len(loaded_pyramids) == 4, f"Should have 4 pyramids, got {len(loaded_pyramids)}"
    print(f"  ✓ Reloaded: {len(loaded_pyramids)} pyramids")

    # Verify all have property sets
    prop_rels = loaded.by_type("IfcRelDefinesByProperties")
    for pyramid in loaded_pyramids:
        has_props = any(pyramid in rel.RelatedObjects for rel in prop_rels)
        assert has_props, f"{pyramid.Name} should have properties"

    print("  ✓ All pyramids have ASTRA properties")

    # File size check
    file_size = os.path.getsize(output_file)
    print(f"  ✓ File size: {file_size:,} bytes")

    return True


def run_all_tests():
    """Run all test cases and report results."""
    print("=" * 60)
    print("🚀 IFC Light Version Test Suite")
    print("=" * 60)

    tests = [
        ("Basic Creation", test_basic_creation),
        ("Coordinate Transformation", test_coordinate_transformation),
        ("Pyramid Creation", test_pyramid_creation),
        ("Property Sets", test_properties),
        ("Template Pyramids", test_template_pyramids),
        ("Pyramid Dimensions", test_pyramid_dimensions),
        ("Full Workflow", test_full_workflow),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, "✅ PASSED"))
        except AssertionError as e:
            results.append((name, f"❌ FAILED: {e}"))
        except Exception as e:
            results.append((name, f"⚠️ ERROR: {e}"))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if "PASSED" in result)
    total = len(results)

    for name, result in results:
        print(f"{name:30} {result}")

    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The lightweight version is working correctly.")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the implementation.")

    return passed == total


if __name__ == "__main__":
    # Ensure output directory exists
    Path("../output").mkdir(exist_ok=True)

    # Run tests
    success = run_all_tests()
    exit(0 if success else 1)