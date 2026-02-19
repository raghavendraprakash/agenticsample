ULD LOAD PLANNER - KNOWLEDGE BASE DATA
=======================================

This directory contains synthetic data files for the ULD Load Planner multi-agent system.
All data is in .txt format for easy parsing and knowledge base integration.

DIRECTORY CONTENTS (29 files)
==============================

1. FLIGHT SCHEDULES (5 files)
   - flight_schedule_001.txt - AA1234 (JFK→LHR, B777)
   - flight_schedule_002.txt - BA456 (LAX→NRT, A350)
   - flight_schedule_003.txt - LH789 (FRA→SIN, B747)
   - flight_schedule_004.txt - EK234 (DXB→SYD, A330)
   - flight_schedule_005.txt - UA567 (ORD→CDG, B767)

2. AIRCRAFT CONFIGURATIONS (5 files)
   - aircraft_config_a330.txt - Airbus A330-300 (24 positions)
   - aircraft_config_a350.txt - Airbus A350-900 (28 positions)
   - aircraft_config_b747.txt - Boeing 747-8F (38 positions)
   - aircraft_config_b767.txt - Boeing 767-400ER (22 positions)
   - aircraft_config_b777.txt - Boeing 777-300ER (32 positions)

3. ULD SPECIFICATIONS (5 files)
   - uld_spec_aaa_ld7.txt - AAA/LD7 Container
   - uld_spec_aap_ld6.txt - AAP/LD6 Container
   - uld_spec_ake_ld3.txt - AKE/LD3 Container
   - uld_spec_akn_ld8.txt - AKN/LD8 Container
   - uld_spec_ama_ld9.txt - AMA/LD9 Container

4. SHIPMENT DATA (5 files)
   - shipment_awb_001.txt - Electronics (JFK→LHR, 850kg)
   - shipment_awb_002.txt - Medical/Perishable (LAX→NRT, 420kg)
   - shipment_awb_003.txt - Heavy Machinery (FRA→SIN, 1850kg)
   - shipment_awb_004.txt - Dangerous Goods (DXB→SYD, 680kg)
   - shipment_awb_005.txt - Live Animals (ORD→CDG, 320kg)

5. VALIDATION RULES (3 files)
   - validation_rules_dimensional.txt - 10 dimensional constraint rules
   - validation_rules_handling.txt - Handling code compatibility matrix
   - validation_rules_weight.txt - 7 structural weight validation rules

6. HISTORICAL PATTERNS (2 files)
   - historical_pattern_jfk_lhr.txt - JFK→LHR route analysis (90 days)
   - historical_pattern_lax_nrt.txt - LAX→NRT route analysis (90 days)

7. CURRENT FBL DATA (2 files)
   - fbl_current_aa1234.txt - Flight AA1234 current assignments
   - fbl_current_ba456.txt - Flight BA456 current assignments

8. ULD INVENTORY (2 files)
   - uld_inventory_station_jfk.txt - JFK station inventory
   - uld_inventory_station_lax.txt - LAX station inventory

DATA CATEGORIES SUMMARY
========================

AIRCRAFT TYPES COVERED:
- Boeing 777-300ER
- Airbus A350-900
- Boeing 747-8F
- Boeing 767-400ER
- Airbus A330-300

ULD TYPES COVERED:
- AKE (LD3) - Most common, 3.5 m³
- AAA (LD7) - Double LD3, 7.2 m³
- AKN (LD8) - Medium, 5.5 m³
- AAP (LD6) - Similar to LD7, 7.2 m³
- AMA (LD9) - Large, 11.6 m³

HANDLING CODES COVERED:
- HEA (Heavy Cargo)
- DGR (Dangerous Goods)
- AVI (Live Animals)
- PER (Perishable)
- LAR (Large/Oversized)
- GEN (General Cargo)

ROUTES COVERED:
- JFK → LHR (New York to London)
- LAX → NRT (Los Angeles to Tokyo)
- FRA → SIN (Frankfurt to Singapore)
- DXB → SYD (Dubai to Sydney)
- ORD → CDG (Chicago to Paris)

KEY METRICS IN DATA
===================

WEIGHT RANGES:
- Light cargo: 320-850 kg
- Medium cargo: 850-1850 kg
- Heavy cargo: 1850+ kg

VOLUME RANGES:
- Small: 1.8-2.8 m³
- Medium: 2.8-4.2 m³
- Large: 4.2+ m³

AIRCRAFT CAPACITIES:
- B767: 12,600 kg, 22 positions
- A330: 14,800 kg, 24 positions
- A350: 16,200 kg, 28 positions
- B777: 18,500 kg, 32 positions
- B747: 24,500 kg, 38 positions

USAGE SCENARIOS
===============

1. PATTERN ANALYSIS AGENT:
   - Use historical_pattern_*.txt files
   - Analyze loading trends and optimization opportunities
   - Identify common cargo mixes and position preferences

2. ALLOCATION RECOMMENDATION AGENT:
   - Use aircraft_config_*.txt for position layouts
   - Use uld_spec_*.txt for container selection
   - Use validation_rules_*.txt for constraint checking
   - Use uld_inventory_*.txt for availability

3. LOAD PLANNER ORCHESTRATOR:
   - Combine data from all sources
   - Match shipments to flights
   - Optimize ULD allocation
   - Generate comprehensive load plans

VALIDATION RULES SUMMARY
=========================

DIMENSIONAL RULES (10):
- Maximum piece dimensions
- Overhang limits by ULD type
- Weight distribution requirements
- Stacking height limits
- Volume utilization targets
- Piece count limits
- Mixed commodity restrictions
- Fragile cargo placement

WEIGHT RULES (7):
- ULD maximum gross weight
- Aircraft position weight limits
- Floor loading limits
- Total aircraft cargo weight
- Weight balance requirements
- Heavy cargo concentration limits
- Single piece weight limits

HANDLING COMPATIBILITY:
- Segregation requirements for dangerous goods
- Live animal handling restrictions
- Perishable cargo requirements
- Heavy cargo ULD requirements
- Position restrictions by handling code

DATA QUALITY NOTES
==================

All data is synthetic but realistic:
- Based on actual IATA ULD specifications
- Aircraft configurations match real-world layouts
- Weight and dimension limits are accurate
- Handling codes follow IATA standards
- Validation rules reflect industry best practices

INTEGRATION NOTES
=================

For Knowledge Base Integration:
1. Parse .txt files into structured format
2. Index by category (flights, aircraft, ULDs, shipments)
3. Create relationships between entities
4. Enable semantic search across all data
5. Support pattern matching and historical analysis

For Agent Usage:
- Pattern Analysis Agent: Focus on historical_pattern_*.txt
- Allocation Agent: Focus on aircraft_config_*, uld_spec_*, validation_rules_*
- Orchestrator: Access all data sources for comprehensive planning

FUTURE ENHANCEMENTS
===================

Additional data that could be added:
- More flight schedules (target: 15 total)
- More shipment AWBs (target: 40 total)
- Additional ULD types (target: 20 total)
- More historical patterns (different routes/seasons)
- Weather and delay data
- Customs and regulatory requirements
- Cost optimization data
- Real-time tracking data

---

Created: 2026-02-20
Version: 1.0
Format: Plain text (.txt)
Total Files: 29
Total Size: ~150 KB
