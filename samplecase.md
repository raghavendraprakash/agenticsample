**Key Requirement**

Provide Historical Pattern Analysis report leveraging aircraft-specific loading patterns and ULD type matching data and provide Allocation plan recommendations.

**Persona:** Load Planner

Architecture: Multi-Agent collaboration with Agents as Tools pattern

Orchestrator agent: 

*   Load Planner Agent interacts with specialist agents and consolidate the report to the user, uses Claude Sonnet 4.5

Specialist agents:

*   Pattern Analysis agent provides historical pattern analysis report, uses Nova model
*   Allocation plan recommendation agent provides position recommendation report, uses Noval model

**Knowledge Base Requirements**

1\. Flight & Aircraft Data (JSON/CSV):

*   Flight schedules (15 sample flights with departure times, aircraft types, POL)
*   Aircraft configurations (5 types: B777, A350, B747, B767, A330)
*   ULD position layouts and capacity constraints
*   Current FBL data (mock position assignments)

2\. Shipment Inventory Data (JSON/CSV):

*   RFC shipments (40 sample AWBs with dimensions, weight, handling codes)
*   Priority rankings and handling requirements
*   Dimensional characteristics (L×W×H)
*   Handling code definitions (HEA, DGR, AVI, PER, LAR)

3\. ULD Specifications Data (JSON):

*   ULD types (20 types: AKE, AKN, AAA, AMA, etc.)
*   Dimensions, tare weights, structural weight limits
*   ULD-aircraft compatibility matrix
*   Available inventory at station

4\. Validation Rules & Constraints (JSON):

*   Dimensional constraint rules (15 core rules)
*   Overhang limits by ULD type
*   Structural weight validation thresholds
*   Handling code compatibility matrix