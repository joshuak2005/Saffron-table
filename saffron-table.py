"""
Saffron Table — Flask Backend
APIs: Menu, Orders, Contact Messages, Admin
Database: SQLite (saffron.db)
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend requests from any origin

DB_PATH = os.path.join(os.path.dirname(__file__), 'saffron.db')

# ─────────────────────────────────────────
#  DATABASE SETUP
# ─────────────────────────────────────────

def get_db():
    """Return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    return conn

def init_db():
    """Create tables and seed menu data if not already present."""
    conn = get_db()
    cur = conn.cursor()

    # ── MENU TABLE ──
    cur.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            category   TEXT NOT NULL,
            price      INTEGER NOT NULL,
            icon       TEXT,
            description TEXT,
            badge      TEXT,
            is_veg     INTEGER DEFAULT 1,
            available  INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ── ORDERS TABLE ──
    cur.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            customer_email TEXT,
            customer_phone TEXT,
            items_json   TEXT NOT NULL,
            total        INTEGER NOT NULL,
            status       TEXT DEFAULT 'pending',
            created_at   TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ── ORDER ITEMS TABLE ──
    cur.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id   INTEGER NOT NULL,
            dish_id    INTEGER NOT NULL,
            dish_name  TEXT NOT NULL,
            quantity   INTEGER NOT NULL,
            unit_price INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    ''')

    # ── CONTACTS TABLE ──
    cur.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            email      TEXT NOT NULL,
            subject    TEXT,
            message    TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ── SEED MENU DATA (only if empty) ──
    cur.execute('SELECT COUNT(*) FROM menu')
    if cur.fetchone()[0] == 0:
        menu_items = [
            ('Paneer Tikka',          'starters', 249, '🧆', 'Charred cottage cheese with mint chutney & onions',  'Bestseller', 1),
            ('Crispy Calamari',       'starters', 319, '🦑', 'Light tempura batter, served with sriracha aioli',    None,         0),
            ('Mezze Platter',         'starters', 399, '🫙', 'Hummus, baba ganoush, falafel & warm pita',           "Chef's Pick", 1),
            ('Butter Chicken',        'mains',    449, '🍛', 'Slow-cooked in tomato & cream sauce, best with naan', 'Bestseller', 0),
            ('Dal Makhani',           'mains',    329, '🍲', 'Black lentils simmered overnight with butter & spice', None,        1),
            ('Grilled Sea Bass',      'mains',    549, '🐟', 'Herb-marinated fillet, lemon butter, served w/ risotto',"Chef's Pick",0),
            ('Lamb Rogan Josh',       'mains',    519, '🍖', 'Kashmiri-style slow braised lamb, aromatic and rich',  None,        0),
            ('Margherita Pizza',      'pizza',    369, '🍕', 'San Marzano tomato, buffalo mozzarella, fresh basil',  None,        1),
            ('Spicy Pepperoni',       'pizza',    449, '🍕', 'Double pepperoni, jalapeños, smoked mozzarella',       'Bestseller', 0),
            ('Truffle Mushroom',      'pizza',    499, '🍕', 'Wild mushrooms, truffle oil, fontina cheese',          "Chef's Pick", 1),
            ('Gulab Jamun Cheesecake','desserts', 229, '🍮', 'New York cheesecake infused with rose syrup & pistachio','Signature',1),
            ('Kulfi Brûlée',          'desserts', 199, '🍦', 'Cardamom custard with caramelised sugar crust',        None,        1),
            ('Chocolate Lava Cake',   'desserts', 249, '🍫', 'Warm dark chocolate, salted caramel ice cream',        'Bestseller', 1),
            ('Mango Lassi',           'drinks',    129, '🥭', 'Thick Alphonso mango blended with chilled yoghurt',   None,        1),
            ('Masala Chai Latte',     'drinks',     99, '☕', 'House-blend spices, ginger, oat milk, served warm',   None,        1),
            ('Fresh Coconut Water',   'drinks',     89, '🥥', 'Young coconut, served chilled with a wedge of lime',  None,        1),
        ]
        cur.executemany('''
            INSERT INTO menu (name, category, price, icon, description, badge, is_veg)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', menu_items)

    conn.commit()
    conn.close()
    print("✅ Database initialised at", DB_PATH)


# ─────────────────────────────────────────
#  HELPER
# ─────────────────────────────────────────

def row_to_dict(row):
    return dict(row)


# ─────────────────────────────────────────
#  ROUTES — FRONTEND
# ─────────────────────────────────────────

@app.route('/')
def index():
    """Serve the frontend HTML."""
    return send_from_directory('.', 'saffron-table.html')


# ─────────────────────────────────────────
#  API — MENU
# ─────────────────────────────────────────

@app.route('/api/menu', methods=['GET'])
def get_menu():
    """GET /api/menu?category=mains  (or omit for all)"""
    category = request.args.get('category')
    conn = get_db()
    cur = conn.cursor()
    if category and category != 'all':
        cur.execute('SELECT * FROM menu WHERE available=1 AND category=?', (category,))
    else:
        cur.execute('SELECT * FROM menu WHERE available=1')
    items = [row_to_dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify({'success': True, 'data': items, 'count': len(items)})


@app.route('/api/menu/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    """GET /api/menu/4 — single dish"""
    conn = get_db()
    row = conn.execute('SELECT * FROM menu WHERE id=?', (dish_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'success': False, 'error': 'Dish not found'}), 404
    return jsonify({'success': True, 'data': row_to_dict(row)})


# ─────────────────────────────────────────
#  API — ORDERS
# ─────────────────────────────────────────

@app.route('/api/orders', methods=['POST'])
def place_order():
    """
    POST /api/orders
    Body: {
      "customer_name": "Arjun",
      "customer_email": "arjun@email.com",
      "customer_phone": "9876543210",
      "items": [ { "id": 1, "name": "Paneer Tikka", "price": 249, "qty": 2 }, ... ]
    }
    """
    data = request.get_json()
    if not data or 'items' not in data or not data['items']:
        return jsonify({'success': False, 'error': 'Order must contain at least one item'}), 400

    items = data['items']
    total = sum(item['price'] * item['qty'] for item in items)

    conn = get_db()
    cur = conn.cursor()

    # Insert order
    cur.execute('''
        INSERT INTO orders (customer_name, customer_email, customer_phone, items_json, total, status)
        VALUES (?, ?, ?, ?, ?, 'confirmed')
    ''', (
        data.get('customer_name', 'Guest'),
        data.get('customer_email', ''),
        data.get('customer_phone', ''),
        json.dumps(items),
        total
    ))
    order_id = cur.lastrowid

    # Insert individual order items
    for item in items:
        cur.execute('''
            INSERT INTO order_items (order_id, dish_id, dish_name, quantity, unit_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, item['id'], item['name'], item['qty'], item['price']))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Order placed successfully!',
        'order_id': order_id,
        'total': total,
        'estimated_delivery': '25–35 minutes'
    }), 201


@app.route('/api/orders', methods=['GET'])
def get_orders():
    """GET /api/orders — list all orders (admin use)"""
    conn = get_db()
    orders = [row_to_dict(r) for r in conn.execute(
        'SELECT * FROM orders ORDER BY created_at DESC'
    ).fetchall()]
    conn.close()
    # Parse items_json back to list
    for o in orders:
        o['items'] = json.loads(o['items_json'])
    return jsonify({'success': True, 'data': orders, 'count': len(orders)})


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """GET /api/orders/5 — single order with items"""
    conn = get_db()
    order = conn.execute('SELECT * FROM orders WHERE id=?', (order_id,)).fetchone()
    if not order:
        conn.close()
        return jsonify({'success': False, 'error': 'Order not found'}), 404
    order_dict = row_to_dict(order)
    order_dict['items'] = json.loads(order_dict['items_json'])
    order_dict['order_items'] = [row_to_dict(r) for r in conn.execute(
        'SELECT * FROM order_items WHERE order_id=?', (order_id,)
    ).fetchall()]
    conn.close()
    return jsonify({'success': True, 'data': order_dict})


@app.route('/api/orders/<int:order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    """PATCH /api/orders/5/status  Body: {"status": "delivered"}"""
    data = request.get_json()
    valid_statuses = ['pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled']
    status = data.get('status')
    if status not in valid_statuses:
        return jsonify({'success': False, 'error': f'Status must be one of {valid_statuses}'}), 400
    conn = get_db()
    conn.execute('UPDATE orders SET status=? WHERE id=?', (status, order_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'Order #{order_id} status updated to {status}'})


# ─────────────────────────────────────────
#  API — CONTACT
# ─────────────────────────────────────────

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """
    POST /api/contact
    Body: { "name": "Arjun", "email": "arjun@email.com", "subject": "Reservation", "message": "..." }
    """
    data = request.get_json()
    name    = data.get('name', '').strip()
    email   = data.get('email', '').strip()
    subject = data.get('subject', 'General Inquiry')
    message = data.get('message', '').strip()

    if not name or not email:
        return jsonify({'success': False, 'error': 'Name and email are required'}), 400

    conn = get_db()
    conn.execute(
        'INSERT INTO contacts (name, email, subject, message) VALUES (?, ?, ?, ?)',
        (name, email, subject, message)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f"Thank you {name}! We'll get back to you soon."}), 201


@app.route('/api/contact', methods=['GET'])
def get_contacts():
    """GET /api/contact — list all messages (admin)"""
    conn = get_db()
    rows = [row_to_dict(r) for r in conn.execute(
        'SELECT * FROM contacts ORDER BY created_at DESC'
    ).fetchall()]
    conn.close()
    return jsonify({'success': True, 'data': rows, 'count': len(rows)})


# ─────────────────────────────────────────
#  API — STATS (Admin Dashboard)
# ─────────────────────────────────────────

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """GET /api/stats — quick dashboard numbers"""
    conn = get_db()
    total_orders   = conn.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
    total_revenue  = conn.execute('SELECT COALESCE(SUM(total),0) FROM orders').fetchone()[0]
    total_contacts = conn.execute('SELECT COUNT(*) FROM contacts').fetchone()[0]
    total_dishes   = conn.execute('SELECT COUNT(*) FROM menu WHERE available=1').fetchone()[0]
    top_dish = conn.execute('''
        SELECT dish_name, SUM(quantity) as total_qty
        FROM order_items GROUP BY dish_name ORDER BY total_qty DESC LIMIT 1
    ''').fetchone()
    conn.close()
    return jsonify({
        'success': True,
        'data': {
            'total_orders':   total_orders,
            'total_revenue':  total_revenue,
            'total_contacts': total_contacts,
            'total_dishes':   total_dishes,
            'top_dish':       row_to_dict(top_dish) if top_dish else None
        }
    })


# ─────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    print("\n🍛 Saffron Table Backend Running")
    print("   Frontend : http://localhost:5000")
    print("   API Base : http://localhost:5000/api")
    print("\n   Endpoints:")
    print("   GET    /api/menu")
    print("   GET    /api/menu?category=mains")
    print("   GET    /api/menu/<id>")
    print("   POST   /api/orders")
    print("   GET    /api/orders")
    print("   GET    /api/orders/<id>")
    print("   PATCH  /api/orders/<id>/status")
    print("   POST   /api/contact")
    print("   GET    /api/contact")
    print("   GET    /api/stats\n")
    app.run(debug=True, port=5000)