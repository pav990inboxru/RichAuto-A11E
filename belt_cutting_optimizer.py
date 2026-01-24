import math
from itertools import combinations
from typing import List, Tuple, Dict, Any

class BeltCuttingOptimizer:
    """
    Optimizes cutting of roll material into belts to minimize waste.
    
    All dimensions and calculations are in millimeters (mm).
    """
    
    def __init__(self, roll_width: int, left_waste: int, right_waste: int):
        """
        Initialize the optimizer with roll parameters.
        
        Args:
            roll_width: Total width of the roll in mm
            left_waste: Waste on the left side in mm
            right_waste: Waste on the right side in mm
        """
        self.roll_width = roll_width
        self.left_waste = left_waste
        self.right_waste = right_waste
        self.useful_width = roll_width - left_waste - right_waste
        
    def validate_input(self, orders: List[Dict[str, int]]) -> None:
        """Validate input data."""
        if not orders:
            raise ValueError("Order table cannot be empty")
            
        for order in orders:
            if 'width' not in order or 'length' not in order or 'quantity' not in order:
                raise ValueError("Each order must contain width, length, and quantity")
                
            width = order['width']
            length = order['length']
            quantity = order['quantity']
            
            # Check if values are numbers
            if not isinstance(width, int) or not isinstance(length, int) or not isinstance(quantity, int):
                raise ValueError("Width, length, and quantity must be integers")
                
            # Check for positive values
            if width <= 0 or length <= 0 or quantity <= 0:
                raise ValueError("Width, length, and quantity must be greater than zero")
                
            # Check if belt width exceeds useful width
            if width > self.useful_width:
                raise ValueError(f"Belt width {width}mm exceeds useful roll width {self.useful_width}mm")
    
    def find_width_combinations(self, orders: List[Dict[str, int]]) -> List[Tuple[List[int], int]]:
        """
        Find all possible combinations of belts that fit within the useful width.
        
        Returns:
            List of tuples: (belt_indices, remaining_width)
        """
        valid_combinations = []
        num_belts = len(orders)
        
        # Check all possible combinations of belts
        for r in range(1, num_belts + 1):
            for combo in combinations(range(num_belts), r):
                # Calculate total width for this combination
                total_width = sum(orders[i]['width'] for i in combo)
                
                if total_width <= self.useful_width:
                    remaining_width = self.useful_width - total_width
                    valid_combinations.append((list(combo), remaining_width))
                    
        return valid_combinations
    
    def calculate_length_patterns(self, orders: List[Dict[str, int]], base_length: int) -> List[Dict[str, Any]]:
        """
        Calculate how many pieces of each belt length can be cut from a given base length.
        
        Args:
            orders: List of belt orders
            base_length: Length of the material piece to cut from
            
        Returns:
            List of dictionaries with length cutting info
        """
        patterns = []
        for order in orders:
            length = order['length']
            pieces_count = base_length // length
            leftover = base_length % length
            patterns.append({
                'order_index': orders.index(order),
                'belt_length': length,
                'pieces_per_base': pieces_count,
                'leftover': leftover
            })
        return patterns
    
    def find_optimal_solution(self, orders: List[Dict[str, int]]) -> Dict[str, Any]:
        """
        Find the optimal cutting pattern that minimizes waste and material usage.
        
        Args:
            orders: List of belt orders
            
        Returns:
            Dictionary with optimal solution details
        """
        # Validate inputs
        self.validate_input(orders)
        
        # Add index to each order for tracking
        indexed_orders = []
        for i, order in enumerate(orders):
            indexed_orders.append({**order, 'index': i})
        
        # Find all possible width combinations
        width_combinations = self.find_width_combinations(indexed_orders)
        
        # Generate possible base lengths based on LCM of belt lengths
        belt_lengths = [order['length'] for order in indexed_orders]
        base_lengths = []
        
        # Add multiples of each length up to a reasonable limit
        max_length = max(belt_lengths) if belt_lengths else 1000
        min_length = min(belt_lengths) if belt_lengths else 100
        
        # Generate candidate base lengths (multiples of belt lengths)
        for length in belt_lengths:
            for multiplier in range(1, max(10, (max_length * 3) // length + 1)):
                base_len = length * multiplier
                if base_len <= max_length * 5:  # Reasonable upper bound
                    base_lengths.append(base_len)
        
        base_lengths = sorted(set(base_lengths))  # Remove duplicates and sort
        
        best_solution = None
        min_roll_usage = float('inf')
        
        # Try all combinations of width layout and base length
        for width_combo, remaining_width in width_combinations:
            for base_length in base_lengths:
                # Calculate how many pieces of each needed length we can get from this base length
                combo_orders = [indexed_orders[i] for i in width_combo]
                length_patterns = self.calculate_length_patterns(combo_orders, base_length)
                
                # Calculate how many base cuts we need to fulfill orders for the belt types in this combo
                needed_cuts = 0
                fulfilled = {}
                
                # Initialize fulfilled dict for all orders with infinity
                for order in indexed_orders:
                    fulfilled[order['index']] = {
                        'needed_cuts': float('inf'),
                        'pieces_per_cut': 0,
                        'total_pieces': 0,
                        'pattern': None
                    }
                
                for i, pattern in enumerate(length_patterns):
                    # Get the original order index from the combo
                    original_order_idx = width_combo[i]  
                    order = indexed_orders[original_order_idx]
                    pieces_per_cut = pattern['pieces_per_base']
                    
                    if pieces_per_cut > 0:
                        needed_for_order = math.ceil(order['quantity'] / pieces_per_cut)
                        fulfilled[original_order_idx] = {
                            'needed_cuts': needed_for_order,
                            'pieces_per_cut': pieces_per_cut,
                            'total_pieces': needed_for_order * pieces_per_cut,
                            'pattern': pattern
                        }
                        
                        needed_cuts = max(needed_cuts, needed_for_order)
                
                # Check if this combination can fulfill all orders
                # Actually, we need to handle multiple patterns for a complete solution
                # A single width combo might not be able to fulfill all orders
                # We need to consider combinations of multiple width layouts
                
                # For now, let's implement a simplified version that tries to find the best single pattern
                can_fulfill_all = all(
                    fulfilled[order['index']]['needed_cuts'] != float('inf') 
                    for order in indexed_orders
                )
                
                if can_fulfill_all:
                    # Calculate total roll usage
                    roll_usage = base_length * needed_cuts
                    
                    # Calculate actual production and waste
                    actual_production = {}
                    total_waste_area = 0
                    total_waste_length = 0
                    
                    for order in indexed_orders:
                        idx = order['index']
                        fulfilled_info = fulfilled[idx]
                        actual_qty = fulfilled_info['total_pieces']
                        
                        # Calculate waste for this cut
                        waste_per_cut = fulfilled_info['pattern']['leftover'] if fulfilled_info['pattern'] else 0
                        total_waste_length += waste_per_cut * needed_cuts
                        
                        # Width waste
                        width_waste_per_cut = remaining_width
                        waste_area = width_waste_per_cut * base_length * needed_cuts
                        total_waste_area += waste_area
                        
                        actual_production[idx] = {
                            'width': order['width'],
                            'length': order['length'],
                            'needed': order['quantity'],
                            'produced': actual_qty,
                            'surplus': max(0, actual_qty - order['quantity'])
                        }
                    
                    # Consider this solution if it's better
                    if roll_usage < min_roll_usage:
                        min_roll_usage = roll_usage
                        best_solution = {
                            'total_roll_usage': roll_usage,
                            'base_length': base_length,
                            'needed_cuts': needed_cuts,
                            'width_combo': width_combo,
                            'remaining_width': remaining_width,
                            'fulfilled': fulfilled,
                            'actual_production': actual_production,
                            'total_waste_area': total_waste_area,
                            'total_waste_length': total_waste_length,
                            'usage_efficiency': (sum(o['width'] * o['length'] * o['quantity'] for o in orders) / 
                                               (self.useful_width * roll_usage)) * 100 if roll_usage > 0 else 0
                        }
        
        if best_solution is None:
            raise ValueError("No feasible solution found to fulfill all orders")
        
        return best_solution
    
    def generate_report(self, orders: List[Dict[str, int]]) -> str:
        """
        Generate a detailed report of the optimal cutting plan.
        
        Args:
            orders: List of belt orders
            
        Returns:
            Formatted report string
        """
        try:
            solution = self.find_optimal_solution(orders)
        except ValueError as e:
            return f"Error: {str(e)}"
        
        report = []
        report.append("=" * 60)
        report.append("ОРДЕР НА РЕМНИ:")
        report.append("-" * 60)
        report.append(f"{'Ширина (мм)':<12} {'Длина (мм)':<12} {'Количество':<10}")
        report.append("-" * 60)
        for order in orders:
            report.append(f"{order['width']:<12} {order['length']:<12} {order['quantity']:<10}")
        
        report.append("\n" + "=" * 60)
        report.append("ОБЩИЙ РАСХОД МАТЕРИАЛА:")
        report.append("-" * 60)
        report.append(f"Общая длина использованного рулона: {solution['total_roll_usage']} мм")
        
        report.append("\n" + "=" * 60)
        report.append("КАКИЕ ЗАГОТОВКИ НУЖНО РЕЗАТЬ:")
        report.append("-" * 60)
        report.append(f"{'№':<3} {'Длина заготовки (мм)':<20} {'Сколько раз резать':<20}")
        report.append("-" * 60)
        report.append(f"1 {solution['base_length']:<19} {solution['needed_cuts']:<20}")
        
        report.append(f"\n" + "=" * 60)
        report.append(f"ЗАГОТОВКА {solution['base_length']} мм ({solution['needed_cuts']} раз)")
        report.append("-" * 60)
        
        report.append("\nПО ШИРИНЕ (в одном ряду):")
        report.append("-" * 30)
        report.append(f"{'Ремень':<10} {'Ширина':<10} {'Кол-во'}")
        report.append("-" * 30)
        for i, idx in enumerate(solution['width_combo']):
            order = orders[idx]
            report.append(f"Тип {i+1:<6} {order['width']} мм{'':<7} 1")
        
        report.append(f"Отход по ширине: {solution['remaining_width']} мм")
        
        report.append("\nПО ДЛИНЕ:")
        report.append("-" * 50)
        report.append(f"{'Длина ремня':<15} {'Сколько штук из одной заготовки':<30}")
        report.append("-" * 50)
        for idx in solution['width_combo']:
            pattern = solution['fulfilled'][idx]['pattern']
            report.append(f"{pattern['belt_length']} мм{'':<10} {pattern['pieces_per_base']:<30}")
        
        total_leftover = sum(solution['fulfilled'][idx]['pattern']['leftover'] 
                            for idx in solution['width_combo'])
        report.append(f"Отход по длине: {total_leftover} мм")
        
        report.append(f"\n" + "=" * 60)
        report.append("ФАКТИЧЕСКИ ПРОИЗВЕДЕНО:")
        report.append("-" * 60)
        report.append(f"{'Ширина':<8} {'Длина':<8} {'Нужно':<8} {'Сделано':<10} {'Излишек'}")
        report.append("-" * 60)
        for order in orders:
            idx = order['index'] if 'index' in order else orders.index(order)
            prod_info = solution['actual_production'][idx]
            report.append(f"{prod_info['width']:<8} {prod_info['length']:<8} "
                         f"{prod_info['needed']:<8} {prod_info['produced']:<10} "
                         f"{prod_info['surplus']}")
        
        report.append(f"\n" + "=" * 60)
        report.append("ОТХОДЫ:")
        report.append("-" * 60)
        report.append(f"Суммарный отход по ширине: {solution['total_waste_area']} мм²")
        report.append(f"Суммарный отход по длине: {solution['total_waste_length']} мм")
        report.append(f"Процент использования материала: {solution['usage_efficiency']:.2f}%")
        
        return "\n".join(report)


def main():
    """Main function to demonstrate the optimizer."""
    # Initialize optimizer with roll parameters
    optimizer = BeltCuttingOptimizer(roll_width=640, left_waste=30, right_waste=30)
    
    # Define the order
    orders = [
        {'width': 50, 'length': 1200, 'quantity': 300},
        {'width': 80, 'length': 900, 'quantity': 150},
        {'width': 120, 'length': 1500, 'quantity': 100}
    ]
    
    # Generate and print the report
    report = optimizer.generate_report(orders)
    print(report)


if __name__ == "__main__":
    main()