#!/usr/bin/env python3

import eventlet; eventlet.monkey_patch()

import os, sys, math
import jetson_utils as ju
import jetson_inference as ji
from flask import Flask, render_template_string
from flask_socketio import SocketIO

# cam + model
CAMERA="v4l2:///dev/video0"
W,H   =1280,720
MODEL ="ssd-mobilenet-v2"
THR   =0.5
LAB   ="labels.txt"

# html ui
HTML='''
<!DOCTYPE html><html><head><meta charset="utf-8">
<title>emoji overlay</title>
<style>
 body{margin:0;padding:20px;background:#000;color:#fff;font-family:arial}
 #status{text-align:center;color:#0f0;margin-bottom:10px}
 #frame{position:relative;width:640px;height:360px;max-width:90vw;margin:0 auto;border:2px solid #555}
 .emoji{position:absolute;transform:translate(-50%,-50%);pointer-events:none;transition:.08s linear}
</style></head><body>
<div id="status">waiting…</div><div id="frame"></div>
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
<script>
const f=document.getElementById('frame'),s=document.getElementById('status'),sock=io();
const pool={};                                   // id → element

sock.on('detections',list=>{
  s.textContent=`detected ${list.length}`;
  const alive=new Set();
  list.forEach(o=>{
    let n=pool[o.id];
    if(!n){ n=document.createElement('div'); n.className='emoji'; pool[o.id]=n; f.appendChild(n); }
    n.textContent   = o.emoji;                  // update each tick
    n.style.left    = (o.x*100)+'%';
    n.style.top     = (o.y*100)+'%';
    n.style.fontSize= o.fs+'px';
    n.style.opacity = 1;
    alive.add(o.id);
  });
  // drop gone ids
  for(const id in pool) if(!alive.has(+id)){ f.removeChild(pool[id]); delete pool[id]; }
});
sock.on('camera_error',m=>s.textContent=m);
</script></body></html>
'''

app=Flask(__name__)
socketio=SocketIO(app,cors_allowed_origins='*',async_mode='eventlet')

@app.route('/')
def idx(): return render_template_string(HTML)

# coco → emoji
EMOJI={'person':'👤','bicycle':'🚲','car':'🚗','motorcycle':'🏍️','airplane':'✈️','bus':'🚌',
'train':'🚆','truck':'🚚','boat':'⛵','traffic light':'🚦','fire hydrant':'🧯','stop sign':'🛑',
'parking meter':'🅿️','bench':'🪑','bird':'🐦','cat':'🐱','dog':'🐕','horse':'🐴','sheep':'🐑',
'cow':'🐄','elephant':'🐘','bear':'🐻','zebra':'🦓','giraffe':'🦒','backpack':'🎒','umbrella':'☂️',
'handbag':'👜','tie':'👔','suitcase':'💼','frisbee':'🥏','skis':'🎿','snowboard':'🏂','sports ball':'🏀',
'kite':'🪁','baseball bat':'⚾','baseball glove':'🧤','skateboard':'🛹','surfboard':'🏄','tennis racket':'🎾',
'bottle':'🍾','wine glass':'🍷','cup':'☕','fork':'🍴','knife':'🔪','spoon':'🥄','bowl':'🥣',
'banana':'🍌','apple':'🍎','sandwich':'🥪','orange':'🍊','broccoli':'🥦','carrot':'🥕','hot dog':'🌭',
'pizza':'🍕','donut':'🍩','cake':'🎂','chair':'🪑','couch':'🛋️','bed':'🛏️',
'dining table':'🍽️','toilet':'🚽','tv':'📺','laptop':'💻','mouse':'🖱️','remote':'🎛️','keyboard':'⌨️',
'cell phone':'📱','microwave':'♨️','oven':'🔥','toaster':'🍞','sink':'🚰','refrigerator':'🧊',
'book':'📚','clock':'⏰','vase':'🏺','scissors':'✂️','teddy bear':'🧸','hair drier':'💇'}

def detect_loop():
    cam=ju.videoSource(CAMERA,argv=[f'--input-width={W}',f'--input-height={H}',
                                    '--input-codec=mjpeg','--input-rate=30'])
    net=ji.detectNet(MODEL,threshold=THR,argv=[f'--labels={LAB}'])

    while True:
        img=cam.Capture()
        if img is None:
            socketio.emit('camera_error','camera timeout')
            eventlet.sleep(0.2); continue

        out=[]
        for i,d in enumerate(net.Detect(img)):
            cx=1-d.Center[0]/W                       # mirror x
            cy=d.Center[1]/H
            fs=max(15,min(100,int(math.sqrt(d.Area)/4)))
            out.append({'id':i,'emoji':EMOJI.get(net.GetClassDesc(d.ClassID),'❓'),
                        'x':cx,'y':cy,'fs':fs})
        socketio.emit('detections',out)
        eventlet.sleep(0.1)                          # ~10 fps

if __name__=='__main__':
    socketio.start_background_task(detect_loop)
    print('open → http://<jetson-ip>:5000')
    socketio.run(app,host='0.0.0.0',port=5000)
