# Silber‑Preis‑Prognose 2024‑2028 – Technische Analyse & Umsetzungsempfehlungen  

*(Diese Datei fasst die zuvor erarbeiteten Inhalte zusammen und ist als eigenständiges Markdown‑Dokument nutzbar.)*  

---  

## 1. Grund‑Architektur – „Data‑to‑Collaboration‑Layer“

| Ebene | Ziel | Standard / Praxis | Kern‑Artefakte |
|------|------|-------------------|----------------|
| **1  Data‑Layer** | Roh‑geometrische & attributive Daten (BIM‑Modelle, GIS, Sensoren) | **IFC 4 / 4.3** (offenes Klassen‑/Eigenschaftsschema) – z. B. `IfcProject`, `IfcSite`, `IfcBuilding`, `IfcWall` usw.; **IfcPropertySet** für standardisierte Attributsammlungen【14†L31-L44】 | Modell‑Dateien (`*.ifc`), Property‑Set‑Templates (`Pset_…`) |
| **2  Information‑Layer** | Kontextualisierte, projekt‑spezifische Infos (Pläne, Stücklisten, Verfahrensanweisungen) | **ISO 19650‑1 / 2** (CDE, IDM, IAG/OPR) – Information Requirements & Exchange Formats (COBie, BCF) | Informations‑Container (Ordner, PDFs, Excel‑COBie, BCF‑Dateien) |
| **3  Collaboration‑Layer** | Rollen‑basiertes Arbeiten, Review‑Workflows, Freigaben | **ISO 19650‑3 / 5** (Projekt‑/Asset‑Management); **BuildingSMART‑Swiss** (SIA 1001/11‑Ergänzungs‑Vereinbarung)【17†L3-L13】 | CDE (BIM‑360, Trimble Connect, Share‑IT), Issue‑Tracking, Audit‑Logs |

> **Prinzip:** Alle Daten werden über die offene **IFC‑Schnittstelle** modelliert, in einem **ISO‑19650‑konformen CDE** versioniert und die Prozesse über ein **Information‑Delivery‑Manual (IDM)** gesteuert.  

---  

## 2. ISO 19650 – Informations‑Delivery‑Manual (IDM)

| IDM‑Element | Inhalt | Praktische Umsetzung |
|-------------|--------|----------------------|
| **IAG** (Information‑Asset‑Group) | Auftraggeber‑Anforderungen (z. B. „Bauwerksmodell LOD 300 bis 2025‑03‑31“). | In der **BIM‑Execution‑Plan (BEP)** definiert, z. B. in einem Excel‑Template im CDE. |
| **OPR** (Exchange‑Information‑Requirements) | Detaillierte Angaben, welche Daten in welchem Format (IFC, COBie, BCF) ausgetauscht werden müssen. | Verknüpft mit **MVD‑Definitionen** (Model‑View‑Definitions) – z. B. *IFC‑MVD for Design‑Construction hand‑over*. |
| **CDE** (Common Data Environment) | Zentraler Ablage‑ und Versions‑Server, strukturiert nach **ISO 19650‑2‑Ordner‑Regeln** (§ 5.2). | Ordner‑ und Dateinamen nach **BIMicon‑Namenskonvention** (Titel‑Case, Feld‑Trenner „‑“, Sequenz‑Nummern)【12†L18-L28】【12†L77-L84】. |

**Tipp:** Jede Datei erhält eine **GUID** (IFC‑global‑unique‑identifier) und wird im Dateinamen mitgeführt (z. B. `PRJ123-01-ARCH-Model-LOD300-20240315-GUID12345.ifc`).  

---  

## 3. IFC‑Schema – Kern‑Klassen & Property‑Sets (Ontologie)

| Klasse | Sinn | Typische Property‑Sets (`Pset_…`) |
|--------|------|---------------------------------|
| **IfcProject** | Projekt‑Root, globale Koordinatensysteme. | `Pset_ProjectGeneral` (Projekt‑ID, Owner, Currency). |
| **IfcSite** | Standort‑Info (Geodaten, Topographie). | `Pset_SiteCommon`. |
| **IfcBuilding** | Gebäude‑Objekt, LOD‑Angaben, Nutzung. | `Pset_BuildingCommon`, `Pset_BuildingStorey`. |
| **IfcWall / IfcDoor / IfcWindow** | Technische Bauteile. | `Pset_WallCommon`, `Pset_DoorCommon`, `Pset_WindowCommon`. |
| **IfcComponent** (z. B. **IfcElectricalDevice**) | Anlagen‑ und Haustechnik. | `Pset_ElectricalDeviceCommon`. |

*Die Benennung der Property‑Sets folgt dem „**Pset_​Xxx**“-Muster (siehe Zeile 42‑44)【14†L42-L44】. Selbst‑definierte Sets dürfen **kein** „Pset_“-Präfix erhalten (Zeile 45‑47)【14†L45-L47】.*  

### 3.1 IFC – Ontologie‑Erweiterung (IfcOWL)

- **IfcOWL** (RDF‑basierte Ontologie) ermöglicht semantische Abfragen (SPARQL) über BIM‑Daten.  
- Ideal für **Asset‑Management‑ und Facility‑Operation‑Workflows**, weil die Daten leicht mit anderen Unternehmens‑Ontologien (z. B. ISO 12006‑2) verknüpft werden können.  

---  

## 4. Namens‑ & Ordner‑Konventionen (ISO 19650 + BIMicon)

| Ebene | Muster (Beispiel) | Erläuterung |
|------|-------------------|-------------|
| **Projekt‑Ordner** | `PRJ‑1234‑[Phase]‑[Disziplin]` | `PRJ-1234-01-ARCH` (Entwurfs‑Phase, Architektur). |
| **Datei‑Name** | `PRJ1234‑01‑ARCH‑Model‑LOD300‑20240315‑UID12345.ifc` | Felder: Projekt‑ID – Phase – Disziplin – Artefakt – LOD – Datum – GUID. |
| **Version** | `v001`, `v002` (numerisch, führende Nullen) – immer nach Datum / GUID. | Verhindert Sortier‑Probleme (siehe Zeile 77‑84)【12†L77-L84】. |
| **Zeichen‑Verbot** | Keine der Zeichen `/ \ : * ? " < > | [ ] & $ , . { } @` (Zeile 28‑33)【12†L28-L33】. |
| **Länge** | Max. 260 Zeichen (OS‑Grenze) (Zeile 66‑70)【12†L66-L70】. |

**Check‑Liste für neue Dateien**  

1. Titel‑Case, keine Sonderzeichen.  
2. Felder durch „‑“ trennen, innerhalb eines Feldes Leerzeichen oder Unterstrich „_“.  
3. GUID am Ende, **vor** der Dateiendung.  
4. Versions‑Nummer im Metadaten‑Tag (z. B. `IfcOwnerHistory`).  

---  

## 5. Prozesse & Workflows (nach ISO 19650)

```mermaid
graph LR
    A[Client – IAG] -->|Define| B["Project Information Requirements (PID)"]
    B --> C["Information Delivery Manual (IDM)"]
    C --> D["Common Data Environment (CDE)"]
    D --> E["Model Creation – IFC (LOD‑x)"]
    E --> F[Model Review – BCF Issues]
    F --> G[Validated Release – COBie / IFC]
    G --> H[Construction – FM Handover]
    H --> I[Asset Management – IfcOWL / GIS]
``````
