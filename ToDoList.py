```python
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

# Temporärer Datenspeicher während der Laufzeit
todo_lists = {}
todo_entries = {}

# Hilfsfunktionen für die Fehlerbehandlung
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

def validate_list_id(list_id):
    return list_id in todo_lists

def validate_entry_id(list_id, entry_id):
    if list_id in todo_entries:
        return any(entry['id'] == entry_id for entry in todo_entries[list_id])
    return False

# Route für die Hauptseite und Liste aller Todo-Listen
@app.route('/')
@app.route('/todo-lists')
def index():
    return jsonify(list(todo_lists.values()))

@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(list(todo_lists.values()))

# Endpunkt zum Abrufen aller Einträge einer bestimmten Liste
@app.route('/todo-list/<string:list_id>', methods=['GET'])
def get_list(list_id):
    if not validate_list_id(list_id):
        return error_response('Ungültige Listen-ID', 404)
    return jsonify(todo_entries.get(list_id, []))

# Endpunkt zum Löschen einer bestimmten Liste
@app.route('/todo-list/<string:list_id>', methods=['DELETE'])
def delete_list(list_id):
    if not validate_list_id(list_id):
        return error_response('Ungültige Listen-ID', 404)
    del todo_lists[list_id]
    del todo_entries[list_id]
    return jsonify({'message': 'Liste wurde gelöscht'}), 200

# Endpunkt zum Hinzufügen einer neuen Liste
@app.route('/todo-list', methods=['POST'])
def add_list():
    data = request.get_json()
    if not data or 'name' not in data:
        return error_response('Ungültige Listen-Daten', 406)
    list_id = str(uuid.uuid4())
    todo_lists[list_id] = {'id': list_id, 'name': data['name']}
    todo_entries[list_id] = []
    logging.debug(f"Liste hinzugefügt: {todo_lists[list_id]}")  # Loggen der hinzugefügten Liste
    return jsonify(todo_lists[list_id]), 201

# Endpunkt zum Hinzufügen eines neuen Eintrags in eine Liste
@app.route('/todo-list/<string:list_id>/entry', methods=['POST'])
def add_entry(list_id):
    if not validate_list_id(list_id):
        return error_response('Ungültige Listen-ID', 404)
    data = request.get_json()
    if 'name' not in data:
        return error_response('Ungültige Eintrags-Daten', 406)
    entry_id = str(uuid.uuid4())
    data['id'] = entry_id
    if list_id not in todo_entries:
        todo_entries[list_id] = []
    todo_entries[list_id].append(data)
    return jsonify(data), 201

# Endpunkt zum Aktualisieren eines bestimmten Eintrags in einer Liste
@app.route('/todo-list/<string:list_id>/entry/<string:entry_id>', methods=['PATCH'])
def update_entry(list_id, entry_id):
    if not validate_entry_id(list_id, entry_id):
        return error_response('Eintrag nicht gefunden', 404)
    data = request.get_json()
    for entry in todo_entries[list_id]:
        if entry['id'] == entry_id:
            entry.update(data)
            return jsonify(entry), 200
    return error_response('Eintrag nicht gefunden', 404)

# Endpunkt zum Löschen eines bestimmten Eintrags aus einer Liste
@app.route('/todo-list/<string:list_id>/entry/<string:entry_id>', methods=['DELETE'])
def delete_entry(list_id, entry_id):
    if not validate_entry_id(list_id, entry_id):
        return error_response('Eintrag nicht gefunden', 404)
    todo_entries[list_id] = [entry for entry in todo_entries[list_id] if entry['id'] != entry_id]
    return jsonify({'message': 'Eintrag gelöscht'}), 200

if __name__ == '__main__':
    # Starte den Flask-Server
    app.run(host='0.0.0.0', port=5000, debug=True)
```