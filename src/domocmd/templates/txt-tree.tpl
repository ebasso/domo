Report: {{title}}

{% for server in servers %}
{{ server['name'] }}
{% for disk in server['disks'] %}
|- {{ disk['label'] }}
|-- Used  : {{ disk['used_human'] }}
|-- Size  : {{ disk['size_human'] }}
|-- Perc  : {{ disk['used_perc'] }}
{% endfor %}

{% endfor %}
