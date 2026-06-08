# ================================================================
#  Project 3 — The Data Warehouse
#  Python Bonus Script: Connect to AWS RDS via SSH Tunnel
#  DecodeLabs Cloud Computing Internship
#  Author: Muhammad Hassan Raza
# ================================================================

import pymysql
from sshtunnel import SSHTunnelForwarder

# ----------------------------------------------------------------
#  CONFIGURATION
#  ⚠️  If your EC2 was stopped/restarted, update EC2_HOST below
#      with the new Public IP from the AWS console.
# ----------------------------------------------------------------

# EC2 Bastion Host
EC2_HOST     = '100.54.35.199' # Update if EC2 IP changes
EC2_PORT     = 22
EC2_USER     = 'ec2-user'
EC2_KEY_PATH = r'C:\Users\YourUsername\.ssh\your-key.pem'  # Update with your PEM key path

# RDS MySQL Instance
RDS_ENDPOINT = 'decodelabs-data-warehouse.cqlmwgauqebn.us-east-1.rds.amazonaws.com'
RDS_PORT     = 3306
DB_USER      = 'admin'
DB_PASSWORD  = 'xyz12345'  # Use the password you set when creating the RDS instance
DB_NAME      = 'decodelabs_db'

# ----------------------------------------------------------------
#  HELPER: Print results as a formatted table
# ----------------------------------------------------------------

def print_table(rows, headers):
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    separator  = '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'
    header_row = '|' + '|'.join(f' {str(h):<{col_widths[i]}} '
                                 for i, h in enumerate(headers)) + '|'

    print(separator)
    print(header_row)
    print(separator)
    for row in rows:
        data_row = '|' + '|'.join(f' {str(v):<{col_widths[i]}} '
                                   for i, v in enumerate(row)) + '|'
        print(data_row)
    print(separator)
    print(f'\n  {len(rows)} row(s) returned\n')

# ----------------------------------------------------------------
#  MAIN
# ----------------------------------------------------------------

def main():
    print()
    print('=' * 62)
    print('   DecodeLabs Data Warehouse — Python Connection Script')
    print('   Project 3  |  Muhammad Hassan Raza')
    print('=' * 62)
    print()

    # ── Step 1: Open SSH Tunnel ──────────────────────────────────
    print(f'[1/3]  Opening SSH tunnel to EC2 @ {EC2_HOST} ...')

    try:
        with SSHTunnelForwarder(
            (EC2_HOST, EC2_PORT),
            ssh_username=EC2_USER,
            ssh_pkey=EC2_KEY_PATH,
            remote_bind_address=(RDS_ENDPOINT, RDS_PORT)
        ) as tunnel:

            local_port = tunnel.local_bind_port
            print(f'       ✅ SSH tunnel open  →  127.0.0.1:{local_port}')
            print()

            # ── Step 2: Connect to MySQL ─────────────────────────
            print(f'[2/3]  Connecting to MySQL RDS ...')

            connection = pymysql.connect(
                host            = '127.0.0.1',
                port            = local_port,
                user            = DB_USER,
                password        = DB_PASSWORD,
                database        = DB_NAME,
                connect_timeout = 10,
                charset         = 'utf8mb4'
            )

            print(f'       ✅ MySQL connected  →  {DB_NAME}@{RDS_ENDPOINT[:45]}...')
            print()

            # ── Step 3: Run Query ────────────────────────────────
            print('[3/3]  Executing query: SELECT * FROM Interns;\n')

            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Interns;')
                rows    = cursor.fetchall()
                headers = [desc[0] for desc in cursor.description]
                print_table(rows, headers)

            connection.close()

            print('  ✅ Connection closed cleanly.')
            print()
            print('=' * 62)
            print('  🏆 Script completed. Data Warehouse is live on AWS.')
            print('=' * 62)
            print()

    # ── Error Handling ───────────────────────────────────────────
    except FileNotFoundError:
        print(f'\n  ❌ PEM key not found at:\n     {EC2_KEY_PATH}')
        print('     Check the path in the CONFIGURATION section.\n')

    except pymysql.err.OperationalError as e:
        print(f'\n  ❌ MySQL error: {e}')
        print('     → Is the RDS instance in Available state?')
        print('     → Is the security group allowing port 3306?\n')

    except Exception as e:
        print(f'\n  ❌ Unexpected error: {e}')
        print()
        print('  Troubleshooting checklist:')
        print('  1. Is EC2 (Server-Commander-01) Running?')
        print('  2. Has the EC2 IP changed? Update EC2_HOST in config.')
        print('  3. Is RDS status Available? (not Stopped/Modifying)')
        print('  4. Is port 3306 open in the default security group?\n')


if __name__ == '__main__':
    main()
