-- CREATE DATABASE qiang;
-- init user
CREATE USER 'bot'@'172.17.0.1' IDENTIFIED BY 'hello1234';
GRANT ALL PRIVILEGES ON *.* TO 'bot'@'172.17.0.1';
FLUSH PRIVILEGES;


CREATE TABLE `qiang_bot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chain_name` varchar(255) DEFAULT NULL,
  `main_balance` varchar(255) DEFAULT NULL,
  `block_num` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `watch_account` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
