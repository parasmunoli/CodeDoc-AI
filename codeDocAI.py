from flask import Flask, request, jsonify

from documentGeneration import CodeDocumentationGenerator
from llmParserGeneral import extractFeaturesFromCode

app = Flask(__name__)

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
        code = codefile.read().decode('utf-8')

        features = extractFeaturesFromCode(code)
        print("Features: ",features)
        generator = CodeDocumentationGenerator(features)
        documentation = generator.generate_full_documentation()
        markdown_doc = generator.convertToMarkdown(documentation.get('message', ''))

        response = app.response_class(
            response=markdown_doc,
            status=200,
            mimetype='text/markdown'
        )
        response.headers['Content-Disposition'] = 'attachment; filename=documentation.md'
        return response

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
