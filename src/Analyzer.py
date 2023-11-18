import re
import ast
import astor

def extract_functions(diff: str, source: str, language: str):
    """
    Extracts functions from the given source code based on the provided diff and language.

    Args:
        diff (str): The diff containing the changes made to the source code.
        source (str): The source code from which to extract the functions.
        language (str): The programming language of the source code. Must be either 'java' or 'python'.

    Returns:
        list: A list of extracted functions from the source code.

    Raises:
        ValueError: If the provided language is not 'java' or 'python'.
    """
    if language not in ["java", "python"]:
        raise ValueError("Language must be either 'java' or 'python'.")
    if language == "java":
        function_names = extract_java_function_names(diff)
        return extract_java_functions_from_source(source, function_names)
    if language == "python":
        function_names = extract_python_function_names(diff)
        return extract_python_functions_from_source(source, function_names)
    
def extract_java_function_names(diff: str):
    lines = diff.splitlines()
    lines = [line for line in lines if not line.strip().startswith("-")]
    diff = '\n'.join(lines)
    # Regular expression pattern to match Java function declarations
    pattern = r"[public|protected|private]?\s*[static|final]?\s*\w+\s+([a-zA-Z_][\w]*)\s*\([^)]*\)\s*\s*{?"

    # Find all matches in the diff message
    matches = re.findall(pattern, diff)

    # Extract function names from matches
    function_names = []
    for match in matches:
        # Extract the function name using a simple regex
        function_name = re.search(r'\w+\s*$', match)
        if function_name:
            function_names.append(function_name.group())

    return function_names

def extract_java_functions_from_source(source_code: str, function_names: list):
    # Initialize an empty dictionary to store the results
    function_definitions = {}

    # Iterate through the list of function names
    for function_name in function_names:
        # Use a regular expression to search for the function definition
        pattern = r"(?s)(?:public|private|protected|static)?\s+[a-zA-Z_$][a-zA-Z\d_$]*\s+" + function_name + r"\s*\([^)]*\)\s*{[^}]*}"
        matches = re.findall(pattern, source_code)
        if matches:
            # If a match is found, add it to the dictionary
            function_definitions[function_name] = matches[0]

    return function_definitions

def extract_python_function_names(diff: str):
    # It simply extract function names from what's following "@@" in diff
    lines = diff.splitlines()
    # 1. Remove the lines starting with "-"
    lines = [line for line in lines if not line.startswith("-")]
    # 2. Search for the function definition
    function_pattern = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\("
    function_names = re.findall(function_pattern, diff)
    return function_names

def extract_python_functions_from_source(source_code: str, function_names: list):
    """
    Retrieves the matching functions from the given code based on the provided function names.

    Args:
        source_code (str): The code to analyze.
        function_names (list): A list of function names to search for.

    Returns:
        dict: A dictionary containing the matching functions as values, with the function names as keys.
            Note that it may be the case that not all function names are present in the returned dictionary.
    """
    
    # Initialize an empty dict to store the matching functions
    matching_functions = {}

    # Parse the file's content into an abstract syntax tree (AST)
    tree = ast.parse(source_code)

    # Traverse the AST to find function definitions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check if the function name matches any name in the list
            if node.name in function_names:
                matching_functions[node.name] = astor.to_source(node)

    return matching_functions    

def separate_diff_by_files(diff_message):
    file_diffs = {}
    current_file = None

    # Split the diff message into lines
    lines = diff_message.split('\n')

    for line in lines:
        # Check if the line starts with "+++ b/"
        if line.startswith('+++ b/'):
            # Extract the file name from the line
            file_name = line[6:]
            current_file = file_name
            file_diffs[current_file] = []
        elif current_file is not None:
            # Append the line to the current file's diff
            file_diffs[current_file].append(line)

    # Join the lines to reconstruct the diff messages
    for file_name, diff_lines in file_diffs.items():
        file_diffs[file_name] = '\n'.join(diff_lines)

    return file_diffs

def extract_involved_functions(diff, sources):
    """
    Extracts the involved functions in the given diff from the sources.

    Args:
        diff (str): The diff containing the changes made.
        sources (dict): A dictionary mapping file names to their corresponding source code.

    Returns:
        list: A list of involved functions extracted from the diff and sources.
    """
    functions = []
    diffs = separate_diff_by_files(diff)
    common_keys = diffs.keys() & sources.keys()
    diffs = {key: diffs[key] for key in common_keys}
    for file_name, diff in diffs.items():
        if file_name.endswith(".java"):
            functions += extract_functions(diff, sources[file_name], "java")
        elif file_name.endswith(".py"):
            functions += extract_functions(diff, sources[file_name], "python")
    return functions
