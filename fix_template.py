
import re
import os

file_path = "templates/porcelanatos.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to find the broken tag: {{ followed by whitespace/newlines followed by p.dimensions followed by whitespace/newlines followed by }}
# We want to replace it with {{ p.dimensions }}
pattern = r"\{\{\s*p\.dimensions\s*\}\}"

# Check if it exists
match = re.search(pattern, content)
if match:
    print("Found broken tag!")
    print(f"Match: {match.group(0)!r}")
    
    # Replace all occurrences with single line
    new_content = re.sub(pattern, "{{ p.dimensions }}", content)
    
    # Also replace any remaining weird ones if my regex was too specific
    # Just generic whitespace flattening inside this specific tag
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("File rewritten.")
else:
    print("Pattern not found using regex.")
    # Fallback: simple string replacement for the exact split I saw
    split_string = """{{
                                            p.dimensions }}"""
    if split_string in content:
        print("Found exact split string!")
        new_content = content.replace(split_string, "{{ p.dimensions }}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("File rewritten (fallback).")
    else:
        # Try stricter indentation from view_file
        split_string_2 = """{{
                                            p.dimensions }}"""
        # This is hard because of indentation. Let's try to normalize spaces.
        print("Could not find exact match. Dumping relevant lines:")
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if "p.dimensions" in line and "{{" in lines[i-1]:
                print(f"Line {i-1}: {lines[i-1]}")
                print(f"Line {i}: {line}")
                # Manual patch
                lines[i-1] = lines[i-1].replace("{{", "{{ p.dimensions }}")
                lines[i] = "" # Delete this line (dangerous but effective if it only had p.dimensions)
                # Actually, better to join them
                # But regex should have caught it.
                
