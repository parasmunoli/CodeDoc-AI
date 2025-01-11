import json

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class CPPFeatureExtractor:
    def __init__(self, model_name="t5-small"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.program_name = "Program Analysis"
        self.features = {
            "Variables": {
                "Declaration": [],
                "Initialization": [],
                "Global Variables": [],
                "Local Variables": [],
                "Constants": []
            },
            "Data Types": {
                "Basic": {"int": 0, "float": 0, "double": 0, "char": 0},
                "Derived": {"Arrays": 0, "Pointers": 0, "Functions": 0},
                "Enumeration": [],
                "User-defined": {"Struct": [], "Union": []}
            },
            "Operators": {
                "Arithmetic": [],
                "Assignment": [],
                "Relational": [],
                "Logical": [],
                "Bitwise": [],
                "Increment/Decrement": [],
                "Conditional (Ternary)": [],
                "Special": []
            },
            "Control Flow": {
                "if statement": 0,
                "else statement": 0,
                "switch-case": 0,
                "for loop": 0,
                "while loop": 0,
                "do-while loop": 0
            },
            "Functions": {
                "Function Declaration": [],
                "Function Definition": [],
                "Call by Value": [],
                "Call by Reference": [],
                "Inline Functions": []
            },
            "Pointers": {
                "Declaration and Initialization": [],
                "Pointer Arithmetic": [],
                "Pointers to Arrays": [],
                "Pointers to Functions": [],
                "Dynamic Memory Allocation": []
            },
            "Arrays": {
                "Single Dimensional Arrays": [],
                "Multidimensional Arrays": [],
                "Arrays of Pointers": []
            },
            "Strings": {
                "String Handling Functions": [],
                "Character Arrays": []
            },
            "Object-Oriented Programming (C++)": {
                "Classes and Objects": [],
                "Constructors and Destructors": [],
                "Inheritance": [],
                "Polymorphism": {
                    "Compile-time": [],
                    "Runtime": []
                },
                "Encapsulation": [],
                "Abstraction": []
            },
            "File Handling": {
                "File Opening Modes": [],
                "Reading/Writing to Files": [],
                "Closing Files": []
            },
            "Standard Template Library (STL - C++)": {
                "Containers": {
                    "Vectors": [],
                    "Lists": [],
                    "Sets": [],
                    "Maps": [],
                    "Queues": []
                },
                "Iterators": [],
                "Algorithms": []
            },
            "Preprocessor Directives": {
                "#define": [],
                "#include": [],
                "#ifdef/#ifndef": [],
                "#undef": [],
                "#pragma": [],
                "Macros": []
            },
            "Debugging": {
                "printf and cerr": [],
                "GDB (GNU Debugger)": [],
                "Valgrind (Memory Debugging)": []
            },
            "Others": {
                "Recursion": [],
                "Multithreading": [],
                "Dynamic Memory Allocation": [],
                "const Keyword": [],
                "Volatile Keyword": []
            }
        }

    def extract_features(self, code):
        prompt = f"Extract C++ features from the following code:\n\n{code}"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = self.model.generate(**inputs, max_length=512)
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Parsing the result (assumes output is in JSON format)
        try:
            extracted_features = json.loads(result)
            self.features.update(extracted_features)
        except json.JSONDecodeError:
            print("Failed to parse the model output. Returning features as-is.")
        return self.features
