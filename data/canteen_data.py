# data/canteen_data.py

MENU = [
    {"id": 1, "name": "Classic Burger", "price": 120, "calories": 450, "stall": "Counter 1", "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600"},
    {"id": 2, "name": "Cheese Pizza", "price": 250, "calories": 800, "stall": "Pizza Oven", "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600"},
    {"id": 3, "name": "Garden Salad", "price": 80, "calories": 150, "stall": "Juice Bar", "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600"},
    {"id": 4, "name": "Pasta Alfredo", "price": 180, "calories": 600, "stall": "Counter 1", "image": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=600"},
    {"id": 5, "name": "Cold Coffee", "price": 60, "calories": 200, "stall": "Juice Bar", "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=600"},
    {"id": 6, "name": "Tandoori Paneer", "price": 190, "calories": 400, "stall": "Counter 1", "image": "https://images.unsplash.com/photo-1567188040759-fb8ad01dc318?w=800"},
    {"id": 7, "name": "Pepperoni Pizza", "price": 280, "calories": 850, "stall": "Pizza Oven", "image": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=800"},
    {"id": 8, "name": "Mango Lassi", "price": 75, "calories": 300, "stall": "Juice Bar", "image": "https://images.unsplash.com/photo-1546173159-315724a31696?w=800"},
    {"id": 9, "name": "Veggie Wrap", "price": 110, "calories": 320, "stall": "Counter 1", "image": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=800"},
    {"id": 10, "name": "Garlic Bread", "price": 90, "calories": 280, "stall": "Pizza Oven", "image": "https://images.unsplash.com/photo-1541745537411-b8046dc6d66c?w=800"},
    {"id": 11, "name": "Fruit Platter", "price": 130, "calories": 180, "stall": "Juice Bar", "image": "https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=600"},
]

CANTEEN_MAP = {
    'Entrance': {'Counter 1': 2, 'Juice Bar': 5},
    'Counter 1': {'Entrance': 2, 'Pizza Oven': 1, 'Tables': 3},
    'Juice Bar': {'Entrance': 5, 'Tables': 4},
    'Pizza Oven': {'Counter 1': 1, 'Tables': 2},
    'Tables': {'Counter 1': 3, 'Juice Bar': 4, 'Pizza Oven': 2}
}