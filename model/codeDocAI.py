from flask import Flask, request, jsonify
from flask_cors import CORS

from documentGeneration import CodeDocumentationGenerator
# from llmParserGeneral import extractFeaturesFromCode

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
        if 'githubLink' not in request.json:
            return jsonify({"error": "No githubLink provided in the request"}), 400

        githubLink = request.json['githubLink']

        # features = extractFeaturesFromCode(code)
        generator = CodeDocumentationGenerator()
        documentation = generator.generate_full_documentation(githubLink)
        markdown_doc = generator.convertToMarkdown(documentation.get('message', ''))
        return markdown_doc, 200, {'Content-Type': 'text/markdown'}

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
