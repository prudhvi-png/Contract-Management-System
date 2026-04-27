CREATE DATABASE IF NOT EXISTS contract_management;
USE contract_management;

CREATE TABLE IF NOT EXISTS workers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  worker_code VARCHAR(30) NOT NULL UNIQUE,
  name VARCHAR(150) NOT NULL,
  photo_path VARCHAR(255) NOT NULL,
  qr_path VARCHAR(255) NOT NULL,
  contract_start DATE NOT NULL,
  contract_end DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  worker_id INT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  type ENUM('IN', 'OUT') NOT NULL,
  CONSTRAINT fk_attendance_worker FOREIGN KEY (worker_id) REFERENCES workers(id)
    ON DELETE CASCADE
);
