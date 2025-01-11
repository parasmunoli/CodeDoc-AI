import esprima
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class JSFeatureExtractor:
    def __init__(self):
        self.features = {
            "Functions": [],
            "Variables": [],
            "Classes": [],
        }

    def extract_features(self, code):
        tree = esprima.parseScript(code, tolerant=True)
        self._traverse_tree(tree.body)
        return self.features

    def _traverse_tree(self, nodes):
        for node in nodes:
            if node.type == "FunctionDeclaration":
                self.features["Functions"].append({"name": node.id.name, "params": [p.name for p in node.params]})
            elif node.type == "VariableDeclaration":
                for decl in node.declarations:
                    self.features["Variables"].append({"name": decl.id.name, "kind": node.kind})
            elif node.type == "ClassDeclaration":
                self.features["Classes"].append({"name": node.id.name})

class JSAnalysis:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("t5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

    def analyze_code(self, code):
        extractor = JSFeatureExtractor()
        features = extractor.extract_features(code)
        return features

if __name__ == "__main__":
    sample_js_code = """
    class Calculator {
        add(a, b) {
            return a + b;
        }

        subtract(a, b) {
            return a - b;
        }
    }

    const num = 10;
    function greet() {
        console.log("Hello, World!");
    }
    """
    analyzer = JSAnalysis()
    result = analyzer.analyze_code(sample_js_code)
    print(json.dumps(result, indent=4))
