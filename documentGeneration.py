from markdownify import markdownify
from meta_ai_api import MetaAI


# from transformers import MarkupLMFeatureExtractor, MarkupLMTokenizerFast, MarkupLMProcessor


class CodeDocumentationGenerator:
    def __init__(self, features):
        self.features = features
        print("Initializing MetaAI text generator...")
        self.text_generator = MetaAI()
        print("MetaAI text generator initialized successfully!")

    def generate_text(self, prompt):
        """Generate text using MetaAI text generator."""
        return self.text_generator.prompt(prompt)

    def generate_full_documentation(self):
        """Generate full documentation using features."""
        prompt = (
            f"Generate a detailed elaborated description for code with the following features: {self.features}. "
            "Include sections for overview, variables, functions, and classes, and provide in-depth explanations and response in HTML format providing entire code documentation in html format."
        )
        response = self.generate_text(prompt)
        # markdownContent = self.text_generator.prompt(f"Arrange in markdown format: {response}")
        # print(markdownContent)
        return response

    def convertToMarkdown(self, text):
        markdownCode = markdownify(text)
        print("Markdown Code: ", markdownCode)
        return markdownCode


# Example Usage
if __name__ == "__main__":
    import json

    with open("updatedSampleAnalysis.json", "r") as file:
        sample_features = json.load(file)

    print("Generating documentation...")
    generator = CodeDocumentationGenerator(sample_features)
    print("Documentation generator initialized successfully!")
    documentation = generator.generate_full_documentation()
    print("Documentation generated successfully!")
    print("Documentation:",documentation.get('message', ''))
    print("Converting to markdown...")
    documentation = generator.convertToMarkdown(documentation.get('message', ''))
    print("Documentation converted to markdown successfully!")


    with open("codeDocumentation.md", "w") as file:
        file.write(documentation)

    print("Documentation saved as codeDocumentation.md!")
