"""
Test the improved solution with the provided test cases
"""

def test_solution():
    from io import StringIO
    import sys
    
    # Import the solve function
    sys.path.append('.')
    
    test_input = """6
2 3
hey
hey
3 3
abc
def
ghi
3 2
af
fa
te
1 1
x
3 3
uoe
vbe
mbu
2 3
hyh
kop"""
    
    expected_output = ["4", "16", "2", "0", "11", "3"]
    
    # Redirect stdin
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    
    sys.stdin = StringIO(test_input)
    output_capture = StringIO()
    sys.stdout = output_capture
    
    try:
        # Execute the solve function
        exec(open('G.py').read())
        
        output = output_capture.getvalue().strip().split('\n')
        
        print("Expected:", expected_output)
        print("Got:     ", output)
        
        for i, (expected, got) in enumerate(zip(expected_output, output)):
            if expected == got:
                print(f"Test {i+1}: ✓ PASS")
            else:
                print(f"Test {i+1}: ✗ FAIL (expected {expected}, got {got})")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

if __name__ == "__main__":
    test_solution()