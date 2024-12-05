
from flask import Flask, send_from_directory
import sqlite3

app = Flask(__name__, static_folder='frontend/build')

DATABASE = 'database/lithology_codes.db'


def query_database(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_other(path):
    return send_from_directory(app.static_folder, path)


@app.route('/api/primary_categories', methods=['GET'])
def get_primary_categories():
    categories = query_database("SELECT * FROM PrimaryCategory")
    return jsonify([dict(row) for row in categories])


@app.route('/api/subcategories/<int:primary_category_id>', methods=['GET'])
def get_subcategories(primary_category_id):
    subcategories = query_database("SELECT * FROM SubCategory WHERE primary_category_id = ?", [primary_category_id])
    return jsonify([dict(row) for row in subcategories])


@app.route('/api/options/<int:subcategory_id>', methods=['GET'])
def get_options(subcategory_id):
    options = query_database("SELECT * FROM Options WHERE subcategory_id = ?", [subcategory_id])
    return jsonify([dict(row) for row in options])


@app.route('/api/build_code', methods=['POST'])
def build_code():
    data = request.json
    primary_code = data.get('primary_code', '').upper()
    selections = data.get('selections', {})
    code_parts = [primary_code]
    for subcategory_id, selected_options in selections.items():
        if isinstance(selected_options, list):
            # Multi-choice subcategory
            code_parts.append(f"({''.join(selected_options)})")
        else:
            # Single-choice subcategory
            code_parts.append(selected_options)
    return jsonify({"capture_code": ''.join(code_parts)})


if __name__ == '__main__':
    app.run(debug=True)
