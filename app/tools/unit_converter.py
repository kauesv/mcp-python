"""
Tool para converter unidades de medida comuns.
"""

from typing import Dict, Any, Union


async def convert_units(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """
    Converte valores entre diferentes unidades de medida.

    Argumentos:
        value: O valor numérico para converter
        from_unit: A unidade de origem (ex: "km", "miles", "kg", "lbs")
        to_unit: A unidade de destino (ex: "m", "km", "g", "oz")

    Retorna:
        Dicionário com o valor convertido e informações sobre a conversão
    """
    
    # Dicionários de conversão para diferentes categorias
    length_conversions = {
        "km": {"m": 1000, "miles": 0.621371, "ft": 3280.84, "in": 39370.1},
        "m": {"km": 0.001, "miles": 0.000621371, "ft": 3.28084, "in": 39.3701},
        "miles": {"km": 1.60934, "m": 1609.34, "ft": 5280, "in": 63360},
        "ft": {"km": 0.0003048, "m": 0.3048, "miles": 0.000189394, "in": 12},
        "in": {"km": 0.0000254, "m": 0.0254, "miles": 0.000015783, "ft": 0.0833333}
    }
    
    weight_conversions = {
        "kg": {"g": 1000, "lbs": 2.20462, "oz": 35.274},
        "g": {"kg": 0.001, "lbs": 0.00220462, "oz": 0.035274},
        "lbs": {"kg": 0.453592, "g": 453.592, "oz": 16},
        "oz": {"kg": 0.0283495, "g": 28.3495, "lbs": 0.0625}
    }
    
    temperature_conversions = {
        "celsius": {"fahrenheit": lambda x: (x * 9/5) + 32, "kelvin": lambda x: x + 273.15},
        "fahrenheit": {"celsius": lambda x: (x - 32) * 5/9, "kelvin": lambda x: (x - 32) * 5/9 + 273.15},
        "kelvin": {"celsius": lambda x: x - 273.15, "fahrenheit": lambda x: (x - 273.15) * 9/5 + 32}
    }
    
    # Verificar se as unidades são válidas
    from_unit_lower = from_unit.lower()
    to_unit_lower = to_unit.lower()
    
    # Verificar conversões de comprimento
    if from_unit_lower in length_conversions and to_unit_lower in length_conversions[from_unit_lower]:
        conversion_factor = length_conversions[from_unit_lower][to_unit_lower]
        converted_value = value * conversion_factor
        category = "length"
    
    # Verificar conversões de peso
    elif from_unit_lower in weight_conversions and to_unit_lower in weight_conversions[from_unit_lower]:
        conversion_factor = weight_conversions[from_unit_lower][to_unit_lower]
        converted_value = value * conversion_factor
        category = "weight"
    
    # Verificar conversões de temperatura
    elif from_unit_lower in temperature_conversions and to_unit_lower in temperature_conversions[from_unit_lower]:
        conversion_func = temperature_conversions[from_unit_lower][to_unit_lower]
        converted_value = conversion_func(value)
        category = "temperature"
    
    else:
        return {
            "error": f"Conversão não suportada de '{from_unit}' para '{to_unit}'",
            "supported_categories": ["length", "weight", "temperature"],
            "supported_units": {
                "length": ["km", "m", "miles", "ft", "in"],
                "weight": ["kg", "g", "lbs", "oz"],
                "temperature": ["celsius", "fahrenheit", "kelvin"]
            }
        }
    
    return {
        "original_value": value,
        "original_unit": from_unit,
        "converted_value": round(converted_value, 4),
        "converted_unit": to_unit,
        "category": category,
        "success": True
    }
