# j2render
Render jinjas templates from stdin.

# Installation Example (Unprivileged User)
```
$ pip3 install -r https://raw.githubusercontent.com/protosam/j2render/main/requirements.txt
$ mkdir ~/bin
$ curl -o ~/bin/j2render https://raw.githubusercontent.com/protosam/j2render/main/j2render.py
$ chmod +x ~/bin/j2render
```

After this make sure that "~/bin" is in your `PATH`. You might need to add something like this in your `.bashrc` or `.bash_profile` and then run `source` against the updated rc or profile.

```
export PATH="${PATH}:${HOME}/bin/"
```

# Usage
This script can be used to take any jinja2 template and render it. This can be useful for debugging or in my own original use case it can be useful for rendering Kubernetes configurations.

A quick and dirty kitchen sink. Some things to note are that booleans have to be `True` or `False`, with capitolization.
All other variables are `strings`. For things like integers you must do type casting in the template. There is an example with `| int`.
```
$ cat <<EOF | j2render a.b.c=xyz foo=bar mybool=False integer_test=3
{{ j2render.version }}
{{ a.b.c }}
{{ foo }}
MyBool is {% if mybool %}true{% else %}false{% endif %}
{% if (integer_test | int) == 3 %}Integers can be compared to integers{% endif %}
{% if integer_test == "3" %}Integers can be compared to strings{% endif %}
{{ "helloworld" | base64_encode }}
{{ "helloworld" | base64_encode | base64_decode }}
{{ rand(32) }}
{{  rand(32) | base64_encode | base64_decode | stored("~/.some_config_path/" + foo + "/test.txt") }}
EOF
```

Get and parse a template from the internet.
```
$ curl -s https://.../path/to/file.j2.yaml | j2render a.b.c=xyz foo=bar
```

Parse a local file.
```
$ cat /path/to/file.j2.yaml | j2render a.b.c=xyz foo=bar
```
