from markdownify import markdownify
from meta_ai_api import MetaAI
from transformers import T5Tokenizer, T5ForConditionalGeneration

class CodeDocumentationGenerator:
    def __init__(self):
        # self.features = features
        print("Initializing AI text generator...")
        self.text_generator = MetaAI()
        print("AI text generator initialized successfully!")

    def generate_full_documentation(self, link, projectdesc):
        """Generate full documentation using features."""
        print("Generating Basic Skeleton for documentation...")
        prompt = (
            f"""response only in HTML code visit {link} and generate Project title only for the project do not generate any description use <h1>."""
        )
        basicDoc = self.text_generator.prompt(prompt)
        description = self.elaboratedDesc(link)
        toc = '''<h2>Table of Contents</h2>
                <li>Install and Run the Project</li>
                <li>Use the Project</li>
                <li>Credits</li>
                <li>License</li>
                <li>Contribution</li>'''
        cloneCommand = self.cloneCommand(link, projectdesc)
        usage = self.usage(link)
        credit = self.credits(link)
        contribution = self.contributionInstruct(link)
        markdown_doc = self.convertToMarkdown(basicDoc.get('message', '') + description.get('message', '') + '<h1>Getting Started</h1>' + toc + cloneCommand + usage.get('message', '') + credit.get('message', '') + contribution.get('message', ''))
        return markdown_doc
    @staticmethod
    def convertToMarkdown(self, text):
        return markdownify(text)

    def elaboratedDesc(self,link):
        print("Elaborating description...")
        descprompt = (
            f"""response in html code only Detailed Elaborate the description of the project: {link}"""
        )
        description = self.text_generator.prompt(descprompt)
        print("Elaborated description generated successfully!")
        return description

    def toc(self):
        print("Generating Table of Contents...")
        return f'''<h2>Table of Contents</h2>
                <li>Install and Run the Project</li>
                <li>Use the Project</li>
                <li>Project Structure</li>    
                <li>Credits</li>
                <li>License</li>
                <li>Contribution</li>'''

    def cloneCommand(self,link, projectdesc):
        print("Generating Clone Command...")
        clonePrompt = (
            f"""Analyze the code files and programming languages used in the repository and provide grouped Install dependencies for the project based on the files in the repository: {link} provide one by one in html code. {projectdesc} use this description to generate the clone command."""
        )
        description = self.text_generator.prompt(clonePrompt)
        print("Clone Command generated successfully!")
        return f'''<h3>Installation</h3>
                <ol>
                    <li><strong>Clone the Repository</strong>:
                        <pre><code>git clone {link}.git
                cd CodeDoc-AI</code></pre>
                    </li>
                    <li><strong>Install Dependencies</strong>:
                        {description.get('message', '')}
                    </li>
                </ol>'''

    def usage(self,link):
        print('Generating Usage...')
        usageprompt = f'''Analyze the github repository and provide one by one in html code
                    {link} provide the usage of the project. do not include installation and clone command'''
        usage = self.text_generator.prompt(usageprompt)
        print("Usage generated successfully!")
        return usage

    def credits(self,link):
        print("Generating Credits...")
        creditprompt = f'''Findall the credits for the project: {link} do not generate licenses'''
        creds = self.text_generator.prompt(creditprompt)
        print("Credits generated successfully!")
        return creds

    def contributionInstruct(self,link):
        print("Generating Contribution...")
        prompt = f'''Provide only the contribution instructions for the project: {link} response in html code only.'''
        contribution = self.text_generator.prompt(prompt)
        print("Contribution generated successfully!")
        return contribution

    def finalCodeDoc(self, text):
        print("Converting to Markdown...")
        print("Initialising text model...")
        model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
        tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
        print("Text model initialised successfully!")
        inputs = tokenizer.encode("expand: " + text, return_tensors="pt")
        outputs = model.generate(inputs, max_length=2048, num_beams=4, early_stopping=True)
        elaborated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("Text converted to Markdown successfully!")
        return elaborated_text

# Uncomment to try and test the code
if __name__ == "__main__":
    generator = CodeDocumentationGenerator()
    projectdesc = '''This is a completely python project which generate a detailed documentation for the project. the backend is handeled using django'''
    documentation = generator.generate_full_documentation("https://github.com/parasmunoli/CodeDoc-AI",projectdesc)
    print("HTML Doc: ",documentation)