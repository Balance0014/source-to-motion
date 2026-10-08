"""Shared compositing and six intentionally different stress-test hero scenes.

The heroes are reference implementations, not a selection menu for future users.
New sources require new visual direction; only typography, timing, and factual HUD
composition are meant to be reused.
"""
from __future__ import annotations

import math
import random
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = (1080, 1350)
FPS = 24
DURATION = 12.0
ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / "assets/fonts/SpaceGrotesk-Variable.ttf"

THEMES = {
    "uv": ((255, 132, 78), (169, 110, 255), (15, 8, 31)),
    "ollama": ((173, 255, 173), (143, 141, 255), (6, 16, 27)),
    "trivy": ((255, 83, 106), (64, 221, 244), (5, 14, 26)),
    "duckdb": ((255, 209, 74), (87, 183, 244), (10, 14, 30)),
    "tailscale": ((103, 234, 229), (200, 255, 125), (5, 19, 28)),
    "excalidraw": ((255, 171, 126), (153, 141, 255), (30, 24, 43)),
}

DETAIL_HEADINGS = {
    "uv": ("CREATE", "RESOLVE", "RUN"),
    "ollama": ("MODEL", "CHAT", "BUILD"),
    "trivy": ("TARGETS", "SCANNERS", "CHECKS"),
    "duckdb": ("FILES", "QUERY", "CLIENTS"),
    "tailscale": ("NETWORK", "ENGINE", "DEVICES"),
    "excalidraw": ("CANVAS", "COLLAB", "EXPORT"),
}

def ease(v):
    v = max(0.0, min(1.0, v))
    return v * v * (3 - 2 * v)

def rgba(c, a=1.0):
    return (*c, int(255 * max(0, min(1, a))))

@lru_cache(None)
def font(size, weight=600):
    f = ImageFont.truetype(str(FONT), size)
    try:
        f.set_variation_by_axes([weight])
    except (AttributeError, OSError, ValueError):
        pass
    return f

@lru_cache(None)
def background(project):
    a, b, dark = THEMES[project]
    im = Image.new("RGB", SIZE, dark)
    glow = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(glow)
    d.ellipse((-210, 95, 790, 1095), fill=rgba(a, .24))
    d.ellipse((240, 0, 1450, 930), fill=rgba(b, .10))
    d.ellipse((70, 765, 1000, 1545), fill=rgba(a, .11))
    glow = glow.filter(ImageFilter.GaussianBlur(135))
    im = Image.alpha_composite(im.convert("RGBA"), glow)
    layer = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(layer)
    rng = random.Random(project)
    for _ in range(180):
        x, y = rng.randrange(1080), rng.randrange(1350)
        r = rng.choice((1, 1, 2))
        d.ellipse((x-r, y-r, x+r, y+r), fill=rgba(b, rng.uniform(.08, .27)))
    for y in range(180, 1060, 60):
        d.line((10, y, 1050, y), fill=rgba(b, .045), width=1)
    return Image.alpha_composite(im, layer)

@lru_cache(None)
def art(project):
    return Image.open(ROOT / 'assets' / f'{project}-hero.png').convert('RGB')

@lru_cache(None)
def dark_art(project):
    source=art(project)
    if project=='excalidraw':
        return source.filter(ImageFilter.GaussianBlur(7)).point(lambda v:int(v*.62))
    pixels=np.asarray(source).astype(np.float32)
    gray=(pixels[:,:,0]*.25+pixels[:,:,1]*.6+pixels[:,:,2]*.15)
    base=np.empty_like(pixels)
    base[:,:,0]=gray*.24
    base[:,:,1]=gray*.31
    base[:,:,2]=gray*.42
    return Image.fromarray(np.clip(base,0,255).astype('uint8'),'RGB')

@lru_cache(None)
def coordinates():
    yy,xx=np.indices((SIZE[1],SIZE[0]),dtype=np.float32)
    return xx,yy

def reveal_mask(project,t):
    xx,yy=coordinates()
    if project=='uv':
        dist=np.sqrt(((xx-495)*1.05)**2+((yy-555)*1.07)**2)
        edge=90+920*ease((t-1.3)/6.7)
        m=(edge-dist)/95
    elif project=='ollama':
        edge=-80+132*t
        m=(edge-xx+32*np.sin(yy*.014+t*1.7))/80
    elif project=='trivy':
        edge=50+145*max(0,t-.5)
        m=(edge-yy+24*np.sin(xx*.014+t))/68
    elif project=='duckdb':
        edge=-100+136*t
        m=(edge-xx+24*np.sin(yy*.018-t))/85
    elif project=='tailscale':
        dist=np.sqrt(((xx-465)*1.08)**2+((yy-610)*.95)**2)
        edge=50+115*max(0,t-1.1)
        m=(edge-dist)/75
    else:
        edge=-100+150*t
        m=(edge-(yy*.72+xx*.26)+20*np.sin(xx*.024+yy*.013))/80
    return Image.fromarray(np.uint8(np.clip(m,0,1)*255),'L')

@lru_cache(None)
def shade():
    overlay=Image.new('RGBA',SIZE)
    p=overlay.load()
    for y in range(SIZE[1]):
        for x in range(SIZE[0]):
            right=ease((x-665)/380)
            bottom=ease((y-1000)/300)
            top=1-ease((y-10)/170)
            p[x,y]=(2,8,18,int(255*max(.02,.65*right,.75*bottom,.68*top)))
    return overlay

def art_frame(project,t):
    source=art(project)
    base=dark_art(project)
    zoom=1+.065*ease(t/6)-.025*ease((t-8)/3)
    cropw=int(source.width/zoom);croph=int(source.height/zoom)
    drift=int(9*math.sin(t*.23))
    cx=source.width//2+drift
    box=(cx-cropw//2,(source.height-croph)//2,cx+cropw//2,(source.height+croph)//2)
    lit=source.crop(box).resize(SIZE,Image.Resampling.BICUBIC)
    low=base.crop(box).resize(SIZE,Image.Resampling.BICUBIC)
    image=Image.composite(lit,low,reveal_mask(project,t)).convert('RGBA')
    if project in ('trivy','duckdb') and .5<t<9.5:
        effect=Image.new('RGBA',SIZE)
        d=ImageDraw.Draw(effect)
        if project=='trivy':
            y=50+145*(t-.5)
            d.line((55,y,735,y),fill=rgba((255,63,88),.58),width=5)
            d.line((50,y-9,745,y-9),fill=rgba((255,63,88),.16),width=19)
        else:
            x=-100+136*t
            d.line((x-105,265,x+105,980),fill=rgba((255,216,91),.62),width=5)
            d.line((x-122,265,x+88,980),fill=rgba((255,216,91),.18),width=18)
        image.alpha_composite(effect)
    image.alpha_composite(shade())
    return image

def ring(d, cx, cy, rx, ry, color, alpha, width=3, phase=0):
    points = []
    for k in range(129):
        q = 2 * math.pi * k / 128 + phase
        points.append((cx + rx * math.cos(q), cy + ry * math.sin(q)))
    d.line(points, fill=rgba(color, alpha), width=width, joint="curve")

def line(d, p, color, alpha=1, width=3):
    d.line(p, fill=rgba(color, alpha), width=width, joint="curve")

def orb(d, x, y, radius, color, alpha=1):
    d.ellipse((x-radius*2.4, y-radius*2.4, x+radius*2.4, y+radius*2.4), fill=rgba(color, alpha*.11))
    d.ellipse((x-radius*1.55, y-radius*1.55, x+radius*1.55, y+radius*1.55), fill=rgba(color, alpha*.23))
    d.ellipse((x-radius, y-radius, x+radius, y+radius), fill=rgba(color, alpha))

def polygon(d, pts, color, alpha=.5, outline=None, width=3):
    d.polygon(pts, fill=rgba(color, alpha))
    if outline:
        d.line(pts+[pts[0]], fill=rgba(outline, min(1, alpha+.3)), width=width, joint="curve")

def label(d, xy, text, size=19, color=(236,246,252), alpha=1, weight=600, anchor=None):
    d.text(xy, text, font=font(size,weight), fill=rgba(color,alpha), anchor=anchor)

def wrap_text(d, text, width, size, weight=600):
    rows=[]; current=""
    for word in text.split():
        trial=(current+" "+word).strip()
        if current and d.textbbox((0,0),trial,font=font(size,weight))[2]>width:
            rows.append(current);current=word
        else:
            current=trial
    if current:rows.append(current)
    return rows

def hero_uv(t, a, b):
    im=Image.new("RGBA",(720,780));d=ImageDraw.Draw(im)
    cx,cy=360,390
    gather=ease((t-1.2)/4);lock=ease((t-5)/2)
    # An unstructured dependency constellation contracts into a single lock core.
    for i in range(40):
        q=i*2.39996+t*.19
        r=(95+240*((i*37)%41)/41)*(1-.55*gather)
        x=cx+r*math.cos(q);y=cy+.70*r*math.sin(q)
        x2=cx+88*math.cos(q+i*.02);y2=cy+64*math.sin(q+i*.02)
        line(d,(x,y,x+(x2-x)*gather,y+(y2-y)*gather),a,.15+.32*gather,2)
        orb(d,x+(x2-x)*gather,y+(y2-y)*gather,2.8,a,.56+.4*gather)
    for k in range(5):
        r=75+k*32+6*math.sin(t*1.2+k)
        ring(d,cx,cy,r,r*.72,b,.14+.13*lock,2,t*.05)
    rad=92+16*lock
    outer=[(cx+rad*math.cos(math.pi/3*k+t*.035),cy+rad*math.sin(math.pi/3*k+t*.035)) for k in range(6)]
    polygon(d,outer,(45,26,70),.93,a,5)
    inner=[(cx+rad*.67*math.cos(math.pi/3*k-t*.22),cy+rad*.67*math.sin(math.pi/3*k-t*.22)) for k in range(6)]
    polygon(d,inner,a,.11,b,3)
    for k in range(6):line(d,(outer[k][0],outer[k][1],inner[k][0],inner[k][1]),b,.25+.45*lock,2)
    ring(d,cx,cy,52,52,a,.55+.42*lock,4,t*.1)
    label(d,(cx,cy-13),"uv",64,(255,241,230),1,700,"mm")
    if lock>0:
        for k in range(14):
            q=2*math.pi*k/14+t*.5
            r=155+25*lock
            orb(d,cx+r*math.cos(q),cy+r*.72*math.sin(q),2.2,b,.8*lock)
    return im

def hero_ollama(t,a,b):
    im=Image.new("RGBA",(720,780));d=ImageDraw.Draw(im)
    cx,cy=350,390;on=ease((t-2.4)/2.6);reply=ease((t-6.3)/1.8)
    # A local inference chamber, not an Earth/planet metaphor.
    for k in range(9):
        y=130+k*53
        x=50+37*math.sin(k*2.4+t*.15)
        line(d,(x,y,160+on*130,y),a,.08+.33*on,3)
        if on>0:orb(d,160+on*130,y,4,a,.5*on)
    for k in range(8):
        q=2*math.pi*k/8+t*.075
        p=(cx+225*math.cos(q),cy+175*math.sin(q))
        line(d,(cx,cy,*p),b,.16+.16*on,2)
        orb(d,*p,5,b,.5+.4*on)
    for j in range(6):
        yy=cy-185+j*74
        width=220+26*math.sin(t*.8+j)
        ring(d,cx,yy,width*.68,35,a,.16+.16*on,3,t*.02)
    diamond=[(cx,cy-220),(cx+175,cy-35),(cx+112,cy+190),(cx,cy+240),(cx-112,cy+190),(cx-175,cy-35)]
    polygon(d,diamond,(21,47,68),.90,b,4)
    for j in range(8):
        y0=cy-170+j*45
        line(d,(cx-95,y0,cx+95,y0+20*math.sin(j+t*.5)),a,.18+.63*on,2)
    ring(d,cx,cy,88,115,a,.45+.45*on,4,t*.08)
    orb(d,cx,cy,22,a,.55+.45*on)
    for j in range(7):
        y=245+j*55
        x=490+(j%3)*17
        line(d,(x,y,x+105*reply,y),a,.2+.55*reply,3)
        if reply:
            orb(d,x+105*reply,y,3.5,b,reply)
            q=(t*.62+j*.19)%1
            orb(d,x+105*reply*q,y,3,b,.8*reply)
    return im

def hero_trivy(t,a,b):
    im=Image.new("RGBA",(720,780));d=ImageDraw.Draw(im)
    scan=ease((t-2)/5);flag=ease((t-6.1)/1.7)
    # One container block is physically scanned layer by layer.
    front=[(158,250),(491,250),(570,340),(570,634),(235,634),(158,550)]
    top=[(158,250),(258,180),(590,180),(491,250)]
    side=[(491,250),(590,180),(647,280),(647,576),(570,634),(570,340)]
    polygon(d,top,(38,95,111),.75,b,4)
    polygon(d,side,(23,50,78),.86,b,4)
    polygon(d,front,(17,40,59),.86,b,5)
    for k in range(7):
        x=185+k*51
        line(d,(x,275,x,600),b,.24,3)
        line(d,(x+2,275,x+2,600),a,.08,1)
    for k in range(3):
        y=325+k*100
        line(d,(178,y,546,y),b,.28,3)
    sy=196+scan*440
    polygon(d,[(130,sy),(590,sy),(668,sy-56),(208,sy-56)],a,.11*scan,a,2)
    line(d,(130,sy,590,sy),a,.25+.68*scan,6)
    line(d,(590,sy,668,sy-56),a,.25+.68*scan,4)
    for k,(x,y) in enumerate(((279,355),(435,455),(342,548))):
        reveal=ease((scan-((y-196)/440)+.12)*7)*flag
        if reveal:
            pulse=25+9*math.sin(t*5+k)
            ring(d,x,y,pulse,pulse,a,.8*reveal,3)
            line(d,(x-17,y-17,x+17,y+17),a,reveal,4)
            line(d,(x+17,y-17,x-17,y+17),a,reveal,4)
    if t>7:
        sweep=((t-7)*.42)%1
        y=255+350*sweep
        line(d,(174,y,558,y),a,.35,3)
    return im

def hero_duckdb(t,a,b):
    im=Image.new("RGBA",(720,780));d=ImageDraw.Draw(im)
    query=ease((t-2.3)/3.6);result=ease((t-6.2)/2)
    # CSV/Parquet rows become a query plane and a clean result stack.
    for k in range(9):
        x=80+k*65
        h=145+((k*73)%205)
        rise=ease((t-.3-k*.16)/.8)
        y=620-h*rise
        polygon(d,[(x,y),(x+42,y-18),(x+42,620-18),(x,620)],(24,62,88),.84,b,2)
        polygon(d,[(x,y),(x+25,y-22),(x+66,y-40),(x+42,y-18)],a,.28,a,2)
        for row in range(4):
            yy=y+28+row*29
            if yy<610:line(d,(x+5,yy,x+34,yy-11),a,.30+.35*query,2)
    plane_y=125+450*query
    polygon(d,[(50,plane_y),(520,plane_y-160),(685,plane_y-80),(210,plane_y+85)],a,.08*query,a,3)
    for k in range(5):
        yy=295+k*48
        alpha=result*ease((t-6.2-k*.16)/.8)
        polygon(d,[(235,yy),(523,yy-98),(612,yy-58),(324,yy+40)],(64,81,96),.31*alpha,b,2)
        line(d,(350,yy+4,515,yy-52),a,.7*alpha,3)
        if result:
            q=(t*.55+k*.14)%1
            orb(d,350+165*q,yy+4-56*q,3.2,a,.85*alpha)
    label(d,(345,391),"SELECT *",37,(255,242,209),result,700,"mm")
    return im

def hero_tailscale(t,a,b):
    im=Image.new("RGBA",(720,780));d=ImageDraw.Draw(im)
    nodes=[(360,365),(125,245),(568,245),(120,545),(567,558),(355,665),(365,115)]
    connect=ease((t-2)/5)
    # Separate device islands join a mesh; there is no globe or hub-only star.
    edges=[(0,1),(0,2),(0,3),(0,4),(1,6),(2,6),(1,3),(2,4),(3,5),(4,5),(3,4)]
    for i,j in edges:
        x1,y1=nodes[i];x2,y2=nodes[j]
        on=ease((connect-(i+j)*.045)*3)
        line(d,(x1,y1,x1+(x2-x1)*on,y1+(y2-y1)*on),a,.1+.54*on,3)
        if on>.2:
            q=(t*.55+i*.13+j*.07)%1
            orb(d,x1+(x2-x1)*q,y1+(y2-y1)*q,4,b,on)
    for k,(x,y) in enumerate(nodes):
        r=42 if k==0 else 31
        angle=t*.05+k
        points=[(x+r*math.cos(angle+q*math.pi/3),y+r*math.sin(angle+q*math.pi/3)) for q in range(6)]
        polygon(d,points,(24,69,73),.93,a,3)
        ring(d,x,y,r*.65,r*.65,b,.22+.35*connect,2,t*.08)
        orb(d,x,y,5,a,.75+.25*connect)
    ring(d,360,365,115+18*math.sin(t*.8),78+10*math.sin(t*.8),a,.3*connect,3,t*.08)
    return im

def hero_excalidraw(t,a,b):
    im=Image.new("RGBA",(720,780));d=ImageDraw.Draw(im)
    # Draw only translucent ink paths on the generated sheet. The paper and
    # marks underneath remain visible; the artwork is never covered by a UI.
    def stroke(points,start,duration,color=b,w=5):
        u=ease((t-start)/duration)
        if u<=0:return
        end=max(2,int((len(points)-1)*u)+1)
        d.line(points[:end],fill=rgba(color,.78),width=w,joint='curve')
        orb(d,*points[end-1],4,a,.8)
    paths=[
        [(115+i*5,275+30*math.sin(i*.10)+i*.6) for i in range(80)],
        [(515-i*4,232+i*2+12*math.sin(i*.16)) for i in range(75)],
        [(180+i*3,515-i*1.2+18*math.sin(i*.11)) for i in range(115)],
        [(560-i*3.3,500+i*.7+9*math.sin(i*.18)) for i in range(115)],
        [(140+i*4,630-i*.9+12*math.sin(i*.13)) for i in range(110)],
    ]
    for j,pts in enumerate(paths):stroke(pts,8 if j==4 else 1+j*1.45,2.6 if j==4 else 1.5,b if j%2 else a,5 if j==4 else 4)
    return im

HEROES={"uv":hero_uv,"ollama":hero_ollama,"trivy":hero_trivy,
        "duckdb":hero_duckdb,"tailscale":hero_tailscale,"excalidraw":hero_excalidraw}

def draw_hud(im,t,project,facts):
    a,b,_=THEMES[project]
    layer=Image.new("RGBA",SIZE)
    d=ImageDraw.Draw(layer)
    white=(238,245,250);muted=(151,174,192)
    d.rounded_rectangle((24,28,1056,130),radius=17,fill=(2,9,22,230),outline=rgba(a,.68),width=2)
    label(d,(49,51),facts['name']['display'],54,white,1,700)
    label(d,(1032,69),"SOURCE → MOTION",20,a,1,600,"ra")
    if project=='excalidraw':
        d.rounded_rectangle((25,145,740,211),radius=13,fill=(2,8,19,179))
        label(d,(42,160),facts['hero']['display'],31,white,1,700)
    else:
        label(d,(42,155),facts['hero']['display'],31,white,1,700)
    # Perimeter panels are factual, compact, and synchronized to the central event.
    panels=[("SOURCE",'input',260,1.0),("TRANSFORM",'transform',444,4.0),("RESULT",'result',628,7.0)]
    if project=='uv':
        panels[-1]=("ASTRAL CLAIM",'metric',628,7.0)
    for idx,(caption,fid,y,when) in enumerate(panels):
        active=ease((t-when)/.9)
        accent=a if idx!=1 else b
        d.rounded_rectangle((756,y,1052,y+168),radius=15,fill=(2,11,24,211),outline=rgba(accent,.28+.59*active),width=2)
        line(d,(777,y+21,814+38*active,y+21),accent,.6+.4*active,3)
        label(d,(779,y+37),f"0{idx+1} / {caption}",19,accent,1,700)
        txt=facts[fid]['display']
        rows=wrap_text(d,txt,250,28,700)
        if len(rows)>3:rows=rows[:2]+[' '.join(rows[2:])]
        for j,row in enumerate(rows):
            size=27 if len(row)<18 else 23
            label(d,(779,y+80+j*32),row,size,white,.24+.76*active,700)
        if project=='uv' and idx==2:
            label(d,(779,y+123),facts['caveat']['display'],15,muted,active,600)
        for k in range(6):
            x0=780+k*40
            line(d,(x0,y+146,x0+24*ease((t-when-k*.13)/.7),y+146),accent,.16+.72*active,3)
    # GitHub popularity is a dated repository snapshot, never a product KPI.
    snap=ease((t-5.4)/1.0)
    d.rounded_rectangle((756,812,1052,986),radius=15,fill=(2,11,24,216),outline=rgba(b,.28+.53*snap),width=2)
    label(d,(778,829),"GITHUB SNAPSHOT",18,b,1,700)
    label(d,(778,855),facts['snapshot_date']['display'],16,muted,1,500)
    for x,fid,caption in ((779,'stars','STARS'),(920,'forks','FORKS')):
        value=facts[fid]['display']
        size=34 if len(value)<=6 else 30
        label(d,(x,889),value,size,white,.18+.82*snap,700)
        label(d,(x,939),caption,18,muted,.4+.6*snap,700)
        line(d,(x,970,x+100*snap,970),a if fid=='stars' else b,.25+.5*snap,3)
    # Six project-specific, source-backed details replace decorative analyzer bars.
    d.rounded_rectangle((27,1012,1053,1285),radius=16,fill=(2,9,21,225),outline=rgba(a,.45),width=2)
    headings=DETAIL_HEADINGS[project]
    for idx,(x0,x1) in enumerate(((52,360),(390,720),(750,1028))):
        if idx:line(d,(x0-17,1034,x0-17,1263),a,.25,2)
        label(d,(x0,1038),headings[idx],19,b if idx==1 else a,1,700)
        for row in range(2):
            active=ease((t-(1.1+idx*2.7+row*.65))/.8)
            yy=1094+row*75
            color=a if row==0 else b
            orb(d,x0+7,yy+13,4,color,.2+.8*active)
            detail=facts[f'detail_{idx*2+row+1}']['display']
            size=26 if len(detail)<23 else 23
            for k,part in enumerate(wrap_text(d,detail,x1-x0-30,size,650)[:2]):
                label(d,(x0+21,yy+k*29),part,size,white,.22+.78*active,650)
            line(d,(x0+20,yy+59,x0+20+(x1-x0-48)*active,yy+59),color,.15+.45*active,2)
    if project=='uv':
        label(d,(54,1250),"ASTRAL CLAIM: "+facts['metric']['display']+" · "+facts['caveat']['display'],17,muted,ease((t-7.7)/.6),500)
    else:
        label(d,(53,1250),"UNOFFICIAL CONCEPT  /  README FACTS + DATED GITHUB SNAPSHOT",16,muted,1,500)
    label(d,(31,1314),f"{project.upper()}  /  SOURCE-CHECKED CONTENT",17,muted,1,500)
    im.alpha_composite(layer)

def render(t,facts,project):
    a,b,_=THEMES[project]
    im=art_frame(project,t)
    hero=HEROES[project](t,a,b)
    # Three camera beats: establish, inspect, pull back for the factual output.
    zoom=1+.12*ease((t-2.2)/2.4)-.13*ease((t-8.2)/2.1)
    hh=int(780*zoom);ww=int(720*zoom)
    hero=hero.resize((ww,hh),Image.Resampling.BICUBIC)
    alpha=hero.getchannel('A').point(lambda q:int(q*(.48 if project=='excalidraw' else .66)))
    hero.putalpha(alpha)
    x=int(12-(ww-720)/2+16*math.sin(t*.19));y=int(185-(hh-780)/2)
    im.alpha_composite(hero,(x,y))
    draw_hud(im,t,project,facts)
    return im.convert("RGB")
