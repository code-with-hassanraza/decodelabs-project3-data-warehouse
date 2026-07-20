# 🔐 Security Incident Report
## Exposed Database Credentials in Public GitHub Repository

**Project:** The Data Warehouse — DecodeLabs Cloud Computing Internship
**Incident ID:** SEC-2026-001
**Date Detected:** June 9, 2026
**Date Resolved:** June 9, 2026 (Same Day)
**Severity:** High
**Status:** ✅ Resolved

---

## 📋 Incident Summary

During the development of Project 3 (AWS RDS MySQL + Python),
a Python script containing hardcoded database credentials was
accidentally pushed to a public GitHub repository.

The exposure was detected by GitGuardian — an automated secret
scanning service that monitors public repositories in real-time.

The incident was identified, escalated, and fully resolved
within the same day it was detected.

---

## 🔍 What Was Exposed

| Credential Type | Variable | Exposure Status |
|---|---|---|
| RDS Endpoint URL | `RDS_ENDPOINT` | ⚠️ Exposed |
| Database Username | `DB_USER` | ⚠️ Exposed |
| Database Password | `DB_PASSWORD` | ⚠️ Exposed |
| EC2 Public IP | `EC2_HOST` | ⚠️ Exposed |

### Exposed Code (Before Fix):
```python
# ❌ BAD PRACTICE — Never do this
EC2_HOST     = '100.54.35.199'
RDS_ENDPOINT = 'database-name.xxxxxx.us-east-1.rds.amazonaws.com'
DB_USER      = 'admin'
DB_PASSWORD  = 'MyPassword@2026'
```

---

## ⏱️ Incident Timeline

| Time | Event |
|---|---|
| June 9, 2026 — 13:28 UTC | Python script pushed to public GitHub repo |
| June 9, 2026 — 18:18 UTC | GitGuardian automated alert received via email |
| June 9, 2026 — 18:35 UTC | Incident acknowledged and investigation started |
| June 9, 2026 — 18:57 UTC | RDS master password rotated via AWS Console |
| June 9, 2026 — 19:09 UTC | Python script cleaned (credentials replaced with placeholders) |
| June 9, 2026 — 19:23 UTC | Fixed code pushed to GitHub |
| June 9, 2026 — 19:45 UTC | GitGuardian alert marked as resolved |

**Total Time to Resolution: ~2.5 hours**

---

## 🛡️ Why The Database Was Still Safe

Despite the credentials being exposed publicly, the actual
database was NOT compromised. Here is why:

```
Internet User (attacker)
        │
        │ tries to connect to RDS endpoint
        ▼
   AWS VPC Firewall
        │
        │ BLOCKED — RDS has no public IP
        │ Publicly Accessible = NO
        ▼
   Connection Refused ✅

ONLY this path works:
Developer → SSH (port 22) → EC2 Bastion → Port 3306 → Private RDS
```

**Security controls that prevented exploitation:**
- RDS instance had `Publicly Accessible = NO`
- Port 3306 was locked to EC2 Security Group only (not internet)
- Database was in a private subnet with no internet gateway route
- Attacker would need both: valid SSH key + EC2 access + correct IP

---

## 🔧 Remediation Steps Taken

### Step 1 — Password Rotation (Immediate Priority)
```
AWS Console → RDS → decodelabs-data-warehouse
→ Modify → New master password set
→ Apply immediately
```

### Step 2 — Code Sanitization
Replaced all hardcoded values with safe placeholders:

```python
# ✅ GOOD PRACTICE — Use placeholders or environment variables
EC2_HOST     = 'YOUR-EC2-PUBLIC-IP'
EC2_USER     = 'ec2-user'
EC2_KEY_PATH = r'path/to/your/key.pem'
RDS_ENDPOINT = 'YOUR-RDS-ENDPOINT.rds.amazonaws.com'
DB_USER      = 'YOUR-DB-USERNAME'
DB_PASSWORD  = 'YOUR-DB-PASSWORD'
DB_NAME      = 'your_database_name'
```

### Step 3 — Repository Update
```bash
git add rds_connect.py
git commit -m "Security: remove hardcoded credentials, replace with placeholders"
git push
```

---

## ✅ Best Practices to Prevent This

### Option 1 — Environment Variables (Recommended)
```python
import os

DB_PASSWORD  = os.environ.get('DB_PASSWORD')
DB_USER      = os.environ.get('DB_USER')
RDS_ENDPOINT = os.environ.get('RDS_ENDPOINT')
EC2_HOST     = os.environ.get('EC2_HOST')
```

Set environment variables before running:
```powershell
# Windows PowerShell
$env:DB_PASSWORD = "your-actual-password"
$env:DB_USER = "admin"
python rds_connect.py
```

### Option 2 — .env File + python-dotenv
```bash
pip install python-dotenv
```

Create a `.env` file (NEVER push to GitHub):
```
DB_PASSWORD=your-actual-password
DB_USER=admin
RDS_ENDPOINT=your-endpoint.rds.amazonaws.com
EC2_HOST=your-ec2-ip
```

Load in Python:
```python
from dotenv import load_dotenv
import os

load_dotenv()
DB_PASSWORD = os.getenv('DB_PASSWORD')
```

### Option 3 — AWS Secrets Manager (Production Grade)
```python
import boto3
import json

def get_secret():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId='rds/decodelabs/credentials')
    return json.loads(response['SecretString'])

secrets = get_secret()
DB_PASSWORD = secrets['password']
DB_USER     = secrets['username']
```

### Option 4 — .gitignore (Always Do This)
Create a `.gitignore` file in your repo root:
```
# Environment variables
.env
*.env
config.py
secrets.py

# Keys and certificates
*.pem
*.key
*.cert

# Local config
local_config.py
database_config.py
```

---

## 🔑 Golden Rules — Never Forget

```
❌ NEVER hardcode passwords in source code
❌ NEVER commit .env files to GitHub
❌ NEVER store PEM keys in repositories
❌ NEVER trust that private = safe when credentials are exposed

✅ ALWAYS use environment variables or secrets managers
✅ ALWAYS add .gitignore before first commit
✅ ALWAYS rotate credentials immediately after exposure
✅ ALWAYS use private subnets for databases
✅ ALWAYS enable secret scanning on repositories
```

---

## 📚 Tools That Detect Secret Exposure

| Tool | Purpose | Link |
|---|---|---|
| **GitGuardian** | Monitors GitHub for exposed secrets | gitguardian.com |
| **GitHub Secret Scanning** | Built-in GitHub secret detection | github.com/security |
| **truffleHog** | Scans git history for secrets | github.com/trufflesecurity |
| **detect-secrets** | Pre-commit hook for secret detection | github.com/Yelp/detect-secrets |

---

## 🎓 Key Learnings

1. **Secret scanning tools are real and fast** — GitGuardian detected
   the exposure within hours of the push, not days.

2. **Defense in depth saved the day** — Even though credentials were
   exposed publicly, the private subnet architecture meant the database
   was never actually reachable by an attacker.

3. **Incident response speed matters** — Resolving within 2.5 hours
   is good practice. The faster you rotate credentials after exposure,
   the smaller your attack window.

4. **Architecture decisions are security decisions** — Setting
   `Publicly Accessible = NO` on the RDS instance was the single
   most important security decision in this project.

5. **Git history is permanent** — Even after removing credentials
   from code and pushing a fix, the old commit still exists in git
   history. For production systems, you would need to rewrite git
   history using tools like `git-filter-repo`.

---

## 👤 Author

**Muhammad Hassan Raza**
Cloud Computing Intern — DecodeLabs | Batch 2026
GitHub: https://github.com/code-with-hassanraza
Incident Date: June 9, 2026