#!/usr/bin/env python3
import os
import sys
import pathlib
import jinja2
import benedict
import base64
import secrets

data = benedict.benedict({})
data["j2render"] = {
    'version': '1.0.0-alpha'
}


if len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("Usage: " + sys.argv[0] + " [variable=value] [variable=value] [variable=value] ...")
    print()
    print("  Example:")
    print("    " + sys.argv[0] + " abc.xyz=1234")
    print()
    exit(1)

# Consume our script name.
script_name = sys.argv[0]
del sys.argv[0]

# Slurp up the supplied variables.
for i in sys.argv:
    override = i.split("=", 2)

    if len(override) != 2:
        print("ERROR: " + sys.argv[0] + ": Value overrides are expected as name=value or name.subname=value.")
        exit(1)

    data[override[0]]=override[1]

# slurp up STDIN.
j2script = "".join(sys.stdin.readlines())

env = jinja2.Environment(loader=jinja2.BaseLoader)

# Add filters to jinja.
def base64_decode(i): 
    i = i.encode('utf-8')
    return base64.b64decode(i).decode("utf-8")

env.filters['base64_decode'] = base64_decode

def base64_encode(i): 
    i = i.encode('utf-8')
    return base64.b64encode(i).decode("utf-8")

env.filters['base64_encode'] = base64_encode

def stored(filtered, file_path):
    file_path = os.path.expanduser(file_path)
    file = pathlib.Path(file_path)

    if file.is_dir():
        print("ERROR: " + sys.argv[0] + ": " + file_path + " is a directory.")
        exit(1)
    
    if file.is_file():
        out = ""
        with open(file_path, 'r') as f:
            out += f.read()
        return out
    
    # create directory
    file.parent.mkdir(parents=True, exist_ok=True)

    # open and write file with filtered
    f = open(file_path, 'w')
    f.write(filtered)
    f.close()

    # Return the filtered thing to the template.
    return filtered

env.filters['stored'] = stored

def rand(n):
    return secrets.token_hex(int(n))

env.globals['rand'] = rand

tpl = env.from_string(j2script)
output = tpl.render(data)

print(output)
