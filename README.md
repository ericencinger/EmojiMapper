# 📸 EmojiMapper

A **tiny (~100 LOC) Jetson demo** that turns real-time object detections into an animated emoji HUD-style overlay, streamed to your browser with Flask + Socket.IO.

<p align="center">
  <em>SSD-Mobilenet-V2 → emoji grid → browser — 100 % on-device, no cloud needed.</em><br/>
</p>

---

## ✨ What it does

1. Opens a camera (`/dev/video0` by default).  
2. Runs **`jetson.inference.detectNet`** with the built-in **SSD-Mobilenet-V2** model.  
3. Maps each detected class to an emoji (see `EMOJI` in `emojimapping.py`).  
4. Streams detections via WebSockets to a minimalist HTML page that  
   * positions the emoji over the object’s centre (mirrored x-axis for “selfie” view),  
   * scales emoji size to bounding-box area,  
   * updates ~10 fps with a lightweight CSS transition.

Result: a playful “emoji radar” you can open from any device on the same network.

---

## 🚀 Quick start

```bash
# on the Jetson (JetPack 6+)
sudo apt update
sudo apt install python3-pip -y
```
runtime deps
```bash
pip3 install flask flask-socketio eventlet jetson-inference
```
grab the repo
```bash
git clone https://github.com/ericencinger/EmojiMapper.git
cd EmojiMapper/src
```
install runtime deps
```bash
pip3 install -r requirements.txt
```
run!
```bash
python3 emojimapping.py
```

