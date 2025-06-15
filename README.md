
# 🛰️ Master Location Seeker

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-yellow?style=for-the-badge&logo=flask)]
[![Ngrok](https://img.shields.io/badge/Ngrok-Enabled-blueviolet?style=for-the-badge&logo=ngrok)]
[![License](https://img.shields.io/github/license/Unsagtools/Master-Location-Seeker?style=for-the-badge)](LICENSE)

> Developed by **Phoenix Editz**  
> Repo: https://github.com/Unsagtools/Master-Location-Seeker

Master Location Seeker is a powerful web-based tool built with Flask that helps you collect real-time information like IP address, live geolocation, and silent camera snapshots of any visitor via a clean, mobile-friendly UI. The data is captured securely through Ngrok tunneling.

---

## ⚙️ Features

- 🌐 Public ngrok URL to host the page
- 📍 Live geolocation tracking
- 📸 Silent webcam access (requires browser permissions)
- 📁 Auto-saves photos with IP & timestamp
- 🔐 Random password displayed after verification
- 🎨 Clean UI with bubble animation

---

## 🧰 Requirements

- Python 3.7+
- Linux/Termux or any OS with Python
- Ngrok account (free)

---

## 📦 Python Dependencies

Install required Python packages using:

```bash
pip install flask pyngrok


---

🛠️ Ngrok Installation & Setup

Run these commands one-time to install Ngrok and authenticate it:

# Install ngrok
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok

# Add your ngrok authtoken (get it from https://dashboard.ngrok.com)
ngrok config add-authtoken <your_auth_token_here>

⚠️ Note: You do NOT need to edit the Python file to add the token.


---

🚀 How to Run

git clone https://github.com/Unsagtools/Master-Location-Seeker.git
cd Master-Location-Seeker
python Master-Location-Seeker.py

Wait a few seconds, and you’ll see:

🔗 Public URL: https://xyz123.ngrok.io

Copy that link and send it to your target/victim. When they open the link and give required permissions, data will be captured.


---

📁 Output Files

All captured photos will be saved in the uploads/ directory as:

YYYYMMDD_HHMMSS_microsec_<victim_ip>.jpg

Console will log:

Visitor IP

Geolocation coordinates

Saved photo path



---

🛡️ License

This project is licensed under the MIT License.
See LICENSE for details.


---

🔒 Disclaimer

This project is for educational and ethical hacking purposes only.
Do not use it for unauthorized tracking, spying, or illegal activities.
The developer is not responsible for any misuse of this tool.


---

🙌 Credits

Developed with ❤️ by Phoenix Editz
GitHub: Unsagtools

---
