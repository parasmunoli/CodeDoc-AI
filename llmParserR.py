import json

class RFeatureExtractor:
    def __init__(self):
        self.features = {
            "Functions": [],
            "Variables": [],
        }

    def extract_features(self, code):
        lines = code.split("\n")
        for line in lines:
            if "<-" in line:
                variable = line.split("<-")[0].strip()
                self.features["Variables"].append({"name": variable})
            elif "function" in line:
                function_name = line.split("<-")[0].strip()
                self.features["Functions"].append({"name": function_name})
        return self.features

if __name__ == "__main__":
    sample_r_code = """
    add <- function(a, b) {
        return(a + b)
    }

    x <- 5
    """
    extractor = RFeatureExtractor()
    result = extractor.extract_features(sample_r_code)
    print(json.dumps(result, indent=4))
