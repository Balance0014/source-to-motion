#!/usr/bin/env python3
"""Original cinematic pulse bed for the GapMine market-gap concept film."""
import math
import random
import wave
from pathlib import Path

SR=44100
DURATION=16
OUT=Path(__file__).with_name('audio.wav')
R=random.Random(806)
CUES=(1.6,3.4,5.15,7.0,10.55,13.4)

def clip(v):return max(-.96,min(.96,v))

def main():
    with wave.open(str(OUT),'wb') as wav:
        wav.setnchannels(2);wav.setsampwidth(2);wav.setframerate(SR)
        block=bytearray()
        for n in range(SR*DURATION):
            t=n/SR
            fade=min(1,t/.45,(DURATION-t)/.6)
            # Low engine, beating machinery, and rising filtered noise.
            drone=(.058*math.sin(math.tau*48*t)+.031*math.sin(math.tau*72*t)
                   +.016*math.sin(math.tau*144*t))
            beat=t%.5
            kick=.11*math.sin(math.tau*(78-37*beat)*beat)*math.exp(-24*beat)
            glide=.008*math.sin(math.tau*(250*t+7*t*t))
            rise=0
            if 3.0<t<5.15:rise=.055*((t-3)/2.15)**2*(R.random()*2-1)
            hit=0
            for j,cue in enumerate(CUES):
                u=t-cue
                if 0<=u<1:
                    intensity=1.55 if j in (2,4) else .7
                    hit+=intensity*(.15*math.sin(math.tau*(94-52*u)*u)*math.exp(-7*u)
                                    +.035*(R.random()*2-1)*math.exp(-17*u))
            signal=clip((drone+kick+glide+rise+hit)*fade)
            pan=.22*math.sin(math.tau*.15*t)
            for side in (-1,1):
                block.extend(int(clip(signal*(1+side*pan))*32767).to_bytes(2,'little',signed=True))
            if len(block)>65536:wav.writeframes(block);block.clear()
        if block:wav.writeframes(block)
    print(OUT.resolve())

if __name__=='__main__':main()
