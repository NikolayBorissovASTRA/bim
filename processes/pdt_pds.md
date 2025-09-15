Product Data Templates (PDTs) and Data Sheets for BIM Infrastructure Assets (IFC 4.3)

Introduction to PDTs, PDSs, and IFC 4.3 Infrastructure

In Building Information Modeling (BIM), a Product Data Template (PDT) is a structured definition of all relevant data fields (properties, attributes, etc.) for a type of product or asset. It serves as a schema or template that specifies what information should be captured for that asset type ￼. A Product Data Sheet (PDS) is an instance of a PDT – essentially a filled-out template containing the actual values for a specific product or asset. Using PDTs/PDSs ensures that asset data is consistent, machine-readable, and standardized across projects ￼ ￼.

The Industry Foundation Classes (IFC) schema (especially IFC 4.3, which is tailored for infrastructure) provides an open standard to represent such assets and their data. IFC 4.3 introduced robust support for civil infrastructure domains like roads, bridges, tunnels, railways, and ports ￼ ￼. It defines objects (e.g. physical elements like IfcBridge, IfcTunnel), their inherent attributes (e.g. identification, type, geometry), standard properties (via property sets), and relationships (linking objects to other objects, classifications, etc.) ￼. This allows capturing not just 3D geometry but also rich semantic information about infrastructure assets over their lifecycle (design, construction, maintenance).

Switzerland’s ASTRA (Federal Roads Office), as a key stakeholder in national infrastructure, emphasizes open standards for data. In its BIM strategy, ASTRA highlights using documented data concepts like IFC and even RDF (semantic web technology) to manage infrastructure asset information ￼. This aligns with international best practices where IFC is combined with data dictionaries and linked data to achieve interoperability and longevity of data ￼ ￼. In Europe, for example, new standards (EN ISO 23386/23387 and EN 17549-2) formalize how data templates and IFC-based exchanges work together ￼ ￼ – underscoring the importance of structured data sheets for assets.

Below, we present a systematic approach and examples for defining infrastructure asset PDTs and PDSs (for assets like bridges, tunnels, road elements, and drainage systems) using the IFC schema. The data is shown in both human- and machine-readable formats (YAML/JSON for readability, and a brief look at RDF for linked data), demonstrating how one can specify asset data templates and fill them with instance data.

Structure of a Product Data Template in IFC

Each infrastructure asset can be described in terms of:
	•	Identification and Description – a unique ID (e.g. GUID), name, and optional description/comment. In IFC, every object has a GlobalId and human-readable Name or Description.
	•	Attributes – Intrinsic attributes defined by the IFC schema for that entity. For example, an IfcBridge entity may have a PredefinedType (an enumeration of bridge types) among its attributes. These define high-level characteristics set by the schema (e.g. an IfcTunnel might distinguish road vs. rail tunnels via a type enum).
	•	Properties – Specific characteristics grouped into property sets. These are usually domain-specific. IFC provides standard property sets and allows custom ones. For instance, a bridge might use a “Bridge Common” property set including properties like structural type, load capacity, etc. (e.g. StructureIndicator – “the type of bridge structure (composite, coated, homogeneous, etc.)” is a defined property in the IFC4.3 Bridge Common set ￼). Each property has a name, value (which could be a number, text, boolean, enumerated value, etc.), and unit or data type.
	•	Quantities – Measurable quantities (lengths, areas, volumes, counts) relevant to the asset. These can be captured in IFC via quantity sets (QTOs). For example, a tunnel might have a length, a bridge a total span length or deck area, a pipe a diameter and length, etc. Quantities complement the descriptive properties with numeric metrics.
	•	Metadata – Any additional metadata or classifications. This can include links to external classification systems (e.g. an ASTRA or VSS code for asset type), references to standards, or lifecycle information (like construction year, inspection dates). In IFC, one might use IfcClassificationReference or IfcExternalReference to link an object to an external taxonomy/code, or simply include the classification code as a property. Metadata also covers who owns or operates the asset (which could be modeled via related IFC entities like IfcOrganization and IfcRelAssignsToActor).
	•	Relationships and Links – Connections to other entities. Infrastructure assets are often hierarchical or related: e.g. a road contains road segments, a bridge has parts (spans, piers), a tunnel might be part of a road network, drainage elements (pipes, manholes) connect to a road or site. IFC uses relationship entities (such as IfcRelAggregates, IfcRelNests, IfcRelConnects, etc.) to represent these links. For example, an IfcBridge may aggregate several IfcBridgePart elements for each span, abutment, pier, etc. Similarly, a drainage pipe might be connected to a manhole via an IfcRelConnectsPorts or assigned to a system. These relationships ensure that the data model isn’t just flat properties, but a network of linked information (spatial containment, part-whole breakdown, connectivity, etc.) ￼.

A Product Data Template thus specifies all the above for a generic asset type, while an instance Data Sheet provides the actual values and links for a particular asset. The template can be thought of as a class definition, and the data sheet as an object instance.

Example: Bridge Data Template and Sheet (IFC4.3)

To illustrate, consider a bridge asset, which in IFC 4.3 would be represented by the entity IfcBridge. Below is a simplified Product Data Template for a bridge, shown in a YAML format (for human readability). This template enumerates the key attributes, properties, quantities, and metadata that should be captured for any bridge asset:

# Product Data Template for a Bridge (IFC4.3)
BridgeTemplate:
  applicableIFCClass: IfcBridge
  description: "Template defining standard data fields for a bridge asset."
  attributes:
    - name: GlobalId
      type: GUID
      description: "Unique global identifier for the bridge (generated)."
    - name: Name
      type: IfcLabel (String)
      description: "Name or title of the bridge."
    - name: Description
      type: IfcText (String)
      description: "Longer description or notes about the bridge."
    - name: PredefinedType
      type: IfcBridgeTypeEnum
      description: "Bridge type classification (e.g. OVERPASS, VIADUCT, FOOTBRIDGE, etc)."
  properties:  # Properties typically come from property sets (Pset) in IFC
    - name: StructureIndicator
      type: Enum (PEnum_StructureIndicator)
      description: "Type of bridge structure (composite, homogeneous, etc) [oai_citation:13‡ifc43-docs.standards.buildingsmart.org](https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/Pset_BridgeCommon.htm#:~:text=StructureIndicator%20IfcPropertyEnumeratedValue%20%20%2030)"
    - name: MainSpanMaterial
      type: IfcLabel (String)
      description: "Primary material of the main span (e.g. Concrete, Steel)."
    - name: NumberOfSpans
      type: IfcCountMeasure (Integer)
      description: "Total number of spans in the bridge."
    - name: LoadCapacity
      type: IfcForceMeasure (Double)
      description: "Design load capacity (e.g. in kN) the bridge can carry."
    - name: ConstructionYear
      type: IfcYearNumber (Integer)
      description: "Year the bridge was constructed or opened."
  quantities:  # Quantitative measures (QTO)
    - name: TotalLength
      type: IfcQuantityLength (Length)
      description: "Overall length of the bridge (e.g. end to end, in meters)."
    - name: DeckWidth
      type: IfcQuantityLength (Length)
      description: "Width of the bridge deck or carriageway."
    - name: DeckArea
      type: IfcQuantityArea (Area)
      description: "Surface area of the bridge deck."
    - name: DeckVolume
      type: IfcQuantityVolume (Volume)
      description: "Volume of the bridge deck structure (for material quantity)."
  metadata:
    - name: ASTRA_BridgeTypeCode
      type: String
      description: "Classification code per ASTRA or national standard for this bridge type."
    - name: OwnerOrganization
      type: String
      description: "Organization responsible for the bridge (owner/operator name)."
    - name: InspectionFrequency
      type: IfcTimeMeasure (Time period)
      description: "Planned inspection interval (e.g. in months)."
  relationships:
    - name: HasParts
      type: Aggregation (IfcRelAggregates)
      description: "Relationship linking the bridge to its constituent parts (spans, piers, etc)."
    - name: LocatedIn
      type: SpatialContainment (IfcRelContainedInSpatialStructure)
      description: "Relationship placing the bridge in a site or route context (e.g. which road or site it belongs to)."
    - name: LinkedDocuments
      type: ExternalReference (IfcRelAssociatesDocument)
      description: "Relationship linking the bridge to external documents (manuals, drawings, etc)."

In this template:
	•	The applicableIFCClass is IfcBridge, meaning this template is meant for any instance of an IFC Bridge.
	•	Under attributes, we list core IFC attributes like GlobalId (a GUID each IFC object has), Name, Description, and PredefinedType (IFC4.3 defines PredefinedType for many classes as an enumerated value to categorize the object). For bridges, IfcBridgeTypeEnum could include types like OVERPASS, VIADUCT, etc., or `USERDEFINED with a custom type.
	•	Under properties, we list domain-specific properties. For example, StructureIndicator is a property defined in the IFC schema’s standard Bridge Common property set ￼. Others like MainSpanMaterial, NumberOfSpans, etc., might be custom or from other relevant property sets (if a standard property set exists for those, one would use that). Each property has a data type – some are enumerations (like StructureIndicator which uses a predefined enum list in IFC), others are basic types (strings, numbers).
	•	Quantities cover measurable aspects; here we include total length, deck width/area/volume. These could correspond to an IFC quantity set (IfcQuantityLength, IfcQuantityArea, etc. are IFC resource types for measures). If IFC has a standard quantity set for bridges, those names would be used; otherwise, custom quantity definitions can be added.
	•	Metadata includes additional info like an ASTRA Bridge Type Code (which could map to a Swiss classification for bridge types), owner organization, and inspection frequency. These don’t necessarily have standard IFC fields, but can be captured via properties or external references. For instance, the classification code might be implemented by linking an IfcClassificationReference from the ASTRA dictionary. The owner could be an IfcOrganization linked via an IfcRelAssignsToActor (or simply recorded as text in a property for simplicity).
	•	Relationships outline how this bridge will be connected within the BIM model: it “HasParts” (e.g., IfcBridge parts like spans and supports) via aggregation; it’s “LocatedIn” some spatial structure (maybe an IfcSite or an IfcRoad context); and it can have “LinkedDocuments” (like O&M manuals or design drawings) via document association. These correspond to IFC relationship entities that carry no extra attributes except linking references, but we include them in the template so that when implementing, one knows to set up those links.

Now, when an actual bridge is modeled, a Product Data Sheet (instance) would be created following this template. Below is an example Bridge Data Sheet filled out for a hypothetical bridge, shown in JSON format (machine-readable). This corresponds to an IfcBridge instance with specific values:

{
  "guid": "3f12ABCD-...-XYZ",  /* GlobalId in IFC format (128-bit GUID encoded) */
  "name": "Bridge A1-42 (River Aare Overpass)",
  "description": "Highway overpass bridge crossing the Aare river at km 42.",
  "predefinedType": "OVERPASS",
  "properties": {
    "StructureIndicator": "composite",           /* Bridge structure type (from enum) */
    "MainSpanMaterial": "Concrete",
    "NumberOfSpans": 3,
    "LoadCapacity": 5000.0,                      /* in kN */
    "ConstructionYear": 1998
  },
  "quantities": {
    "TotalLength": 120.5,      /* in meters */
    "DeckWidth": 2*12.0,       /* two decks of 12.0 m each, for example */
    "DeckArea": 2880.0,        /* m^2, e.g. 120.5m x 24m total deck surface */
    "DeckVolume": 7200.0       /* m^3, volume of deck concrete */
  },
  "metadata": {
    "ASTRA_BridgeTypeCode": "ASTRA-BR-112233",   /* hypothetical classification code */
    "OwnerOrganization": "FEDRO (ASTRA)",
    "InspectionFrequency": "60 months"
  },
  "relationships": {
    "hasParts": [
      { "ifcClass": "IfcBridgePart", "Name": "Span-1", "GlobalId": "1111-..."} ,
      { "ifcClass": "IfcBridgePart", "Name": "Span-2", "GlobalId": "2222-..."} ,
      { "ifcClass": "IfcBridgePart", "Name": "Pier-1", "GlobalId": "3333-..."} 
    ],
    "locatedIn": { "ifcClass": "IfcSite", "Name": "Project Area West", "GlobalId": "SITE-..."},
    "linkedDocuments": [
      { "Name": "BridgeA1-42_O&M_Manual.pdf", "DocumentType": "MaintenanceManual" },
      { "Name": "BridgeA1-42_AsBuilt.ifc", "DocumentType": "AsBuiltBIM" }
    ]
  }
}

Example Bridge Data Sheet in JSON: In this instance data, we see the bridge’s guid, name, etc., filled in. The properties section has concrete values (e.g. it’s a composite structure bridge made of concrete, has 3 spans, 5000 kN capacity, built in 1998). Quantities like length, area, volume are given numeric values (with implied units). Metadata includes an example ASTRA classification code and notes ASTRA as the owner. Under relationships, we list parts (each part would itself be an IfcBridgePart object in the IFC model with its own data sheet), a reference to the site (context location), and linked documents (which in IFC would be via document references). These relationship entries are illustrative – in an actual IFC file, for example, the IfcBridge with GlobalId “3f12ABCD-…” would have an IfcRelAggregates relation pointing to the parts’ GlobalIds, etc., but here we show it in a nested JSON form for clarity.

Linking to IFC Schema: Implementing this in an actual IFC model means: the bridge object will carry the attributes (GlobalId, Name, Description, PredefinedType). Properties like StructureIndicator would be attached via an IfcPropertySet named “Pset_BridgeCommon” (since StructureIndicator is defined in that standard set) ￼. Other custom properties (if not in standard sets) could be in a project-defined IfcPropertySet. Quantities would appear in an IfcElementQuantity set (e.g., a “BridgeBaseQuantities” set, if defined, or a custom one) attached to the bridge via IfcRelDefinesByProperties. The metadata classification code might be linked by using an IfcClassification and IfcRelAssociatesClassification (pointing to “ASTRA-BR-112233” in an external ASTRA dictionary). The owner could be an IfcOrganization referenced by an IfcActor for the bridge via IfcRelAssignsToActor. All the parts/spatial relations are handled by the appropriate IfcRel objects. Thus, the template provides a blueprint, and the instance data populates the IFC model accordingly.

Other Asset Types: Tunnels, Road Elements, Drainage – Templates & Data

The approach for other asset types in infrastructure is analogous: define a template of required attributes/properties, then instantiate it for each asset. IFC 4.3 introduced entities like IfcTunnel (for tunnels), IfcRoad (for road facilities), and various element classes for road furniture, drainage, etc. Here’s a brief look at each:
	•	Tunnel (IfcTunnel): A tunnel’s PDT would include attributes like PredefinedType (perhaps distinguishing a ROAD_TUNNEL vs. RAIL_TUNNEL), and properties such as TunnelLength, CrossSectionShape, NumberOfTubes, FireSafetyLevel, LiningMaterial, etc. Quantities would include total length, cross-sectional area, volume of excavated material, etc. Relationships might link the tunnel to a road or rail line (spatially), to its tunnel parts (each tube, portals, ventilation shafts as IfcTunnelPart), and to systems like lighting or ventilation equipment inside the tunnel. Example: A JSON data sheet for a road tunnel might have {"name": "Tunnel ABC", "PredefinedType": "ROAD_TUNNEL", "properties": {"NumberOfTubes": 2, "LiningMaterial": "Concrete", "FireSafetyLevel": "RABT-class"}, "quantities": {"TunnelLength": 340.0, "ExcavationVolume": 50000.0}, ... }. The IFC model would implement these via IfcTunnel with appropriate Psets (e.g., a Pset_TunnelCommon if available) and quantities.
	•	Road Element (IfcRoad / components): Roads can be broken into segments and various elements (carriageways, pavements, shoulders, road markings, guardrails, signs, etc.). A Road as a whole (IfcRoad) would have a template including things like road type (highway, local road), design speed, number of lanes, length, surface type, etc. But many “road elements” are modeled as sub-elements. For instance, a road segment or alignment part could have properties like start and end chainage, pavement structure type, lane count, slope, etc. A guardrail (IfcBeam with a specific type or a dedicated IfcGuardRail if defined) would have properties such as length, material, containment level (from crash tests), etc. Each of these can have their own PDT. The key is to identify the IFC class and relevant properties/quantities. Example: A YAML template for a road segment might include attributes (Name, PredefinedType like “highwaySection”), properties like SurfaceMaterial, LaneCount, DesignSpeed, and quantities like SegmentLength. An instance data sheet then fills in, say, SegmentLength: 1.2 km, LaneCount: 3, SurfaceMaterial: “Asphalt Concrete”, etc., and links the segment to the overall road via IfcRelAggregates (the road facility aggregates segments).
	•	Drainage Asset (e.g., IfcPipeSegment, IfcDrainageSystem): Infrastructure projects include drainage networks (stormwater drainage, sewers). A typical drainage asset like a culvert or drain pipe could be represented by IfcPipeSegment (with a predefined type like CULVERT). Its template would cover attributes (perhaps a System attribute linking it to an IfcDistributionSystem for “DrainageNetwork”), and properties such as Diameter, Length, Material, Capacity (flow), InstallationYear, etc. Quantities would include length (which might equal the design length if straight), excavated depth, etc. For a manhole or inlet, an IfcFlowTerminal or IfcDistributionChamberElement might be used, with properties like dimensions, cover type, etc. Relationships link these elements into a network (using IfcRelConnectsPorts or IfcRelAggregates under an IfcDrainageSystem). Example: A JSON data sheet for a drainage pipe might look like: {"ifcClass": "IfcPipeSegment", "PredefinedType": "CULVERT", "Name": "Culvert under Bridge A1-42", "properties": {"Diameter": 1.2, "Material": "HDPE", "DesignFlow": 500.0}, "quantities": {"Length": 30.0}, "metadata": {"InstallationYear": 2010}, "relationships": {"connectsTo": "Manhole-XYZ"}}. This indicates a 30 m long, 1.2 m diameter HDPE culvert pipe installed in 2010, with a design flow capacity, connected to a specific manhole. In IFC, the IfcPipeSegment would carry those properties (perhaps via Pset_PipeSegmentCommon for Diameter, etc.) and be connected in the model via port connections or an aggregation under a drainage system.

Each of these examples follows the same pattern: define the necessary fields in a template, then provide the values in an instance. The IFC schema provides the classes and relationship framework to formalize this. Notably, one can also use Information Delivery Specifications (IDS) alongside IFC, which essentially are machine-readable requirements (often in XML/YAML) stating what properties must be present for certain objects – effectively encoding the PDT rules. This can be used to validate that an IFC file (with numerous PDS instances) conforms to the required templates.

Machine-Readable Formats: JSON, YAML, RDF

It’s important that these templates and data sheets are both human-readable and machine-processable. JSON and YAML are popular formats for structured data. In fact, buildingSMART has been developing official IFC JSON schemas and serialization alongside the traditional STEP (ASCII) format ￼ ￼. JSON is easily parsed by software and widely used in web APIs, while YAML is essentially a more human-friendly superset of JSON (the YAML examples above can be converted to JSON automatically, and vice versa).

For example, the JSON snippet provided for the bridge data sheet could be ingested by a BIM platform or a validation tool to automatically populate or check an IFC model. Similarly, one could imagine maintaining a library of YAML templates for different asset types – these could be read by scripts to ensure that all required fields are present in a model or to generate input forms for data collection.

RDF (Resource Description Framework) is another machine-readable format, following a linked data/semantic web approach. IFC data can be represented in RDF via the ifcOWL ontology (an OWL representation of the IFC schema) ￼. This means each IFC entity becomes a subject in a triple store, with attributes and properties as predicate–value pairs. RDF is highly suited for linking data across domains – e.g., linking an IFC bridge to an entry in an external asset registry or to GIS data. ASTRA’s mention of RDF ￼ suggests an interest in linking BIM data with other datasets (e.g., asset management systems, which might use semantic web standards). For instance, using RDF one could link the bridge’s GUID to an entry in a maintenance database or to a geospatial identifier, enabling queries that combine BIM and asset management information.

Example RDF snippet (simplified in Turtle syntax):

:BridgeA142 rdf:type ifc:IfcBridge ;
    ifc:GlobalId "3f12ABCD-...-XYZ" ;
    ifc:Name "Bridge A1-42 (River Aare Overpass)" ;
    ifc:PredefinedType ifc4x3_bridge:OVERPASS ;  # using a prefixed enum individual
    ifc:hasPropertySet :BridgeA142_PsetCommon .  # link to a property set individual

:BridgeA142_PsetCommon rdf:type ifc:IfcPropertySet ;
    ifc:Name "Pset_BridgeCommon" ;
    ifc:hasProperty :Prop_StructureIndicator .

:Prop_StructureIndicator rdf:type ifc:IfcPropertyEnumeratedValue ;
    ifc:Name "StructureIndicator" ;
    ifc:nominalValue :Enum_StructureIndicator_Composite .

:Enum_StructureIndicator_Composite rdf:type ifc:PEnum_StructureIndicator ;
    ifc:value "composite" .

Illustrative RDF/ifcOWL triples: showing an IfcBridge instance with a property set and an enumerated property value for StructureIndicator (“composite”). In a full RDF graph, the bridge would also be linked to other resources: e.g., an external classification URI for the ASTRA type code, relationships to parts (via blank nodes or relations linking to other IFC individuals), etc. The power of RDF is that the Product Data Template can itself be published as a concept in a dictionary (e.g., the template says “IfcBridge shall have a property StructureIndicator defined as …”), and instances link to those concepts, enabling reasoners to check conformance. The buildingSMART Data Dictionary (bSDD) is essentially a repository of such definitions (concepts for properties, templates, etc.) accessible via linked data APIs ￼.

Implementing Templates with IFC Schema

To systematically specify and implement these templates in an IFC-based project, one can follow these steps:
	1.	Define Data Templates: For each asset type, list all required attributes, properties, etc. This can be done in a human-readable form (tables or YAML/JSON as above). Align each field with IFC schema elements: identify if it maps to an IFC attribute, a standard property set, a quantity, or requires a custom property. Use standardized definitions whenever possible (e.g., reuse IFC’s predefined property sets and enums, or definitions from bSDD to maintain consistency ￼). In IFC terms, you could formalize this using IfcPropertySetTemplate and IfcPropertyTemplate entities (which IFC provides for template definitions), but these are often used by schema developers; for a project, a simpler approach is to document the templates externally or via an IDS.
	2.	Populate Instance Data: When creating the BIM model, ensure each asset instance (Ifc element) includes all the data per the template. This means setting the IFC object’s attributes (GlobalId auto-generated by software, Name/Description filled in, PredefinedType chosen appropriately). Then attach property sets for the template’s properties: e.g., create an IfcPropertySet named as per the template (or reuse a standard one) and attach IfcPropertySingleValue, IfcPropertyEnumeratedValue, etc., for each property. Do similar for quantities (using IfcQuantitySet). Many BIM authoring tools allow configuring these properties, or one can enrich the IFC file after export (some workflows use scripts or middleware to inject data).
	3.	Establish Relationships: Create the linking relationships in IFC: e.g., use IfcRelAggregates to compose a facility from parts, IfcRelContainedInSpatialStructure to place elements in sites or projects, IfcRelAssociatesClassification to tag classifications, IfcRelAssociatesDocument for documents, and so on. This step implements the “links” part of the template, ensuring the IFC model isn’t just isolated pieces but a connected graph of information.
	4.	Use Machine-Readable Formats and Validation: Store or exchange the template definitions in a machine-readable form (YAML/JSON/RDF). For instance, an IDS (Information Delivery Specification) can be written (often in XML or YAML) to formally require that “IfcBridge must have properties X, Y, Z with such datatypes” – this IDS can be used with software to automatically check an IFC file for compliance. The JSON or RDF representations of the data can be used for integration with other systems: e.g., exporting an IFC model to ifcJSON allows web applications to directly consume the data ￼, and exposing it as linked data (RDF) allows queries using SPARQL across BIM and asset management data.

By following this systematic approach, one ensures that each asset in an infrastructure BIM project has a comprehensive, standardized data sheet associated with it, fulfilling the information requirements (for ASTRA or any stakeholder). The combination of IFC as the exchange format and data templates as the content schema provides a robust solution: IFC takes care of interoperability (the “how” to transport data), while the templates/data sheets ensure completeness and consistency of the “what” data is included ￼. This leads to richer BIM models that serve not only during design/construction but also feed into asset management systems and long-term maintenance of infrastructure. It’s a cornerstone of achieving a digital twin of infrastructure that ASTRA and others aim for, where all asset information is readily available, up-to-date, and exchangeable throughout the asset’s lifecycle.

Sources: The methodology above is informed by IFC4.3 documentation and buildingSMART guidelines. IFC4.3 supports infrastructure assets like bridges, roads, etc., with new entity definitions and property sets ￼. BuildingSMART’s Data Dictionary and Product Data Template standards (EN ISO 23386/23387) provide the framework for defining properties and templates in a consistent way ￼. Combining IFC with data templates is recognized as crucial for interoperability – “IFC provides the ‘how’ (transport format), while data templates provide the ‘what’ (content structure)” ￼. The example bridge property StructureIndicator is drawn from the IFC4.3 standard bridge property set ￼. Moreover, efforts like CEN EN 17549-2 (2023) explicitly introduce an IFC-based exchange structure for product data based on templates ￼, underscoring the approach shown here. Finally, the Swiss road authority ASTRA’s BIM strategy endorses open standards (IFC, RDF) ￼, aligning with the use of such data templates and linked data for managing infrastructure asset information in Switzerland.
