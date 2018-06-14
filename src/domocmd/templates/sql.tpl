DROP TABLE IF EXISTS SERVER_DISKS;
CREATE TABLE hosts (
    server_name VARCHAR(255),
    disk_label VARCHAR(255),
    disk_used VARCHAR(100),
    disk_total_size VARCHAR(100)
);

{% for server in servers %}
{% for disk in server['disks'] %}
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("{{ server['name'] }}","{{ disk['label'] }}", "{{ disk['used_human'] }}","{{ disk['size_human'] }}");
{% endfor %}
{% endfor %}
