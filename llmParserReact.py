import esprima
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class ReactFeatureExtractor:
    def __init__(self):
        self.features = {
            "Components": [],
            "Functions": [],
            "Variables": [],
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
                self.features["Components"].append({"name": node.id.name})

class ReactAnalysis:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("t5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

    def analyze_code(self, code):
        extractor = ReactFeatureExtractor()
        features = extractor.extract_features(code)
        return features

if __name__ == "__main__":
    sample_react_code = """
    import React from 'react';

    class Calculator extends React.Component {
        render() {
            return <div>Calculator</div>;
        }
    }

    const add = (a, b) => a + b;
    """
    analyzer = ReactAnalysis()
    result = analyzer.analyze_code(sample_react_code)
    print(json.dumps(result, indent=4))
