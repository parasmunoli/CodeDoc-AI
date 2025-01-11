from pydart_analyzer import analyze_dart_code
import json

class DartFeatureExtractor:
    def __init__(self):
        self.features = {
            "Classes": [],
            "Functions": [],
            "Variables": [],
        }

    def extract_features(self, code):
        analysis_result = analyze_dart_code(code)
        for entity in analysis_result:
            if entity['type'] == 'class':
                self.features["Classes"].append({"name": entity["name"]})
            elif entity['type'] == 'function':
                self.features["Functions"].append({"name": entity["name"]})
            elif entity['type'] == 'variable':
                self.features["Variables"].append({"name": entity["name"]})
        return self.features

if __name__ == "__main__":
    sample_dart_code = """
    class Calculator {
        int add(int a, int b) => a + b;
    }
    """
    extractor = DartFeatureExtractor()
    result = extractor.extract_features(sample_dart_code)
    print(json.dumps(result, indent=4))
