from meta_ai_api import MetaAI


class CodeDocumentationGenerator:
    def __init__(self, features):
        self.features = features
        print("Initializing MetaAI text generator...")
        self.text_generator = MetaAI()
        print("MetaAI text generator initialized successfully!")

    def _generate_text(self, prompt):
        """Generate text using MetaAI text generator."""
        return self.text_generator.prompt(prompt)

    def generate_full_documentation(self):
        """Generate full documentation using features."""
        prompt = (
            f"Generate a detailed elaborated description for code with the following features: {self.features}. "
            "Include sections for overview, variables, functions, and classes, and provide in-depth explanations and response in markdown format providing entire code documentation."
        )
        responce = self._generate_text(prompt)
        # markdownContent = self.text_generator.prompt(f"Arrange in markdown format: {responce}")
        # print(markdownContent)
        return responce


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

    with open("codeDocumentation.md", "w") as file:
        file.write(documentation)

    print("Documentation saved as codeDocumentation.md!")
