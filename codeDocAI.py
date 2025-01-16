from flask import Flask, request, jsonify
from flask_cors import CORS
from meta_ai_api import MetaAI
from documentGeneration import CodeDocumentationGenerator
from llmParserGeneral import extractFeaturesFromCode

app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return "Welcome to CodeDoc-AI API!"

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'success': True, 'code': 200}), 200

@app.route('/generateDocumentation', methods=['POST'])
def generateDocumentation():
    try:
        if 'codefile' not in request.files:
            return jsonify({"error": "No codefile provided in the request"}), 400
        codefile = request.files['codefile']
        if codefile.filename == '':
            return jsonify({"error": "Empty file provided"}), 400
        try:
            code = codefile.read().decode('utf-8')
        except UnicodeDecodeError:
            return jsonify({"error": "Unable to decode the file. Ensure it is a valid text file."}), 400
        features = extractFeaturesFromCode(code)
        generator = CodeDocumentationGenerator(features)
        documentation = generator.generate_full_documentation()
        markdown_doc = generator.convertToMarkdown(documentation.get('message', ''))
        return markdown_doc, 200, {'Content-Type': 'text/markdown'}

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
