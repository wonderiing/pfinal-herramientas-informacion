from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

tickets_db = [
    {"id": 1, "title": "Error de inicio de sesión", "comments": ["Revisar credenciales de usuario", "El problema persiste en la versión móvil"]},
    {"id": 2, "title": "Lentitud en reportes", "comments": ["Optimizar consulta SQL en el módulo de reportes"]}
]

@app.route('/')
def home():
    return jsonify({"message": "FixIt Solutions Helpdesk API v1.0", "endpoints": ["/api/tickets", "/api/tickets/<id>/comment"]})

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    return jsonify(tickets_db)

@app.route('/api/tickets/<int:ticket_id>/comment', methods=['POST'])
def add_comment(ticket_id):
    data = request.get_json() or {}
    comment_text = data.get('comment', '')
    
    ticket = next((t for t in tickets_db if t["id"] == ticket_id), None)
    if not ticket:
        return jsonify({"error": "Ticket no encontrado"}), 404
        
    ticket["comments"].append(comment_text)
    
    html_response = f"<h3>Comentario agregado exitosamente al ticket {ticket_id}</h3><p>{comment_text}</p>"
    return render_template_string(html_response), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
