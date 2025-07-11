# 📸 EmojiMapper

A **tiny (~100 LOC) Jetson demo** that turns real-time object detections into an animated emoji HUD-style overlay, streamed to your browser with Flask + Socket.IO.

<p align="center">
  <em>On-device only – no cloud or API calls required.</em><br/>
</p>

---

## ✨ What it does

1. Opens a camera (`/dev/video0` by default).  
2. Runs **`jetson.inference.detectNet`** with the built-in **SSD-Mobilenet-V2** model.  
3. Maps each detected class to an emoji (see `EMOJI` in `emojimapping.py`).  
4. Streams detections via WebSockets to a HTML page that  
   * positions the emoji over the object’s centre,
   * scales emoji size to bounding-box area,  
   * updates ~10 fps with a lightweight CSS transition.

Result: a playful “emoji radar” you can open from any browser on the same network.

---
## 🧪 Tested On

- Jetson Orin Nano (JetPack 6.0)
- Logitech USB webcam (/dev/video0)
- Python 3.10
- Chrome & Firefox (desktop and mobile)

## 🚀 Quick start

On the Jetson (JetPack 6+)
```bash
sudo apt update
sudo apt install python3-pip -y
```
Grab the repo
```bash
git clone https://github.com/ericencinger/EmojiMapper.git
cd EmojiMapper
```
Install runtime deps
```bash
pip3 install -r requirements.txt
```
Run!
```bash
python3 emoji_mapper.py
```
Once running, open your browser and go to:
```bash
http://<your-jetson-ip>:5000
```
*Replace `<your-jetson-ip>` with the IP address of your Jetson.*
