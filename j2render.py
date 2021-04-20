#!/usr/bin/env python3
import sys
import jinja2
import benedict

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

tpl = jinja2.Environment(loader=jinja2.BaseLoader).from_string(j2script)
output = tpl.render(data)

print(output)
