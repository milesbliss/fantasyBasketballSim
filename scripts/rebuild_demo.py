import subprocess
subprocess.run(["python", "scripts/reset_db.py"], check=True)
subprocess.run(["python", "scripts/seed_demo.py"], check=True)
print("Rebuilt DB with demo data.")
