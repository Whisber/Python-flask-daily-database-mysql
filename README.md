# Python-flask-daily-database-mysql
Sending datas from realtime database table to daily database table with using python flask.

First table (name)(jsontable)
+-------+-----------------+------+-----+---------+----------------+
| Field | Type            | Null | Key | Default | Extra          |
+-------+-----------------+------+-----+---------+----------------+
| id    | bigint unsigned | NO   | PRI | NULL    | auto_increment |
| code  | varchar(191)    | NO   |     | NULL    |                |
| ip    | varchar(150)    | NO   |     | NULL    |                |
| date  | date            | YES  |     | NULL    |                |
| data  | json            | YES  |     | NULL    |                |
+-------+-----------------+------+-----+---------+----------------+

Second table (name)(jsontabledaily) 
+-------+-----------------+------+-----+---------+----------------+
| Field | Type            | Null | Key | Default | Extra          |
+-------+-----------------+------+-----+---------+----------------+
| id    | bigint unsigned | NO   | PRI | NULL    | auto_increment |
| code  | varchar(191)    | NO   |     | NULL    |                |
| ip    | varchar(150)    | NO   |     | NULL    |                |
| date  | date            | YES  |     | NULL    |                |
| data  | json            | YES  |     | NULL    |                |
+-------+-----------------+------+-----+---------+----------------+
Used different two table but with the same fields. One of them is realtime db , second one is daily table. Second table everyday changes. It depends on daily datas to send. It coded for API datas.
