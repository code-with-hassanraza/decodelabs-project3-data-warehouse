# 🗄️ Project 3 — The Data Warehouse
### DecodeLabs Cloud Computing Internship | Batch 2026

![AWS](https://img.shields.io/badge/AWS-RDS-orange?logo=amazon-aws)
![MySQL](https://img.shields.io/badge/MySQL-8.4.8-blue?logo=mysql)
![Python](https://img.shields.io/badge/Python-3.x-green?logo=python)
![SSH](https://img.shields.io/badge/SSH-Tunnel-lightgrey)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

## 📋 Scenario
An e-commerce company is struggling with Excel sheets to manage customer data.
As their user base grows, they need a robust, scalable, and secure cloud database
to store user records reliably. The mission: provision a managed relational database,
engineer a proper schema, populate it with data, and prove persistence.

---

## 🎯 Mission Accomplished
- ✅ Provisioned Amazon RDS MySQL 8.4.8 instance in a private subnet
- ✅ Configured Security Group locked strictly to Port 3306 from EC2 only
- ✅ Engineered Interns table with PRIMARY KEY, UNIQUE, NOT NULL constraints
- ✅ Inserted 5 dummy records using INSERT INTO
- ✅ Verified data persistence with SELECT * via MySQL Workbench over SSH tunnel
- ✅ **BONUS:** Built Python script using PyMySQL + SSHTunnel for programmatic access

---

## 🏗️ Architecture

```
Developer (Local Machine)
     │
     │  MySQL Workbench / Python Script
     │  Standard TCP/IP over SSH
     ▼
┌─────────────────────────────────────────────────┐
│                  AWS VPC (Default)              │
│                                                 │
│  Public Subnet                Private Subnet    │
│  ┌──────────────┐             ┌───────────────┐ │
│  │ EC2 Bastion  │──Port 3306──▶ RDS Instance │ │
│  │ Server-      │  Forwarding │  MySQL 8.4.8  │ │
│  │ Commander-01 │             │  db.t4g.micro │ │
│  └──────┬───────┘             │  Private only │ │
│         │ SSH Port 22         └───────────────┘ │
└─────────┼───────────────────────────────────────┘
          │
     Developer
```

**Security:** Publicly accessible = NO | Port 3306 locked to EC2 Security Group only

---

## 📁 Repository Structure

```
decodelabs-project3-data-warehouse/
├── README.md
├── sql/
│   ├── 01-create-database.sql
│   ├── 02-create-table.sql
│   ├── 03-insert-records.sql
│   └── 04-select-query.sql
├── python/
│   └── rds_connect.py
├── config/
│   ├── rds-configuration.md
│   └── security-group-rules.md
└── screenshots/
    ├── 01-rds-instance-available.png
    ├── 02-security-group-port-3306.png
    ├── 03-mysql-workbench-connection-setup.png
    ├── 04-mysql-workbench-select-results.png
    └── 05-python-script-terminal-output.png
```

---

## 🗃️ Database Schema

```sql
CREATE DATABASE decodelabs_db;
USE decodelabs_db;

CREATE TABLE Interns (
    InternID  INT          PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50)  NOT NULL,
    LastName  VARCHAR(50)  NOT NULL,
    Role      VARCHAR(100) NOT NULL,
    Email     VARCHAR(100) UNIQUE NOT NULL
);
```

### Constraint Explanation
| Constraint | Column | Purpose |
|---|---|---|
| PRIMARY KEY | InternID | Uniquely identifies each row, enables auto-indexing |
| AUTO_INCREMENT | InternID | Automatically assigns the next ID |
| NOT NULL | FirstName, LastName, Role | Prevents empty/meaningless entries |
| UNIQUE | Email | Ensures no two interns share the same email |

---

## 📊 Sample Data (SELECT * Result)

| InternID | FirstName | LastName | Role | Email |
|---|---|---|---|---|
| 1 | Muhammad Hassan | Raza | Cloud Security Engineer | heyyy.hassan0@gmail.com |
| 2 | John | Doe | Cloud Computing Intern | jdoe@decodelabs.com |
| 3 | Jane | Smith | DevOps Intern | jsmith@decodelabs.com |
| 4 | Ahmed | Khan | AWS Solutions Architect | akhan@decodelabs.com |
| 5 | Sara | Ali | Database Administrator | sali@decodelabs.com |

---

## ⚙️ RDS Configuration

| Setting | Value |
|---|---|
| DB Identifier | decodelabs-data-warehouse |
| Engine | MySQL 8.4.8 |
| Instance Class | db.t4g.micro (Free Tier) |
| Storage | 20 GB gp2 |
| Region / AZ | us-east-1c |
| Publicly Accessible | NO |
| VPC | Default VPC |
| Port | 3306 |

---

## 🔒 Security Group Rules

| Security Group | Rule | Port | Source |
|---|---|---|---|
| default (RDS) | MySQL/Aurora Inbound | 3306 | EC2 Security Group ID |
| launch-wizard-1 (EC2) | SSH Inbound | 22 | Admin IP |

---

## 🐍 Python Bonus Script
The `python/rds_connect.py` script demonstrates programmatic access to the private
RDS instance through an SSH tunnel using PyMySQL and SSHTunnel libraries.

**Install dependencies:**
```bash
pip install pymysql sshtunnel
pip install paramiko==2.12.0
```

**Run:**
```bash
python rds_connect.py
```

---

## 📸 Screenshots
> See the `/screenshots` folder for step-by-step visual proof of the entire setup.

---

## 🛠️ Technologies Used
- **Amazon RDS** — Managed relational database service
- **MySQL 8.4.8** — Database engine
- **Amazon EC2** — SSH Bastion Host
- **MySQL Workbench** — GUI database client
- **Python / PyMySQL** — Programmatic database access
- **SSHTunnel / Paramiko** — SSH tunneling library
- **AWS VPC / Security Groups** — Network isolation and access control

---

## 👤 Author
**Muhammad Hassan Raza**
Cloud Computing Intern @ DecodeLabs | Batch 2026
