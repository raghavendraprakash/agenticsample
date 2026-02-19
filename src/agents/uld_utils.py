"""
ULD Utility Functions - Local tools for cargo calculations and validations.

This module provides utility functions that can be called by ULD agents
during orchestration for calculations, validations, and data processing.
"""

from strands import tool
from typing import Dict, List, Tuple, Optional
import json


@tool
def calculate_total_weight(cargo_items: str) -> str:
    """Calculate total weight of cargo items.
    
    This tool calculates the total weight from a list of cargo items.
    Input should be JSON string with format: [{"weight": 500, "quantity": 5}, ...]
    
    Args:
        cargo_items: JSON string containing list of cargo items with weight and quantity
        
    Returns:
        String with total weight calculation and breakdown
        
    Example:
        >>> result = calculate_total_weight('[{"weight": 500, "quantity": 5}, {"weight": 300, "quantity": 3}]')
        >>> print(result)
        "Total Weight: 3400 kg (5 items @ 500kg = 2500kg, 3 items @ 300kg = 900kg)"
    """
    try:
        items = json.loads(cargo_items)
        
        total_weight = 0
        breakdown = []
        
        for item in items:
            weight = item.get('weight', 0)
            quantity = item.get('quantity', 1)
            item_total = weight * quantity
            total_weight += item_total
            
            breakdown.append(f"{quantity} items @ {weight}kg = {item_total}kg")
        
        result = f"Total Weight: {total_weight} kg\nBreakdown:\n" + "\n".join(f"  - {b}" for b in breakdown)
        return result
        
    except Exception as e:
        return f"Error calculating weight: {str(e)}"


@tool
def calculate_total_volume(cargo_items: str) -> str:
    """Calculate total volume of cargo items.
    
    This tool calculates the total volume from cargo dimensions.
    Input should be JSON string with format: [{"length": 120, "width": 100, "height": 80, "quantity": 5}, ...]
    Dimensions in centimeters, returns volume in cubic meters.
    
    Args:
        cargo_items: JSON string containing cargo items with dimensions (cm) and quantity
        
    Returns:
        String with total volume calculation and breakdown
        
    Example:
        >>> result = calculate_total_volume('[{"length": 120, "width": 100, "height": 80, "quantity": 5}]')
        >>> print(result)
        "Total Volume: 4.8 cubic meters"
    """
    try:
        items = json.loads(cargo_items)
        
        total_volume_cm3 = 0
        breakdown = []
        
        for item in items:
            length = item.get('length', 0)
            width = item.get('width', 0)
            height = item.get('height', 0)
            quantity = item.get('quantity', 1)
            
            # Calculate volume in cubic centimeters
            item_volume_cm3 = length * width * height
            item_volume_m3 = item_volume_cm3 / 1_000_000  # Convert to cubic meters
            total_item_volume = item_volume_m3 * quantity
            
            total_volume_cm3 += item_volume_cm3 * quantity
            
            breakdown.append(
                f"{quantity} items @ {length}x{width}x{height}cm = {total_item_volume:.2f}m³"
            )
        
        total_volume_m3 = total_volume_cm3 / 1_000_000
        
        result = f"Total Volume: {total_volume_m3:.2f} cubic meters\nBreakdown:\n" + "\n".join(f"  - {b}" for b in breakdown)
        return result
        
    except Exception as e:
        return f"Error calculating volume: {str(e)}"


@tool
def validate_weight_constraints(uld_type: str, cargo_weight: float, include_tare: bool = True) -> str:
    """Validate if cargo weight is within ULD capacity limits.
    
    This tool checks if the cargo weight fits within the specified ULD type's
    maximum weight capacity, optionally including tare weight.
    
    Args:
        uld_type: ULD type code (AKE, AAA, AKN, AAP, AMA)
        cargo_weight: Weight of cargo in kg
        include_tare: Whether to include tare weight in calculation (default: True)
        
    Returns:
        String with validation result and capacity information
        
    Example:
        >>> result = validate_weight_constraints("AKE", 1500, True)
        >>> print(result)
        "✅ VALID: Cargo weight 1500kg fits in AKE (LD3) - Max capacity: 1588kg"
    """
    # ULD specifications (max gross weight and tare weight)
    uld_specs = {
        "AKE": {"name": "LD3", "max_gross": 1588, "tare": 85, "max_net": 1503},
        "AAA": {"name": "LD7", "max_gross": 4626, "tare": 120, "max_net": 4506},
        "AKN": {"name": "LD8", "max_gross": 2449, "tare": 105, "max_net": 2344},
        "AAP": {"name": "LD6", "max_gross": 3176, "tare": 115, "max_net": 3061},
        "AMA": {"name": "LD9", "max_gross": 6804, "tare": 180, "max_net": 6624},
    }
    
    uld_type_upper = uld_type.upper()
    
    if uld_type_upper not in uld_specs:
        return f"❌ ERROR: Unknown ULD type '{uld_type}'. Valid types: AKE, AAA, AKN, AAP, AMA"
    
    spec = uld_specs[uld_type_upper]
    
    if include_tare:
        total_weight = cargo_weight + spec["tare"]
        max_capacity = spec["max_gross"]
        capacity_type = "max gross weight"
    else:
        total_weight = cargo_weight
        max_capacity = spec["max_net"]
        capacity_type = "max net weight"
    
    if total_weight <= max_capacity:
        remaining = max_capacity - total_weight
        utilization = (total_weight / max_capacity) * 100
        
        result = f"✅ VALID: Cargo weight {cargo_weight}kg fits in {uld_type_upper} ({spec['name']})\n"
        result += f"  - {capacity_type.title()}: {max_capacity}kg\n"
        result += f"  - Total weight (with tare): {total_weight}kg\n" if include_tare else f"  - Cargo weight: {total_weight}kg\n"
        result += f"  - Remaining capacity: {remaining}kg\n"
        result += f"  - Utilization: {utilization:.1f}%"
        
        return result
    else:
        excess = total_weight - max_capacity
        result = f"❌ INVALID: Cargo weight {cargo_weight}kg EXCEEDS {uld_type_upper} ({spec['name']}) capacity\n"
        result += f"  - {capacity_type.title()}: {max_capacity}kg\n"
        result += f"  - Total weight (with tare): {total_weight}kg\n" if include_tare else f"  - Cargo weight: {total_weight}kg\n"
        result += f"  - Excess weight: {excess}kg\n"
        result += f"  - Recommendation: Use larger ULD type or split cargo"
        
        return result


@tool
def calculate_uld_requirements(total_weight: float, total_volume: float, uld_type: str = "AKE") -> str:
    """Calculate how many ULDs are needed for given cargo weight and volume.
    
    This tool determines the number of ULDs required based on both weight
    and volume constraints, returning the limiting factor.
    
    Args:
        total_weight: Total cargo weight in kg
        total_volume: Total cargo volume in cubic meters
        uld_type: ULD type to use (default: AKE)
        
    Returns:
        String with ULD quantity calculation and reasoning
        
    Example:
        >>> result = calculate_uld_requirements(2500, 9.0, "AKE")
        >>> print(result)
        "ULDs Required: 3 x AKE (LD3) containers (limited by volume)"
    """
    # ULD specifications
    uld_specs = {
        "AKE": {"name": "LD3", "max_net": 1503, "volume": 3.5},
        "AAA": {"name": "LD7", "max_net": 4506, "volume": 7.2},
        "AKN": {"name": "LD8", "max_net": 2344, "volume": 5.5},
        "AAP": {"name": "LD6", "max_net": 3061, "volume": 7.2},
        "AMA": {"name": "LD9", "max_net": 6624, "volume": 11.6},
    }
    
    uld_type_upper = uld_type.upper()
    
    if uld_type_upper not in uld_specs:
        return f"❌ ERROR: Unknown ULD type '{uld_type}'. Valid types: AKE, AAA, AKN, AAP, AMA"
    
    spec = uld_specs[uld_type_upper]
    
    # Calculate ULDs needed based on weight
    ulds_by_weight = (total_weight / spec["max_net"])
    ulds_by_weight_rounded = int(ulds_by_weight) + (1 if ulds_by_weight % 1 > 0 else 0)
    
    # Calculate ULDs needed based on volume
    ulds_by_volume = (total_volume / spec["volume"])
    ulds_by_volume_rounded = int(ulds_by_volume) + (1 if ulds_by_volume % 1 > 0 else 0)
    
    # The limiting factor determines actual ULDs needed
    ulds_required = max(ulds_by_weight_rounded, ulds_by_volume_rounded)
    limiting_factor = "weight" if ulds_by_weight_rounded > ulds_by_volume_rounded else "volume"
    
    result = f"ULDs Required: {ulds_required} x {uld_type_upper} ({spec['name']}) containers\n"
    result += f"  - Limiting factor: {limiting_factor}\n"
    result += f"  - By weight: {ulds_by_weight:.2f} ULDs ({total_weight}kg ÷ {spec['max_net']}kg)\n"
    result += f"  - By volume: {ulds_by_volume:.2f} ULDs ({total_volume}m³ ÷ {spec['volume']}m³)\n"
    result += f"  - Weight utilization: {(total_weight / (ulds_required * spec['max_net'])) * 100:.1f}%\n"
    result += f"  - Volume utilization: {(total_volume / (ulds_required * spec['volume'])) * 100:.1f}%"
    
    return result


@tool
def check_dimensional_fit(cargo_length: float, cargo_width: float, cargo_height: float, uld_type: str) -> str:
    """Check if cargo dimensions fit within ULD internal dimensions.
    
    This tool validates that cargo pieces will physically fit inside the
    specified ULD type, considering internal dimensions.
    
    Args:
        cargo_length: Cargo length in cm
        cargo_width: Cargo width in cm
        cargo_height: Cargo height in cm
        uld_type: ULD type code (AKE, AAA, AKN, AAP, AMA)
        
    Returns:
        String with dimensional fit validation result
        
    Example:
        >>> result = check_dimensional_fit(120, 100, 150, "AKE")
        >>> print(result)
        "✅ FITS: Cargo 120x100x150cm fits in AKE (LD3) internal dimensions"
    """
    # ULD internal dimensions (length x width x height in cm)
    uld_dimensions = {
        "AKE": {"name": "LD3", "length": 150, "width": 147, "height": 157},
        "AAA": {"name": "LD7", "length": 311, "width": 147, "height": 157},
        "AKN": {"name": "LD8", "length": 238, "width": 147, "height": 157},
        "AAP": {"name": "LD6", "length": 311, "width": 147, "height": 157},
        "AMA": {"name": "LD9", "length": 311, "width": 238, "height": 157},
    }
    
    uld_type_upper = uld_type.upper()
    
    if uld_type_upper not in uld_dimensions:
        return f"❌ ERROR: Unknown ULD type '{uld_type}'. Valid types: AKE, AAA, AKN, AAP, AMA"
    
    dim = uld_dimensions[uld_type_upper]
    
    # Check if cargo fits (allowing 5cm overhang on top as per rules)
    length_fits = cargo_length <= dim["length"]
    width_fits = cargo_width <= dim["width"]
    height_fits = cargo_height <= (dim["height"] + 5)  # 5cm overhang allowed
    
    all_fit = length_fits and width_fits and height_fits
    
    if all_fit:
        result = f"✅ FITS: Cargo {cargo_length}x{cargo_width}x{cargo_height}cm fits in {uld_type_upper} ({dim['name']})\n"
        result += f"  - ULD internal dimensions: {dim['length']}x{dim['width']}x{dim['height']}cm\n"
        result += f"  - Length clearance: {dim['length'] - cargo_length}cm\n"
        result += f"  - Width clearance: {dim['width'] - cargo_width}cm\n"
        result += f"  - Height clearance: {(dim['height'] + 5) - cargo_height}cm (5cm overhang allowed)"
    else:
        result = f"❌ DOES NOT FIT: Cargo {cargo_length}x{cargo_width}x{cargo_height}cm EXCEEDS {uld_type_upper} ({dim['name']}) dimensions\n"
        result += f"  - ULD internal dimensions: {dim['length']}x{dim['width']}x{dim['height']}cm (+ 5cm overhang)\n"
        
        if not length_fits:
            result += f"  - ❌ Length: {cargo_length}cm > {dim['length']}cm (excess: {cargo_length - dim['length']}cm)\n"
        else:
            result += f"  - ✅ Length: {cargo_length}cm ≤ {dim['length']}cm\n"
            
        if not width_fits:
            result += f"  - ❌ Width: {cargo_width}cm > {dim['width']}cm (excess: {cargo_width - dim['width']}cm)\n"
        else:
            result += f"  - ✅ Width: {cargo_width}cm ≤ {dim['width']}cm\n"
            
        if not height_fits:
            result += f"  - ❌ Height: {cargo_height}cm > {dim['height'] + 5}cm (excess: {cargo_height - (dim['height'] + 5)}cm)\n"
        else:
            result += f"  - ✅ Height: {cargo_height}cm ≤ {dim['height'] + 5}cm\n"
        
        result += f"  - Recommendation: Use larger ULD type or reorient cargo"
    
    return result


@tool
def compare_uld_options(cargo_weight: float, cargo_volume: float) -> str:
    """Compare different ULD options for given cargo specifications.
    
    This tool evaluates multiple ULD types and recommends the most efficient
    option based on weight and volume utilization.
    
    Args:
        cargo_weight: Total cargo weight in kg
        cargo_volume: Total cargo volume in cubic meters
        
    Returns:
        String with comparison of ULD options and recommendation
        
    Example:
        >>> result = compare_uld_options(2500, 9.0)
        >>> print(result)
        "Recommended: 2 x AAA (LD7) - Best utilization (85% weight, 62% volume)"
    """
    # ULD specifications
    uld_specs = {
        "AKE": {"name": "LD3", "max_net": 1503, "volume": 3.5},
        "AAA": {"name": "LD7", "max_net": 4506, "volume": 7.2},
        "AKN": {"name": "LD8", "max_net": 2344, "volume": 5.5},
        "AAP": {"name": "LD6", "max_net": 3061, "volume": 7.2},
        "AMA": {"name": "LD9", "max_net": 6624, "volume": 11.6},
    }
    
    options = []
    
    for uld_type, spec in uld_specs.items():
        # Calculate ULDs needed
        ulds_by_weight = (cargo_weight / spec["max_net"])
        ulds_by_weight_rounded = int(ulds_by_weight) + (1 if ulds_by_weight % 1 > 0 else 0)
        
        ulds_by_volume = (cargo_volume / spec["volume"])
        ulds_by_volume_rounded = int(ulds_by_volume) + (1 if ulds_by_volume % 1 > 0 else 0)
        
        ulds_required = max(ulds_by_weight_rounded, ulds_by_volume_rounded)
        
        # Calculate utilization
        weight_util = (cargo_weight / (ulds_required * spec["max_net"])) * 100
        volume_util = (cargo_volume / (ulds_required * spec["volume"])) * 100
        avg_util = (weight_util + volume_util) / 2
        
        options.append({
            "type": uld_type,
            "name": spec["name"],
            "quantity": ulds_required,
            "weight_util": weight_util,
            "volume_util": volume_util,
            "avg_util": avg_util
        })
    
    # Sort by average utilization (descending)
    options.sort(key=lambda x: x["avg_util"], reverse=True)
    
    result = "ULD Options Comparison:\n\n"
    
    for idx, opt in enumerate(options, 1):
        marker = "🏆 RECOMMENDED" if idx == 1 else f"  Option {idx}"
        result += f"{marker}: {opt['quantity']} x {opt['type']} ({opt['name']})\n"
        result += f"  - Weight utilization: {opt['weight_util']:.1f}%\n"
        result += f"  - Volume utilization: {opt['volume_util']:.1f}%\n"
        result += f"  - Average utilization: {opt['avg_util']:.1f}%\n\n"
    
    best = options[0]
    result += f"Recommendation: Use {best['quantity']} x {best['type']} ({best['name']}) for optimal utilization"
    
    return result
