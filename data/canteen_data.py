# data/canteen_data.py

MENU = [
    {"id": 1, "name": "Classic Burger", "price": 120, "calories": 450, "stall": "Counter 1", "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400"},
    {"id": 2, "name": "Cheese Pizza", "price": 250, "calories": 800, "stall": "Pizza Oven", "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400"},
    {"id": 3, "name": "Garden Salad", "price": 80, "calories": 150, "stall": "Juice Bar", "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400"},
    {"id": 4, "name": "Pasta Alfredo", "price": 180, "calories": 600, "stall": "Counter 1", "image": "https://images.unsplash.com/photo-1645112481338-358899371841?w=400"},
    {"id": 5, "name": "Cold Coffee", "price": 60, "calories": 200, "stall": "Juice Bar", "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=400"},
]

CANTEEN_MAP = {
    'Entrance': {'Counter 1': 2, 'Juice Bar': 5},
    'Counter 1': {'Entrance': 2, 'Pizza Oven': 1, 'Tables': 3},
    'Juice Bar': {'Entrance': 5, 'Tables': 4},
    'Pizza Oven': {'Counter 1': 1, 'Tables': 2},
    'Tables': {'Counter 1': 3, 'Juice Bar': 4, 'Pizza Oven': 2}
}