import javalang
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class JavaFeatureExtractor:
    def __init__(self):
        self.features = {
            "Classes": [],
            "Methods": [],
            "Variables": [],
        }

    def extract_features(self, code):
        tree = javalang.parse.parse(code)
        for path, node in tree:
            if isinstance(node, javalang.tree.ClassDeclaration):
                self.features["Classes"].append({"name": node.name, "methods": []})
            elif isinstance(node, javalang.tree.MethodDeclaration):
                self.features["Methods"].append({"name": node.name, "return_type": node.return_type.name if node.return_type else "void"})
            elif isinstance(node, javalang.tree.VariableDeclarator):
                self.features["Variables"].append({"name": node.name})
        return self.features

class JavaAnalysis:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("t5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

    def analyze_code(self, code):
        extractor = JavaFeatureExtractor()
        features = extractor.extract_features(code)
        return features

if __name__ == "__main__":
    sample_java_code = """
    public class Calculator {
        public int add(int a, int b) {
            return a + b;
        }

        public int subtract(int a, int b) {
            return a - b;
        }
    }
    """
    analyzer = JavaAnalysis()
    result = analyzer.analyze_code(sample_java_code)
    print(json.dumps(result, indent=4))
