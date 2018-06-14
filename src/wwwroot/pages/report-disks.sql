DROP TABLE IF EXISTS SERVER_DISKS;
CREATE TABLE hosts (
    server_name VARCHAR(255),
    disk_label VARCHAR(255),
    disk_used VARCHAR(100),
    disk_total_size VARCHAR(100)
);

INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver1","/domino/notesdata", "60.99GB","159.92GB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver1","/domino/notesdata/daos", "270.08GB","549.73GB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver1","/domino/notesdata/fulltext", "194.26GB","229.90GB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver1","/domino/notesdata/logdir", "3.72GB","149.92GB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver1","/domino/notesdata/mail", "429.19GB","1.46TB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver1","/opt", "5.28GB","49.99GB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver1","/var/log", "1.83GB","9.87GB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver2","/domino/notesdata", "68.65GB","159.92GB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver2","/domino/notesdata/daos", "452.88GB","1023.50GB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver2","/domino/notesdata/fulltext", "346.42GB","849.63GB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver2","/domino/notesdata/logdir", "928.30MB","149.92GB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver2","/domino/notesdata/mail", "705.45GB","1.95TB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver2","/opt", "5.28GB","49.99GB");
INSERT INTO hosts (server_name,disk_label,disk_used,disk_total_size) VALUES ("mailserver2","/var/log", "2.52GB","24.87GB");
