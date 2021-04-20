#!/usr/bin/env python3
import sys
import jinja2
import benedict
import base64
import secrets

data = benedict.benedict({})
data["j2render"] = {
    'version': '1.0.0-alpha'
}

if len(sys.argv) < 2  or sys.argv[1] == "--help" or sys.argv[1] == "-h":
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

def rand(n):
    return secrets.token_hex(int(n/2))

env.globals['rand'] = rand

tpl = env.from_string(j2script)
output = tpl.render(data)

print(output)
