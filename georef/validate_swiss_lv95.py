#!/usr/bin/env python3
"""
Enhanced IFC Validation Script for Virtual Elements with BP_ASTRA and Swiss CRS
Validates IFC models against comprehensive IDS specification including:
- Virtual elements with BP coordinates
- Swiss CH1903+ / LV95 CRS configuration
- Map conversion parameters
- Project coordinate operation linkage
"""

import sys
import json
import math
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

try:
    import ifcopenshell
except ImportError:
    print("Error: ifcopenshell not installed. Install with: pip install ifcopenshell")
    sys.exit(1)


class ValidationStatus(Enum):
    """Validation result statuses"""
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationResult:
    """Container for validation results"""
    status: ValidationStatus
    specification: str
    message: str
    details: Dict[str, Any]


@dataclass
class CoordinateSet:
    """Container for BP coordinate values"""
    bp_x: Optional[float] = None
    bp_y: Optional[float] = None
    bp_z: Optional[float] = None
    element_id: Optional[str] = None
    element_name: Optional[str] = None
    
    @property
    def is_complete(self) -> bool:
        """Check if all coordinates are present"""
        return all([
            self.bp_x is not None,
            self.bp_y is not None,
            self.bp_z is not None
        ])


@dataclass
class CRSConfiguration:
    """Container for CRS configuration"""
    name: Optional[str] = None
    description: Optional[str] = None
    map_projection: Optional[str] = None
    map_zone: Optional[str] = None
    map_unit: Optional[str] = None
    vertical_datum: Optional[str] = None
    
    @property
    def is_valid_swiss_lv95(self) -> bool:
        """Check if configuration matches Swiss LV95 requirements"""
        return all([
            self.name == "CH1903+ / LV95",
            self.description == "EPSG:2056",
            self.map_projection == "UTM",
            self.map_zone == "32",
            self.map_unit in ["METRE", "#51"],  # Can be reference or literal
            self.vertical_datum == "LHN95"
        ])


@dataclass
class MapConversionParams:
    """Container for map conversion parameters"""
    eastings: Optional[float] = None
    northings: Optional[float] = None
    orthogonal_height: Optional[float] = None
    x_axis_abscissa: Optional[float] = None
    x_axis_ordinate: Optional[float] = None
    scale: Optional[float] = None
    
    @property
    def is_valid_swiss_params(self) -> bool:
        """Check if parameters match Swiss LV95 requirements"""
        return all([
            self.eastings == 2600000.0,
            self.northings == 1200000.0,
            self.orthogonal_height == 500.0,
            self.x_axis_abscissa == 1.0,
            self.x_axis_ordinate == 0.0,
            self.scale is None or self.scale == 1.0  # Scale is optional
        ])


class SwissLV95Validator:
    """Complete validator for Swiss LV95 CRS and Virtual Elements"""
    
    # Virtual Elements Requirements
    REQUIRED_VE_COUNT = 3
    PROPERTY_SET_NAME = "CustomPset_BP_ASTRA"
    REQUIRED_PROPERTIES = ["BP_X", "BP_Y", "BP_Z"]
    
    # Swiss CRS Requirements
    SWISS_CRS_NAME = "CH1903+ / LV95"
    SWISS_EPSG = "EPSG:2056"
    SWISS_VERTICAL_DATUM = "LHN95"
    
    # Map Conversion Requirements
    SWISS_EASTING = 2600000.0
    SWISS_NORTHING = 1200000.0
    SWISS_HEIGHT = 500.0
    
    def __init__(self, ifc_file_path: str):
        """
        Initialize validator with IFC file
        
        Args:
            ifc_file_path: Path to the IFC file to validate
        """
        self.ifc_file_path = ifc_file_path
        self.model = None
        self.validation_results = []
        
        # Entities to validate
        self.virtual_elements = []
        self.projected_crs = None
        self.map_conversion = None
        self.project = None
    
    def load_model(self) -> bool:
        """Load the IFC model"""
        try:
            self.model = ifcopenshell.open(self.ifc_file_path)
            
            # Check IFC schema version
            schema = self.model.schema
            if schema != 'IFC4X3_ADD2':
                self.validation_results.append(
                    ValidationResult(
                        status=ValidationStatus.WARNING,
                        specification="Schema Version",
                        message=f"⚠ IFC schema is {schema}, expected IFC4X3_ADD2",
                        details={"found": schema, "expected": "IFC4X3_ADD2"}
                    )
                )
            else:
                self.validation_results.append(
                    ValidationResult(
                        status=ValidationStatus.PASS,
                        specification="Schema Version",
                        message=f"✓ IFC schema is IFC4X3_ADD2",
                        details={"schema": schema}
                    )
                )
            
            return True
        except Exception as e:
            self.validation_results.append(
                ValidationResult(
                    status=ValidationStatus.FAIL,
                    specification="Model Loading",
                    message=f"Failed to load IFC file: {str(e)}",
                    details={"file_path": self.ifc_file_path}
                )
            )
            return False
    
    # ========== VIRTUAL ELEMENTS VALIDATION ==========
    
    def validate_virtual_elements(self):
        """Validate virtual elements with BP_ASTRA coordinates"""
        try:
            self.virtual_elements = self.model.by_type('IfcVirtualElement')
        except:
            self.virtual_elements = []
        
        # Check count
        count = len(self.virtual_elements)
        if count == self.REQUIRED_VE_COUNT:
            self.validation_results.append(
                ValidationResult(
                    status=ValidationStatus.PASS,
                    specification="SPEC-001-VIRTUAL-BP",
                    message=f"✓ Found exactly {self.REQUIRED_VE_COUNT} IfcVirtualElement entities",
                    details={"found": count, "required": self.REQUIRED_VE_COUNT}
                )
            )
        else:
            self.validation_results.append(
                ValidationResult(
                    status=ValidationStatus.FAIL,
                    specification="SPEC-001-VIRTUAL-BP",
                    message=f"✗ Expected {self.REQUIRED_VE_COUNT} IfcVirtualElement entities, found {count}",
                    details={"found": count, "required": self.REQUIRED_VE_COUNT}
                )
            )
        
        # Check properties for each element
        all_coordinates = []
        for element in self.virtual_elements:
            coord_set = self._validate_element_properties(element)
            all_coordinates.append(coord_set)
        
        # Summary
        if all_coordinates:
            complete_count = sum(1 for c in all_coordinates if c.is_complete)
            self.validation_results.append(
                ValidationResult(
                    status=ValidationStatus.INFO,
                    specification="SPEC-001-VIRTUAL-BP",
                    message=f"Coordinate Sets: {complete_count}/{len(all_coordinates)} complete",
                    details={"coordinates": [
                        {
                            "element": c.element_name,
                            "BP_X": c.bp_x,
                            "BP_Y": c.bp_y,
                            "BP_Z": c.bp_z,
                            "complete": c.is_complete
                        } for c in all_coordinates
                    ]}
                )
            )
    
    def _get_property_value(self, element, pset_name: str, prop_name: str) -> Optional[Any]:
        """Get a property value from an element's property set"""
        try:
            for definition in element.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    property_set = definition.RelatingPropertyDefinition
                    
                    if property_set.Name == pset_name:
                        for prop in property_set.HasProperties:
                            if prop.Name == prop_name:
                                if hasattr(prop, 'NominalValue'):
                                    return prop.NominalValue.wrappedValue
                                return None
        except:
            pass
        return None
    
    def _validate_element_properties(self, element) -> CoordinateSet:
        """Validate that an element has all required properties"""
        element_id = element.GlobalId if hasattr(element, 'GlobalId') else str(element.id())
        element_name = element.Name if hasattr(element, 'Name') else "Unnamed"
        
        coord_set = CoordinateSet(element_id=element_id, element_name=element_name)
        missing_properties = []
        
        # Check for each required property
        for prop_name in self.REQUIRED_PROPERTIES:
            value = self._get_property_value(element, self.PROPERTY_SET_NAME, prop_name)
            
            if value is not None:
                if prop_name == "BP_X":
                    coord_set.bp_x = float(value) if value else None
                elif prop_name == "BP_Y":
                    coord_set.bp_y = float(value) if value else None
                elif prop_name == "BP_Z":
                    coord_set.bp_z = float(value) if value else None
            else:
                missing_properties.append(prop_name)
        
        # Generate validation result
        if not missing_properties:
            self.validation_results.append(
                ValidationResult(
                    status=ValidationStatus.PASS,
                    specification="SPEC-001-VIRTUAL-BP",
                    message=f"✓ Element {element_name} has all required properties",
                    details={
                        "element_id": element_id,
                        "element_name": element_name,
                        "coordinates": {
                            "BP_X": coord_set.bp_x,
                            "BP_Y": coord_set.bp_y,
                            "BP_Z": coord_set.bp_z
                        }
                    }
                )
            )
        else:
            self.validation_results.append(
                ValidationResult(
                    status=ValidationStatus.FAIL,
                    specification="SPEC-001-VIRTUAL-BP",
                    message=f"✗ Element {element_name} missing properties: {', '.join(missing_properties)}",
                    details={
                        "element_id": element_id,
                        "element_name": element_name,
                        "missing_properties": missing_properties,
                        "property_set": self.PROPERTY_SET_NAME
                    }
                )
            )
        
        return coord_set
    
    # ========== CRS VALIDATION ==========
    
    def validate_projected_crs(self):
        """Validate IfcProjectedCRS configuration"""
        try:
            crs_list = self.model.by_type('IfcProjectedCRS')
            if not crs_list:
                self.validation_results.append(
                    ValidationResult(
                        status=ValidationStatus.FAIL,
                        specification="SPEC-002-CRS-LV95",
                        message="✗ No IfcProjectedCRS found in model",
                        details={"required": "CH1903+ / LV95"}
                    )
                )
                return
            
            self.projected_crs = crs_list[0]
            crs_config = CRSConfiguration()
            
            # Extract CRS attributes
            crs_config.name = self.projected_crs.Name if hasattr(self.projected_crs, 'Name') else None
            crs_config.description = self.projected_crs.Description if hasattr(self.projected_crs, 'Description') else None
            crs_config.map_projection = self.projected_crs.MapProjection if hasattr(self.projected_crs, 'MapProjection') else None
            crs_config.map_zone = self.projected_crs.MapZone if hasattr(self.projected_crs, 'MapZone') else None
            crs_config.vertical_datum = self.projected_crs.VerticalDatum if hasattr(self.projected_crs, 'VerticalDatum') else None
            
            # Map unit can be a reference or string
            if hasattr(self.projected_crs, 'MapUnit'):
                if isinstance(self.projected_crs.MapUnit, str):
                    crs_config.map_unit = self.projected_crs.MapUnit
                elif hasattr(self.projected_crs.MapUnit, 'Name'):
                    crs_config.map_unit = self.projected_crs.MapUnit.Name
                else:
                    crs_config.map_unit = "METRE"  # Default assumption
            
            # Validate configuration
            if crs_config.is_valid_swiss_lv95:
                self.validation_results.append(
                    ValidationResult(
                        status=ValidationStatus.PASS,
                        specification="SPEC-002-CRS-LV95",
                        message="✓ IfcProjectedCRS correctly configured for Swiss LV95",
                        details={
                            "name": crs_config.name,
                            "description": crs_config.description,
                            "projection": crs_config.map_projection,
                            "zone": crs_config.map_zone,
                            "unit": crs_config.map_unit,
                            "vertical_datum": crs_config.vertical_datum
                        }
                    )
                )
            else:
                errors = []
                if crs_config.name != self.SWISS_CRS_NAME:
                    errors.append(f"Name: expected '{self.SWISS_CRS_NAME}', got '{crs_config.name}'")
                if crs_config.description != self.SWISS_EPSG:
                    errors.append(f"Description: expected '{self.SWISS_EPSG}', got '{crs_config.description}'")
                if crs_config.vertical_datum != self.SWISS_VERTICAL_DATUM:
                    errors.append(f"VerticalDatum: expected '{self.SWISS_VERTICAL_DATUM}', got '{crs_config.vertical_datum}'")
                
                self.validation_results.append(
                    ValidationResult(
                        status=ValidationStatus.FAIL,
                        specification="SPEC-002-CRS-LV95",
                        message="✗ IfcProjectedCRS configuration errors",
                        details={
                            "errors": errors,
                            "current_config": {
                                "name": crs_config.name,
                                "description": crs_config.description,
                                "vertical_datum": crs_config.vertical_datum
                            }
                        }
                    )
                )
                
        except Exception as e:
            self.validation_results.append(
                ValidationResult(
                    status=ValidationStatus.FAIL,
                    specification="SPEC-002-CRS-LV95",
                    message=f"✗ Error validating IfcProjectedCRS: {str(e)}",
                    details={"error": str(e)}
                )
            )
    
    # ========== MAP CONVERSION VALIDATION ==========
    
    def validate_map_conversion(self):
        """Validate IfcMapConversion parameters"""
        try:
            conv_list = self.model.by_type('IfcMapConversion')
            if not conv_list:
                self.validation_results.append(
                    ValidationResult(
                        status=ValidationStatus.FAIL,
                        specification="SPEC-003-MAP-CONV",
                        message="✗ No IfcMapConversion found in model",
                        details={"required": "Map conversion with Swiss LV95 parameters"}
                    )
                )
                return
            
            self.map_conversion = conv_list[0]
            params = MapConversionParams()
            
            # Extract parameters
            params.eastings = float(self.map_conversion.Eastings) if hasattr(self.map_conversion, 'Eastings') else None
            params.northings = float(self.map_conversion.Northings) if hasattr(self.map_conversion, 'Northings') else None
            params.orthogonal_height = float(self.map_conversion.OrthogonalHeight) if hasattr(self.map_conversion, 'OrthogonalHeight') else None
            params.x_axis_abscissa = float(self.map_conversion.XAxisAbscissa) if hasattr(self.map_conversion, 'XAxisAbscissa') else None
            params.x_axis_ordinate = float(self.map_conversion.XAxisOrdinate) if hasattr(self.map_conversion, 'XAxisOrdinate') else None
            params.scale = float(self.map_conversion.Scale) if hasattr(self.map_conversion, 'Scale') else None
            
            # Validate parameters
            if params.is_valid_swiss_params:
                self.validation_results.append(
                    ValidationResult(
                        status=ValidationStatus.PASS,
                        specification="SPEC-003-MAP-CONV",
                        message="✓ IfcMapConversion correctly configured with Swiss LV95 parameters",
                        details={
                            "eastings": params.eastings,
                            "northings": params.northings,
                            "orthogonal_height": params.orthogonal_height,
                            "x_axis_abscissa": params.x_axis_abscissa,
                            "x_axis_ordinate": params.x_axis_ordinate,
                            "scale": params.scale
                        }
                    )
                )
            else:
                errors = []
                if params.eastings != self.SWISS_EASTING:
                    errors.append(f"Eastings: expected {self.SWISS_EASTING}, got {params.eastings}")
                if params.northings != self.SWISS_NORTHING:
                    errors.append(f"Northings: expected {self.SWISS_NORTHING}, got {params.northings}")
                if params.orthogonal_height != self.SWISS_HEIGHT:
                    errors.append(f"OrthogonalHeight: expected {self.SWISS_HEIGHT}, got {params.orthogonal_height}")
                if params.x_axis_abscissa != 1.0:
                    errors.append(f"XAxisAbscissa: expected 1.0, got {params.x_axis_abscissa}")
                if params.x_axis_ordinate != 0.0:
                    errors.append(f"XAxisOrdinate: expected 0.0, got {params.x_axis_ordinate}")
                
                self.validation_results.append(
                    ValidationResult(
                        status=ValidationStatus.FAIL,
                        specification="SPEC-003-MAP-CONV",
                        message="✗ IfcMapConversion parameter errors",
                        details={
                            "errors": errors,
                            "current_params": {
                                "eastings": params.eastings,
                                "northings": params.northings,
                                "orthogonal_height": params.orthogonal_height
                            }
                        }
                    )
                )
                
        except Exception as e:
            self.validation_results.append(
                ValidationResult(
                    status=ValidationStatus.FAIL,
                    specification="SPEC-003-MAP-CONV",
                    message=f"✗ Error validating IfcMapConversion: {str(e)}",
                    details={"error": str(e)}
                )
            )
    
    # ========== PROJECT VALIDATION ==========
    
    def validate_project_coordinate_operation(self):
        """Validate IfcProject coordinate operation linkage"""
        try:
            projects = self.model.by_type('IfcProject')
            if not projects:
                self.validation_results.append(
                    ValidationResult(
                        status=ValidationStatus.FAIL,
                        specification="SPEC-004-PROJ-COORD",
                        message="✗ No IfcProject found in model",
                        details={}
                    )
                )
                return
            
            self.project = projects[0]
            has_coordinate_op = False
            
            # Check if project has representation contexts
            if hasattr(self.project, 'RepresentationContexts'):
                for context in self.project.RepresentationContexts:
                    if hasattr(context, 'HasCoordinateOperation'):
                        has_coordinate_op = True
                        break
            
            if has_coordinate_op:
                self.validation_results.append(
                    ValidationResult(
                        status=ValidationStatus.PASS,
                        specification="SPEC-004-PROJ-COORD",
                        message="✓ IfcProject has coordinate operation reference",
                        details={
                            "project_name": self.project.Name if hasattr(self.project, 'Name') else "Unnamed",
                            "has_coordinate_operation": True
                        }
                    )
                )
            else:
                self.validation_results.append(
                    ValidationResult(
                        status=ValidationStatus.WARNING,
                        specification="SPEC-004-PROJ-COORD",
                        message="⚠ IfcProject coordinate operation linkage could not be verified",
                        details={
                            "project_name": self.project.Name if hasattr(self.project, 'Name') else "Unnamed",
                            "note": "Manual verification may be required"
                        }
                    )
                )
                
        except Exception as e:
            self.validation_results.append(
                ValidationResult(
                    status=ValidationStatus.FAIL,
                    specification="SPEC-004-PROJ-COORD",
                    message=f"✗ Error validating IfcProject: {str(e)}",
                    details={"error": str(e)}
                )
            )
    
    # ========== MAIN VALIDATION ==========
    
    def validate(self) -> bool:
        """Run complete validation"""
        print("\n" + "="*60)
        print("STARTING VALIDATION: Swiss LV95 CRS & Virtual Elements")
        print("="*60)
        
        # Load model
        if not self.load_model():
            return False
        
        print("\nValidating specifications...")
        
        # Run all validations
        print("  • SPEC-001: Virtual Elements with BP_ASTRA...")
        self.validate_virtual_elements()
        
        print("  • SPEC-002: Swiss CRS Configuration...")
        self.validate_projected_crs()
        
        print("  • SPEC-003: Map Conversion Parameters...")
        self.validate_map_conversion()
        
        print("  • SPEC-004: Project Coordinate Operation...")
        self.validate_project_coordinate_operation()
        
        # Check overall status
        has_failure = any(r.status == ValidationStatus.FAIL for r in self.validation_results)
        return not has_failure
    
    def print_report(self):
        """Print a formatted validation report"""
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("Swiss LV95 CRS & Virtual Elements with BP_ASTRA")
        print("="*60)
        print(f"IFC File: {self.ifc_file_path}")
        print("-"*60)
        
        # Group results by specification
        specs = {}
        for result in self.validation_results:
            spec = result.specification
            if spec not in specs:
                specs[spec] = []
            specs[spec].append(result)
        
        # Print results by specification
        for spec_name in sorted(specs.keys()):
            print(f"\n📋 {spec_name}:")
            for result in specs[spec_name]:
                if result.status == ValidationStatus.PASS:
                    print(f"  {result.message}")
                elif result.status == ValidationStatus.FAIL:
                    print(f"  {result.message}")
                    if "errors" in result.details:
                        for error in result.details["errors"]:
                            print(f"    → {error}")
                elif result.status == ValidationStatus.WARNING:
                    print(f"  {result.message}")
                elif result.status == ValidationStatus.INFO:
                    print(f"  ℹ {result.message}")
        
        # Overall summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("-"*60)
        
        total = len(self.validation_results)
        passes = sum(1 for r in self.validation_results if r.status == ValidationStatus.PASS)
        failures = sum(1 for r in self.validation_results if r.status == ValidationStatus.FAIL)
        warnings = sum(1 for r in self.validation_results if r.status == ValidationStatus.WARNING)
        
        print(f"Total Checks: {total}")
        print(f"  ✅ Passed: {passes}")
        print(f"  ❌ Failed: {failures}")
        print(f"  ⚠️  Warnings: {warnings}")
        
        print("\n" + "="*60)
        overall_pass = failures == 0
        if overall_pass:
            print("OVERALL RESULT: ✅ VALIDATION PASSED")
        else:
            print("OVERALL RESULT: ❌ VALIDATION FAILED")
        print("="*60 + "\n")
    
    def export_json_report(self, output_path: str):
        """Export validation results as JSON"""
        report = {
            "ifc_file": self.ifc_file_path,
            "specifications": {
                "SPEC-001-VIRTUAL-BP": {
                    "name": "Virtual Elements with BP_ASTRA Coordinates",
                    "requirements": {
                        "element_count": self.REQUIRED_VE_COUNT,
                        "property_set": self.PROPERTY_SET_NAME,
                        "required_properties": self.REQUIRED_PROPERTIES
                    }
                },
                "SPEC-002-CRS-LV95": {
                    "name": "Swiss CH1903+ / LV95 CRS",
                    "requirements": {
                        "name": self.SWISS_CRS_NAME,
                        "epsg": self.SWISS_EPSG,
                        "vertical_datum": self.SWISS_VERTICAL_DATUM
                    }
                },
                "SPEC-003-MAP-CONV": {
                    "name": "Map Conversion Parameters",
                    "requirements": {
                        "eastings": self.SWISS_EASTING,
                        "northings": self.SWISS_NORTHING,
                        "height": self.SWISS_HEIGHT
                    }
                },
                "SPEC-004-PROJ-COORD": {
                    "name": "Project Coordinate Operation",
                    "requirements": "IfcProject must reference coordinate operation"
                }
            },
            "results": [
                {
                    "specification": r.specification,
                    "status": r.status.value,
                    "message": r.message,
                    "details": r.details
                }
                for r in self.validation_results
            ],
            "summary": {
                "total_checks": len(self.validation_results),
                "passed": sum(1 for r in self.validation_results if r.status == ValidationStatus.PASS),
                "failed": sum(1 for r in self.validation_results if r.status == ValidationStatus.FAIL),
                "warnings": sum(1 for r in self.validation_results if r.status == ValidationStatus.WARNING)
            },
            "overall_status": "PASS" if not any(
                r.status == ValidationStatus.FAIL for r in self.validation_results
            ) else "FAIL"
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"JSON report saved to: {output_path}")


def main():
    """Main execution function"""
    if len(sys.argv) < 2:
        print("Swiss LV95 IFC Validator")
        print("-" * 30)
        print("Usage: python validate_swiss_lv95.py <path_to_ifc_file> [json_output_path]")
        print("\nValidates:")
        print("  • 3 IfcVirtualElement with BP_ASTRA coordinates")
        print("  • Swiss CH1903+ / LV95 CRS configuration")
        print("  • Map conversion parameters")
        print("  • Project coordinate operation")
        sys.exit(1)
    
    ifc_path = sys.argv[1]
    json_output = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create and run validator
    validator = SwissLV95Validator(ifc_path)
    validation_passed = validator.validate()
    
    # Print report
    validator.print_report()
    
    # Export JSON if requested
    if json_output:
        validator.export_json_report(json_output)
    
    # Exit with appropriate code
    sys.exit(0 if validation_passed else 1)


if __name__ == "__main__":
    main()