from abc import ABC
from enum import Enum
from typing import Dict, List

class Category(Enum):
    STARTER = 'Starter'
    MAIN_COURSE = 'Main Course'
    DESSERT = 'Dessert'

class MenuItem:
    def __init__(self, name: str, price: float, is_veg: bool, category: Category):
        if price < 0:
            raise ValueError("Item price cannot be -ve")
        
        self.name = name
        self.price = price
        self.is_veg = is_veg
        self.category = category

    def __str__(self) -> str:
        return f"{self.name} - {self.price} Rs - {'Veg' if self.is_veg else 'Non-veg'} - {self.category.value}"

class Menu:
    def __init__(self) -> None:
        self.items: Dict[str, MenuItem] = {}

    def add_item(self, item: MenuItem):
        self.items[item.name] = item

    def update_item_price(self, name: str, new_price: float):
        if(new_price < 0):
            raise ValueError("Price cannot be negative")
        
        if name in self.items:
            self.items[name].price = new_price

        else:
            raise ValueError("Item does not exist.")

    def remove_item(self, name: str):
        if name in self.items:
            del self.items[name]
        else:
            raise ValueError("Item does not exist.")
        
    def get_items(self, is_veg = None, category = None) -> List[MenuItem]:
        filtered_items = list(self.items.values())
        if is_veg is not None:
            filtered_items = [item for item in filtered_items if item.is_veg == is_veg]

        if category is not None:
            filtered_items = [item for item in filtered_items if item.category == category]

        return filtered_items
    
    def __str__(self) -> str:
        return (str(self.items))


class Table:
    def __init__(self, table_number:int) -> None:
        self.table_number = table_number
        self.is_occupied = False
        self.reservation_name = None
        self.orders: List[Order] = []

    def occupy(self, reservation_name: str = None):
        if self.is_occupied:
            raise ValueError("Table is already occupied")
        
        self.is_occupied = True
        self.reservation_name = reservation_name

    def vacate(self):
        self.is_occupied = False
        self.reservation_name = None
        self.orders = []

    def add_order(self, order: 'Order'):
        self.orders.append(order)

    def list_orders(self):
        return "\n".join(str(self.orders))

    def __str__(self) -> str:
        status = "Occupied" if self.is_occupied else "Vacant"
        return f"Table {self.table_number} - {status}"
    
class OrderItem:
    def __init__(self, item: MenuItem, quantity: int) -> None:
        self.item = item
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.item.name} * {self.quantity} = {self.item.price * self.quantity} Rs"
    
class Order:
    def __init__(self) -> None:
        self.items: Dict[str, OrderItem] = {}
        self.is_prepared = False

    def add_item(self, item: MenuItem, quantity: int):
        if item.name in self.items:
            self.items[item.name].quantity += quantity

        else:
            self.items[item.name] = OrderItem(item, quantity)

    def remove_item(self, item_name: str):
        if item_name in self.items:
            del self.items[item_name]
        
        else:
            raise ValueError("Item not found in the order")
        
    def update_item_quantity(self, item_name: str, quantity: int):
        if item_name in self.items:
            self.items[item_name].quantity = quantity
        else:
            raise ValueError("Item not found")
        
    def calculate_total(self, tax_rate: float, additional_charges: float = 0.0) -> float:
        subtotal = sum(item.item.price * item.quantity for item in self.items.values())
        tax = subtotal * tax_rate
        total = subtotal + tax + additional_charges
        return total
    
    def __str__(self) -> str:
        return str(self.items.values())

class PaymentStrategy(ABC):
    def calculate_total(self, order: Order) -> float:
        pass

class CashPayment(PaymentStrategy):
    def calculate_total(self, order: Order) -> float:
        return order.calculate_total(tax_rate=0.1)
    
class CardPayment(PaymentStrategy):
    def calculate_total(self, order: Order) -> float:
        base_total = order.calculate_total(tax_rate=0.1)
        processing_fee = base_total * 0.01
        return base_total + processing_fee
    
class UPIPayment(PaymentStrategy):
    def calculate_total(self, order: Order) -> float:
        return order.calculate_total(tax_rate=0.1)
    
class Payment:
    def __init__(self, strategy: PaymentStrategy) -> None:
        self.strategy = strategy

    def calculate_total(self, order: Order) -> float:
        return self.strategy.calculate_total(order)


class Restaurant:
    def __init__(self):
        self.tables: List[Table] = []
        self.menu = Menu()
        self.kitchen_orders: List[Order] = []

    def add_table(self, table_number: int):
        self.tables.append(Table(table_number))

    def get_vacant_table(self) -> Table:
        for table in self.tables:
            if not table.is_occupied:
                return table
            
        raise ValueError("No vacant tables available")
    
    def get_table_status(self):
        return "\n".join(str(table) for table in self.tables)

    def reserve_table(self, table_number: int):
        table = self._find_table(table_number)
        if table:
            if table.is_occupied:
                raise ValueError("Table is already occupied")
            
        else:
            raise ValueError("Table not found")
        
    def occupy_table(self, table_number: int):
        table = self._find_table(table_number)
        if table:
            if table.is_occupied:
                raise ValueError("Table is already occupied")
            table.occupy()

        else:
            raise ValueError("Table not found")
            
    def vacate_table(self, table_number: int):
        table = self._find_table(table_number)
        if table:
            table.vacate()
        else:
            raise ValueError("Table not found")
        
    def _find_table(self, table_number: int) -> Table:
        for table in self.tables:
            if table.table_number == table_number:
                return table
        return None
    
    def add_order(self, table_number: int, order: Order):
        table = self._find_table(table_number)
        if table:
            table.add_order(order)
            self.kitchen_orders.append(order)
        else:
            raise ValueError("Table not found")
        
    def get_kitchen_orders(self):
        print(self.kitchen_orders)

    def browse_menu(self, is_veg: bool = None, category: Category = None):
        return self.menu.get_items(is_veg, category)
    
    def remove_item_from_order(self, table_number: int, item_name: str):
        table = self._find_table(table_number)
        if table:
            for order in table.orders:
                try:
                    order.remove_item(item_name)
                except ValueError as e:
                    raise e
                else:
                    return
            raise ValueError("Item not found in any order")
        else:
            raise ValueError("Table not found")
        
    def update_item_quantity_in_order(self, table_number: int, item_name: str, quantity: int):
        table = self._find_table(table_number)
        if table:
            for order in table.orders:
                try:
                    order.update_item_quantity(item_name, quantity)
                except ValueError as e:
                    raise e
                else:
                    return
            raise ValueError("Item not found")

    def mark_order_prepared(self, order: Order):
        if order in self.kitchen_orders:
            self.kitchen_orders.remove(order)
            order.is_prepared = True

            for table in self.tables:
                if order in table.orders:
                    table.vacate()
                    break
        else:
            raise ValueError("Order not found")
        
    def calculate_bill(self, table_number: int, payment_strategy: PaymentStrategy):
        table = self._find_table(table_number)
        if table:
            total = 0.0
            for order in table.orders:
                payment = Payment(payment_strategy)
                total += payment.calculate_total(order)

            return total

        else:
            raise ValueError("Table not found") 
        
    def __str__(self) -> str:
        return f"Restaurant with {len(self.tables)} tables"
    
if __name__ == "__main__":
    restaurant = Restaurant()

    #Add tables
    restaurant.add_table(1)
    restaurant.add_table(2)
    restaurant.add_table(3)
    print ("Tables added")
    print(restaurant.get_table_status())

    #Add items
    item1 = MenuItem("Spaghetti", 499, True, Category.STARTER)
    item2 = MenuItem("Chicken", 699, False, Category.MAIN_COURSE)
    item3 = MenuItem("Ice cream", 199, True, Category.DESSERT)

    restaurant.menu.add_item(item1)
    restaurant.menu.add_item(item2)
    restaurant.menu.add_item(item3)
    print("\nMenu:")
    print(restaurant.menu)

    restaurant.menu.update_item_price("Spaghetti", 599)
    print(restaurant.menu)
    
    restaurant.menu.remove_item("Ice cream")
    vacant_table = restaurant.get_vacant_table()
    restaurant.occupy_table(vacant_table.table_number)
    print(restaurant.get_table_status())

    order1 = Order
    restaurant.add_order(1, order1)
    
    restaurant.get_kitchen_orders()
    restaurant.mark_order_prepared(order1)
    restaurant.get_kitchen_orders()
    print(restaurant.get_table_status())


