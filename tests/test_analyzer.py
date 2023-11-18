import pytest
from src.analyzer import extract_java_function_names, extract_python_function_names, get_python_functions_from_code, extract_java_functions_from_code, extract_functions


def test_extract_java_function_names():
    diff_message = """
    @@ -20,7 +20,7 @@ public class MyClass {
        }

        // This is a public method
    -    public void myPublicMethod() {
    +    public void myUpdatedPublicMethod() {
            // Code here
        }

    -    private int myPrivateMethod() {
    +    private int myUpdatedPrivateMethod() {
            // Code here
        }
    }
    """
    function_names = extract_java_function_names(diff_message)
    assert ['myUpdatedPublicMethod', 'myUpdatedPrivateMethod'] == function_names


def test_extract_python_function_names():
    diff = """
    --- a/src/jack.py
    +++ b/src/jack.py
    @@ -31,8 +31,6 @@ def jack_work():
         print('.........................')
         print('..........................')
         print('****************************')
    -    print('****************************')
    -    print('****************************')
         print('...........................')
         print('............................')
         print('.............................')
        
         def jack_not_work():
            not_work = "not work"
        """
    function_names = extract_python_function_names(diff)
    assert ['jack_work', 'jack_not_work'] == function_names

def test_get_python_functions_from_code():
    file = """
def jack_work():
    print('.........................')
def jack_not_work():
    not_work = "not work"
    """
    function_names = ['jack_work', 'jack_not_work']
    matching_functions = get_python_functions_from_code(file, function_names)
    print(matching_functions)
    assert matching_functions["jack_work"] ==  "def jack_work():\n    print('.........................')\n"
    assert matching_functions["jack_not_work"] == "def jack_not_work():\n    not_work = 'not work'\n"

def test_extract_java_functions_from_code():
    source_code = """
    public class MyClass {
        public void myFunction1() {
            // Function 1 code here
        }

        private int myFunction2(String param) {
            // Function 2 code here
            return 42;
        }

        public static void myFunction3() {
            // Function 3 code here
        }
    }
    """
    function_names = ["myFunction1", "myFunction2", "myFunction3"]
    definitions = extract_java_functions_from_code(source_code, function_names)
    assert definitions["myFunction1"] == 'public void myFunction1() {\n            // Function 1 code here\n        }'
    assert definitions["myFunction2"] == 'private int myFunction2(String param) {\n            // Function 2 code here\n            return 42;\n        }'
    assert definitions["myFunction3"] == 'static void myFunction3() {\n            // Function 3 code here\n        }'

def test_extract_functions():
    diff_message = """
    +    public void myFunction1() {
    """
    source = source_code = """
    public class MyClass {
        public void myFunction1() {
            // Function 1 code here
        }
    """
    functions = extract_functions(diff_message, source, "java")
    assert functions["myFunction1"] == "public void myFunction1() {\n            // Function 1 code here\n        }"
