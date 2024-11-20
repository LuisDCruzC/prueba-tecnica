from flask import Flask, request, jsonify
from number_set import NumberSet

app = Flask(__name__)
number_set = NumberSet()

@app.route('/extract', methods=['POST'])
def extract_number():
    data = request.get_json()
    number = data.get('number')
    if not isinstance(number, int) or not (1 <= number <= 100):
        return jsonify({"error": "Número inválido. Debe ser un entero entre 1 y 100."}), 400
    try:
        number_set.extract(number)
        return jsonify({"message": f"Número {number} extraído correctamente."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/missing', methods=['GET'])
def missing_number():
    try:
        missing_number = number_set.find_missing_number()
        return jsonify({"missing_number": missing_number})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)