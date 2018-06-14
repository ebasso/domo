Server Name;Disk Label;Used Human;Total Size Human;Used Perc Human;Used;Free;Total Size
{% for server in servers %}
{% for disk in server['disks'] %}
{{ server['name'] }};{{ disk['label'] }};{{ disk['used_human'] }};{{ disk['size_human'] }};{{ disk['used_perc_human'] }};{{ disk['used'] }};{{ disk['free'] }};{{ disk['size'] }}
{% endfor %}
{% endfor %}
