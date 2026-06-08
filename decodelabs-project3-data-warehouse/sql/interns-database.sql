-- ============================================================
-- Project 3: The Data Warehouse
-- DecodeLabs Cloud Computing Internship | Batch 2026
-- Author: Muhammad Hassan Raza
-- Database: Amazon RDS MySQL 8.4.8
-- ============================================================

-- ── Script 01: Create Database ──────────────────────────────
CREATE DATABASE IF NOT EXISTS decodelabs_db;
USE decodelabs_db;

-- ── Script 02: Create Interns Table ─────────────────────────
CREATE TABLE IF NOT EXISTS Interns (
    InternID  INT          PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50)  NOT NULL,
    LastName  VARCHAR(50)  NOT NULL,
    Role      VARCHAR(100) NOT NULL,
    Email     VARCHAR(100) UNIQUE NOT NULL
);

-- ── Script 03: Insert Dummy Records ─────────────────────────
INSERT INTO Interns (FirstName, LastName, Role, Email)
VALUES
    ('Muhammad Hassan', 'Raza',  'Cloud Security Engineer',  'heyyy.hassan0@gmail.com'),
    ('John',            'Doe',   'Cloud Computing Intern',   'jdoe@decodelabs.com'),
    ('Jane',            'Smith', 'DevOps Intern',            'jsmith@decodelabs.com'),
    ('Ahmed',           'Khan',  'AWS Solutions Architect',  'akhan@decodelabs.com'),
    ('Sara',            'Ali',   'Database Administrator',   'sali@decodelabs.com');

-- ── Script 04: Verify Data Persistence ──────────────────────
SELECT * FROM Interns;

-- ── Expected Output ─────────────────────────────────────────
-- +----------+-----------------+----------+------------------------+-------------------------+
-- | InternID | FirstName       | LastName | Role                   | Email                   |
-- +----------+-----------------+----------+------------------------+-------------------------+
-- |        1 | Muhammad Hassan | Raza     | Cloud Security Engineer | heyyy.hassan0@gmail.com|
-- |        2 | John            | Doe      | Cloud Computing Intern  | jdoe@decodelabs.com    |
-- |        3 | Jane            | Smith    | DevOps Intern           | jsmith@decodelabs.com  | 
-- |        4 | Ahmed           | Khan     | AWS Solutions Architect | akhan@decodelabs.com   |
-- |        5 | Sara            | Ali      | Database Administrator  | sali@decodelabs.com    |
-- +----------+-----------------+----------+------------------------+-------------------------+
-- 5 rows in set
