Since the hackathon starts in **3 days**, do not try to learn everything. Your goal should be to become effective at solving **easy and medium CTF challenges quickly**.

Based on your background (Python, Linux, Flask, SQL, networking), focus on:

1. **Web Security (highest priority)**
2. **Linux Security**
3. **Network Security**
4. **Digital Forensics basics**
5. Windows Security + Incident Response only if time remains

## Day 1 — Web Security + CTF Tools

### Morning (4-5 hours): Web Security Crash Course

Learn and practice:

### SQL Injection

Understand:

```sql
' OR 1=1 --
```

Practice:

* Login bypass
* Extracting database information

Tools:

```bash
sqlmap
```

Example:

```bash
sqlmap -u "http://target.com/page?id=1" --dbs
```

---

### XSS

Learn:

```html
<script>alert(1)</script>
```

Types:

* Reflected XSS
* Stored XSS

---

### File Upload Attacks

Look for:

* Uploading wrong file types
* Bypassing extensions

Examples:

```
shell.php
shell.php.jpg
shell.phtml
```

---

### IDOR

Example:

Normal:

```
/profile?id=100
```

Try:

```
/profile?id=101
```

---

### Authentication Problems

Check:

* Weak passwords
* Default accounts
* Password reset flaws

---

### Afternoon (3-4 hours): Practice

Do:

PortSwigger Web Security Academy platform:

* SQL Injection
* XSS
* Authentication
* Access Control

Install:

```bash
sudo apt install burpsuite
sudo apt install nmap gobuster ffuf
```

Learn Burp basics:

* Proxy
* Repeater
* Intruder

---

## Day 2 — Linux + Network Security

### Linux Privilege Escalation

Learn:

Check system:

```bash
whoami
id
uname -a
```

Find interesting files:

```bash
find / -perm -4000 2>/dev/null
```

Check processes:

```bash
ps aux
```

Install:

```bash
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh

chmod +x linpeas.sh
./linpeas.sh
```

Understand:

* SUID
* sudo permissions
* cron jobs
* weak permissions

---

## Network Security

Master these commands:

### Nmap

```bash
nmap -sV -sC target-ip
```

Find ports:

```bash
nmap -p- target-ip
```

Common ports:

```
21 FTP
22 SSH
80 HTTP
443 HTTPS
3306 MySQL
3389 RDP
```

---

### Web Enumeration

Use:

```bash
gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt
```

Look for:

```
/admin
/login
/uploads
/backup
/config
```

---

### Wireshark Basics

Learn filters:

HTTP:

```
http
```

DNS:

```
dns
```

Passwords:

```
tcp contains "password"
```

---

## Day 3 — Full CTF Simulation

Do not study. Practice.

Go to:

* picoCTF
* TryHackMe
* CTFtime

Solve:

### 5 Web challenges

### 5 Linux challenges

### 3 Network challenges

### 2 Forensics challenges

---

# Prepare Your CTF Toolkit

Install:

```bash
sudo apt update

sudo apt install \
nmap \
gobuster \
ffuf \
sqlmap \
hydra \
wireshark \
john \
hashcat \
netcat \
curl \
wget
```

Python tools:

```bash
pip install requests beautifulsoup4 pwntools
```

---

# During the Competition Strategy

Do not spend 2 hours on one challenge.

Use this rule:

* Easy → 15-20 minutes
* Medium → 45 minutes
* Hard → skip and return later

Always check:

### For web:

```
robots.txt
/.git
/admin
/source
backup files
cookies
headers
```

### For files:

```bash
file filename
strings filename
exiftool filename
binwalk filename
```

### For hashes:

```bash
hashcat
john
```

---

# Your biggest advantage

Because you know **Flask + SQL + Linux**, you already understand how many vulnerable systems are built. Spend the next 3 days becoming good at **enumeration and using tools**, not learning advanced exploits.

A realistic target for 3 days:

* Web Security: strong
* Linux: medium
* Network: medium
* Forensics: basic

That is enough to score well in a beginner/intermediate national CTF.   

tshark -r challenge.pcapng -Y "arp" -T fields -e frame.number -e arp.src.hw_mac -e arp.src.proto_ip -e arp.opcode

