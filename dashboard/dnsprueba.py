import subprocess

def newDns(subdomain):
    nsUpdate =f"""
server master.everyhost.io
zone everyhost.io
update add {subdomain}.everyhost.io 300 A 10.43.120.90
send
    """
    process = subprocess.Popen(['nsupdate'], stdin=subprocess.PIPE)
    process.communicate(nsUpdate.encode())
    print(f"Tu url esta lista en: {subdomain}.everyhost.io")

def deleteDns(subdomain):
    nsUpdate =f"""
server master.everyhost.io
zone everyhost.io
update delete {subdomain}.everyhost.io 300 A 10.43.120.90
send
    """
    process = subprocess.Popen(['nsupdate'], stdin=subprocess.PIPE)
    process.communicate(nsUpdate.encode())
    
    


newDns("mysqladrian")