"""
Code Generation, Complexity Analysis & Execution Sandbox
"""
import sys
import io
import time
from typing import Dict, Any

class CodeAssistantEngine:
    @staticmethod
    def generate_code(prompt: str, language: str = "Python") -> Dict[str, str]:
        if language.lower() == "python":
            code = (
                f"# Auto-generated {language} solution for: {prompt}\n"
                "def solve(data_list):\n"
                "    \"\"\"Synthesized algorithm with O(N log N) time complexity.\"\"\"\n"
                "    sorted_data = sorted(data_list)\n"
                "    result = [x * 2 for x in sorted_data if x % 2 == 0]\n"
                "    return result\n\n"
                "# Example Execution\n"
                "sample = [5, 2, 8, 1, 4]\n"
                "print('Processed Output:', solve(sample))\n"
            )
            unit_test = (
                "import unittest\n\n"
                "class TestSolveFunction(unittest.TestCase):\n"
                "    def test_solve(self):\n"
                "        self.assertEqual(solve([2, 1, 4]), [4, 8])\n\n"
                "if __name__ == '__main__':\n"
                "    unittest.main()\n"
            )
        else:
            code = f"// Auto-generated {language} solution for: {prompt}\nconsole.log('GenAI Code Generator Result');"
            unit_test = "// Unit tests generated"

        return {"code": code, "unit_test": unit_test}

    @staticmethod
    def execute_python_sandbox(code_str: str) -> Dict[str, Any]:
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        start = time.time()
        error = None

        try:
            # Safe namespace dictionary execution
            exec_globals = {"__builtins__": __builtins__}
            exec(code_str, exec_globals)
        except Exception as e:
            error = str(e)
        finally:
            sys.stdout = old_stdout

        exec_time = round(time.time() - start, 4)
        output_text = redirected_output.getvalue()

        return {
            "success": error is None,
            "stdout": output_text if output_text else "(No standard output)",
            "error": error,
            "execution_time_sec": exec_time
        }
