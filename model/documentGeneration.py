from markdownify import markdownify
from meta_ai_api import MetaAI


# from transformers import MarkupLMFeatureExtractor, MarkupLMTokenizerFast, MarkupLMProcessor


class CodeDocumentationGenerator:
    def __init__(self):
        # self.features = features
        print("Initializing AI text generator...")
        self.text_generator = MetaAI()
        print("AI text generator initialized successfully!")

    def generate_full_documentation(self, link):
        """Generate full documentation using features."""
        print("Generating full documentation...")
        prompt = (
            f"""Return the response in HTML format only. Ensure the response is detailed and comprehensive, covering all the sections listed explicitly
{link}, visit the GitHub repository and create a detailed documentation that includes:
Project Overview: Provide a elaborated brief overview of the project, including its purpose, goals, and objectives.
Technologies Used: Read the code files from the repository only and identify the technologies that are used in the project do not include python if not used in repo link
Requirements: Read the code files and describe the requirements for the project. 
Installation Instructions: Read the and analyze all the code and Provide detailed installation instructions for the project. Include the following steps:
Clone the repository using the command and link is {link}
Navigate to the project directory using the command
Install the required dependencies using the command
Configure the project settings as needed
Usage Instructions provide the details such as Code file from the link repository name to run the project and the command to run it and if docker file available available use docker to spin it up
Provide detailed usage instructions for the project.
Read code and run the project using the command
Acknowledgments
Provide acknowledgments for contributors, including:
List of Contributors
Contributions Made
Conclusion
Conclude the project with a summary, including:
Project Overview
Key Features"""
        )
        response = self.text_generator.prompt(prompt)
        print("Full documentation generated successfully!")
        return response

    def convertToMarkdown(self, text):
        markdownCode = markdownify(text)
        return markdownCode