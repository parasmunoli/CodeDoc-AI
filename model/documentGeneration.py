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
        prompt = (
            f"""{link}, visit the GitHub repository and create a detailed documentation that includes:
Project Overview
Provide a brief overview of the project, including its purpose, goals, and objectives.
Technologies Used
Read the code files and identify the technologies used in the project. Provide a detailed list of the programming languages, frameworks, libraries, and tools used.
Requirements
Read the code files and describe the requirements for the project. Provide a detailed list of the hardware and software requirements, including the operating system, processor, memory, and storage requirements.
Installation Instructions
Read the and analyze all the code and Provide detailed installation instructions for the project. Include the following steps:
Clone the repository using the command
Navigate to the project directory using the command
Install the required dependencies using the command
Configure the project settings as needed
Usage Instructions
Provide detailed usage instructions for the project. Include the following steps:
Prepare the input video file
Configure the project settings as needed
Read code and run the project using the command
Monitor the project output and adjust the settings as needed
Documentation
Explain the functionality of the project in an elaborated and detailed manner. Include the following sections:
Project Status
Describe the current status of the project, including:
Development Stage
Testing Stage
Deployment Stage
Contribution Guidelines
Provide guidelines for contributors, including:
Code Style Guidelines
Commit Message Guidelines
Issue Reporting Guidelines
Acknowledgments
Provide acknowledgments for contributors, including:
List of Contributors
Contributions Made
Conclusion
Conclude the project with a summary, including:
Project Overview
Key Features
Future Development Plans
Return the response in HTML format only. Ensure the response is detailed and comprehensive, covering all the sections listed explicitly."""
        )
        response = self.text_generator.prompt(prompt)
        print(response)
        return response

    def convertToMarkdown(self, text):
        markdownCode = markdownify(text)
        return markdownCode