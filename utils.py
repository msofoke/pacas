def calculate_bundle_metrics(bundle, config):
    """Calcular métricas y precios de una paca"""
    total_cost = bundle.get('total_cost', 0)
    total_pieces = bundle.get('total_pieces', 0)
    additional_expenses = bundle.get('additional_expenses', {})
    classification = bundle.get('classification', {})
    
    # Calculate total additional expenses
    total_additional_expenses = sum(additional_expenses.values())
    
    # Calculate cost per piece
    total_cost_with_expenses = total_cost + total_additional_expenses
    cost_per_piece = total_cost_with_expenses / total_pieces if total_pieces > 0 else 0
    
    # Get profit percentages from config
    profit_percentages = config.get('profit_percentages', {
        'premium': 80,
        'regular': 50,
        'economica': 30,
        'rechazo': 0
    })
    
    # Calculate prices by quality
    quality_breakdown = []
    total_minimum_revenue = 0
    total_ideal_revenue = 0
    
    by_quality = classification.get('by_quality', {})
    
    for quality, pieces in by_quality.items():
        if pieces > 0:
            profit_percentage = profit_percentages.get(quality, 0)
            
            # Minimum price (just to recover costs)
            minimum_price = cost_per_piece
            
            # Ideal price (with profit margin)
            ideal_price = cost_per_piece * (1 + profit_percentage / 100)
            
            # Total revenues
            minimum_revenue = minimum_price * pieces
            ideal_revenue = ideal_price * pieces
            
            total_minimum_revenue += minimum_revenue
            total_ideal_revenue += ideal_revenue
            
            quality_breakdown.append({
                'quality': quality,
                'pieces': pieces,
                'cost_per_piece': cost_per_piece,
                'minimum_price': minimum_price,
                'ideal_price': ideal_price,
                'minimum_revenue': minimum_revenue,
                'ideal_revenue': ideal_revenue,
                'profit_percentage': profit_percentage
            })
    
    # Calculate profits
    minimum_profit = total_minimum_revenue - total_cost_with_expenses
    ideal_profit = total_ideal_revenue - total_cost_with_expenses
    
    # Calculate profit margins
    minimum_profit_margin = (minimum_profit / total_cost_with_expenses * 100) if total_cost_with_expenses > 0 else 0
    ideal_profit_margin = (ideal_profit / total_cost_with_expenses * 100) if total_cost_with_expenses > 0 else 0
    
    return {
        'total_cost': total_cost,
        'total_additional_expenses': total_additional_expenses,
        'total_cost_with_expenses': total_cost_with_expenses,
        'cost_per_piece': cost_per_piece,
        'quality_breakdown': quality_breakdown,
        'total_minimum_revenue': total_minimum_revenue,
        'total_ideal_revenue': total_ideal_revenue,
        'minimum_profit': minimum_profit,
        'ideal_profit': ideal_profit,
        'total_estimated_profit': ideal_profit,  # Use ideal profit as estimated
        'minimum_profit_margin': minimum_profit_margin,
        'ideal_profit_margin': ideal_profit_margin
    }

def format_currency(amount):
    """Formatear cantidad como moneda con separadores de miles"""
    return f"${amount:,.2f}"

def format_percentage(percentage):
    """Formatear porcentaje"""
    return f"{percentage:.1f}%"

def format_number(number):
    """Formatear número con separadores de miles"""
    return f"{number:,.2f}" if isinstance(number, float) else f"{number:,}"
