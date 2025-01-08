from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class CodeDocumentationGeneratorT5:
    def __init__(self, features):
        self.features = features
        # Load the T5 base model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("t5-base")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")

    def _generate_t5_text(self, prompt):
        """Generate text using T5 model."""
        inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model.generate(inputs, max_length=300, num_beams=5, early_stopping=True)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def generate_overview(self):
        """Generate an overview section."""
        language = self.features.get("language", "Unknown")
        prompt = f"Describe the programming language {language} and its use cases."
        t5_response = self._generate_t5_text(prompt)
        return f"### Overview\n\nThis code is written in **{language}**.\n\n{t5_response}\n"

    def generate_variables_doc(self):
        """Generate documentation for variables."""
        variables = self.features.get("variables", [])
        if not variables:
            return "### Variables\n\nNo variables were detected in the code.\n"

        docs = ["### Variables\n"]
        for var in variables:
            prompt = (
                f"Describe the variable `{var['name']}` of type `{var['type']}` "
                f"and its potential role in the program."
            )
            t5_response = self._generate_t5_text(prompt)
            docs.append(f"- **{var['name']}**: {t5_response.strip()}")
        return "\n".join(docs) + "\n"

    def generate_functions_doc(self):
        """Generate documentation for functions."""
        functions = self.features.get("functions", [])
        if not functions:
            return "### Functions\n\nNo functions were detected in the code.\n"

        docs = ["### Functions\n"]
        for func in functions:
            args = ", ".join(func['args']) if func['args'] else "No arguments"
            prompt = (
                f"Describe the function `{func['name']}` with arguments `{args}` "
                f"and its purpose in the program."
            )
            t5_response = self._generate_t5_text(prompt)
            docs.append(f"- **{func['name']}**: {t5_response.strip()}")
        return "\n".join(docs) + "\n"

    def generate_classes_doc(self):
        """Generate documentation for classes."""
        classes = self.features.get("classes", [])
        if not classes:
            return "### Classes\n\nNo classes were detected in the code.\n"

        docs = ["### Classes\n"]
        for cls in classes:
            bases = ", ".join(cls['base_classes']) if cls['base_classes'] else "No base classes"
            prompt = (
                f"Describe the class `{cls['name']}` with base classes `{bases}`. "
                f"Explain its purpose in object-oriented programming."
            )
            t5_response = self._generate_t5_text(prompt)
            docs.append(f"- **{cls['name']}**: {t5_response.strip()}")
        return "\n".join(docs) + "\n"

    def generate_full_documentation(self):
        """Combine all sections into a full documentation."""
        sections = [
            self.generate_overview(),
            self.generate_variables_doc(),
            self.generate_functions_doc(),
            self.generate_classes_doc(),
        ]
        return "\n".join(sections)


# Example Usage
if __name__ == "__main__":
    # Sample feature set
    import json

    with open("sampleCodeFeatures.txt", "r") as file:
        sample_features = json.load(file)

    # Initialize T5-enhanced documentation generator
    print("Generating documentation...")
    generator = CodeDocumentationGeneratorT5(sample_features)
    print("T5 model loaded successfully!")
    print("Generating overview section...")
    documentation = generator.generate_full_documentation()
    print("Overview section generated successfully!")
    # Save as a Markdown file
    with open("code_documentation_t5.md", "w") as file:
        file.write(documentation)

    print("Documentation generated successfully!")