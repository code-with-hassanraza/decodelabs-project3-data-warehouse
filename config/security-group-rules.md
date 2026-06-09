# Security Groups — Project 3 RDS Setup

| Security Group     | Rule           | Port | Source              |
|--------------------|----------------|------|---------------------|
| default (RDS)      | MySQL Inbound  | 3306 | EC2 SG ID           |
| launch-wizard-1    | SSH Inbound    | 22   | Admin IP            |
