import json

from meta_ai_api import MetaAI

# Initialize the MetaAI model
try:
    model = MetaAI()
except Exception as e:
    raise RuntimeError(f"Error loading MetaAI model: {str(e)}")


def extract_features_from_code(code: str) -> dict:
    """
    Extract meaningful features from programming language code using the MetaAI LLM.

    Args:
        code (str): Input programming language code as a string.

    Returns:
        dict: Extracted features in JSON format for code documentation generation.
    """
    try:
        # Define a structured prompt for the model
        prompt = (
            f"Analyze the following code and extract all meaningful features based on the respective programming language's features and naming conventions. "
            f"Provide details and their purposes in a JSON format, adhering to the programming language's structure and terminology.\n\nCode:\n{code}"
        )

        # Query the model with the prompt
        print("Querying MetaAI model...")
        response = model.prompt(prompt)
        print("Model response received.")
        print(response)
        # Parse the response to JSON
        try:
            response_message = response.get('message', '')
            features = json.loads(response_message.split('JSON format:\n', 1)[-1])
        except (json.JSONDecodeError, KeyError, IndexError) as parse_error:
            raise RuntimeError(f"Error parsing response to JSON: {str(parse_error)}")
        
        return features
    except Exception as e:
        raise RuntimeError(f"Error extracting features from code: {str(e)}")


# Example usage
if __name__ == "__main__":
    try:
        # Replace this with the path to your input code file
        with open("sampleCode.py", "r") as file:
            example_code = file.read()

        # Extract features using the MetaAI model
        features = extract_features_from_code(example_code)

        # Save the extracted features to a JSON file
        print("Dumping features...")
        with open("updatedSampleAnalysis.json", "w") as json_file:
            json.dump(features, json_file)
        print("Done.")
        
        print("Feature extraction completed. Results saved to 'updatedSampleAnalysis.json'.")
    except FileNotFoundError as e:
        print(f"File not found: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
