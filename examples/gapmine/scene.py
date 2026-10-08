"""GapMine mobile-feed concept: a large market gap with responsive edge data.

Designed at 4:5 for an X phone feed. Artwork is a metaphor; product claims and
numbers are composited from the dated public-source fact manifest.
"""
from __future__ import annotations
import math
import random
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

SIZE=(1080,1350)
FPS=24
DURATION=16.0
W,H=SIZE
ROOT=Path(__file__).resolve().parents[2]
FONT=ROOT/'assets/fonts/SpaceGrotesk-Variable.ttf'
DARK=Image.open(ROOT/'assets/gapmine-market-dark.png').convert('RGB')
LIT=Image.open(ROOT/'assets/gapmine-market-lit.png').convert('RGB')
BLACK=(2,8,17)
WHITE=(239,248,251)
CYAN=(63,216,246)
GOLD=(255,187,76)
MUTED=(143,181,199)
R=random.Random(168)
SEEDS=[(R.random(),R.random(),R.random()) for _ in range(105)]
YY,XX=np.indices((H,W),dtype=np.float32)

def face(size,weight=500):
    f=ImageFont.truetype(str(FONT),size)
    try:f.set_variation_by_axes([weight])
    except (AttributeError,OSError,ValueError):pass
    return f

F15=face(19,500);F18=face(23,500);F22=face(28,500)
F26=face(34,600);F30=face(40,600);F38=face(53,700)
F48=face(67,700);F66=face(92,700)

def cl(v):return max(0.,min(1.,v))
def sm(v):v=cl(v);return v*v*(3-2*v)
def fade(t,a,b,r=.35):return sm((t-a)/r)*(1-sm((t-(b-r))/r))
def C(c,a):return (*c,int(255*cl(a)))
def T(d,xy,s,f,c=WHITE,a=1,anchor=None):
    if a>0:d.text(xy,s,font=f,fill=C(c,a),anchor=anchor)
def L(d,coords,c=CYAN,a=.3,w=2):
    d.line(coords,fill=C(c,a),width=w)

# One fixed shading layer makes the right and bottom dashboard zones readable
# while the central image remains dominant and occupies the whole mobile card.
SHADE=Image.new('RGBA',SIZE)
_p=SHADE.load()
for _y in range(H):
    for _x in range(W):
        right=sm((_x-620)/400)
        top=1-sm((_y-80)/130)
        bottom=sm((_y-965)/310)
        left=1-sm((_x-0)/170)
        alpha=max(.10,.68*right,.59*top,.80*bottom,.30*left)
        _p[_x,_y]=(0,7,15,int(255*alpha))

def hero(t):
    push=.08+.84*sm((t-2.8)/3.8)-.55*sm((t-10.1)/2.3)
    mx=int(10+178*push);my=int(16+222*push)
    drift=int(24*sm((t-6.2)/1.2)-24*sm((t-9.7)/1.0))
    box=(mx+drift,my,DARK.width-mx+drift,DARK.height-my)
    base=ImageOps.fit(DARK.crop(box),SIZE,method=Image.Resampling.BICUBIC)
    lit=ImageOps.fit(LIT.crop(box),SIZE,method=Image.Resampling.BICUBIC)
    # Discovery propagates through the canyon, then heats the adjoining city.
    # This spatial event replaces the old whole-image crossfade.
    frontier=95+1130*sm((t-3.05)/6.3)
    spread=105+310*sm((t-4.1)/4.2)
    axis=515+25*np.sin(YY/170+t*.07)
    down=np.clip((frontier-YY)/115,0,1)
    sideways=np.clip((spread-np.abs(XX-axis))/95,0,1)
    wide=sm((t-9.2)/1.6)
    mask=Image.fromarray(np.uint8(255*np.maximum(down*sideways,wide)),'L')
    image=Image.composite(lit,base,mask)
    pulse=max(0.,1-abs(t-5.2)/.65)
    if pulse:image=ImageEnhance.Brightness(image).enhance(1+.34*pulse)
    return image.convert('RGBA')

def motion(im,t):
    layer=Image.new('RGBA',SIZE);d=ImageDraw.Draw(layer)
    for sx,sy,z in SEEDS:
        x=(sx*W+t*(9+z*28))%W;y=sy*H
        d.ellipse((x,y,x+1.8,y+1.8),fill=C(CYAN,.09+.32*z))
    for k in range(30):
        side=k%2
        x0=1080 if side else 0
        y0=125+(k*57)%800
        x1=514+(k%5-2)*16
        y1=515+(k%7-3)*27
        u=(t*.34+k*.137)%1
        v=max(0,u-.085)
        x=x0+(x1-x0)*u;y=y0+(y1-y0)*u+55*math.sin(math.pi*u)
        px=x0+(x1-x0)*v;py=y0+(y1-y0)*v+55*math.sin(math.pi*v)
        a=(.12+.63*sm((t-1.4)/2))*(1-.15*sm((t-12)/2))
        col=GOLD if k%7==0 else CYAN
        L(d,(px,py,x,y),col,a,2)
        d.ellipse((x-3,y-3,x+3,y+3),fill=C(WHITE,a))
    for cue,col in ((5.15,GOLD),(10.5,CYAN)):
        u=t-cue
        if 0<u<1.4:
            r=30+430*sm(u/1.4)
            d.ellipse((514-r,526-r,514+r,526+r),outline=C(col,.55*(1-u/1.4)),width=4)
    # The opening itself keeps changing after illumination: coherent data veins
    # descend through the canyon and resolve into a source-linked discovery.
    grow=sm((t-4.1)/5.7)
    for k in range(17):
        x0=372+k*18+8*math.sin(k*2.7)
        y0=275+(k%4)*21
        y1=y0+(780-y0)*grow
        wobble=11*math.sin(k*1.5+t*.7)
        col=GOLD if k%3 else CYAN
        L(d,(x0,y0,x0+wobble,y1),col,.06+.39*grow,1 if k%2 else 2)
        if grow>.05:d.ellipse((x0+wobble-2,y1-2,x0+wobble+2,y1+2),fill=C(WHITE,.5*grow))
    # Physical reticle stays anchored over the canyon during the reveal.
    a=sm((t-2.4)/.7)
    for r in (105,158):
        start=int(t*44)%360
        d.arc((514-r,526-r,514+r,526+r),start,start+78,fill=C(CYAN,.55*a),width=3)
        d.arc((514-r,526-r,514+r,526+r),start+180,start+253,fill=C(GOLD,.49*a),width=3)
    im.alpha_composite(layer)

def panel(d,box,color=CYAN):
    x0,y0,x1,y1=box
    d.rounded_rectangle(box,radius=13,fill=(2,12,24,218),outline=C(color,.52),width=2)
    L(d,(x0+15,y0+16,x0+55,y0+16),color,.95,3)
    L(d,(x0+15,y0+16,x0+15,y0+45),color,.95,3)

def wave(d,x,y,w,t,color=CYAN,phase=0):
    pts=[]
    for i in range(45):
        u=i/44
        yy=y+8*math.sin(u*15+t*2+phase)+4*math.sin(u*39-t+phase)
        pts.append((x+w*u,yy))
    d.line(pts,fill=C(color,.55),width=2)
    mark=pts[int(((t*.19+phase*.17)%1)*44)]
    d.ellipse((mark[0]-4,mark[1]-4,mark[0]+4,mark[1]+4),fill=C(WHITE,.94))

def hud(im,t,f):
    layer=Image.new('RGBA',SIZE);d=ImageDraw.Draw(layer)
    # Header and a sparse title leave the huge landscape unobstructed.
    d.rounded_rectangle((22,26,1058,124),radius=13,fill=(2,9,18,223),outline=C(CYAN,.34),width=2)
    T(d,(47,49),f['name']['display'],F38)
    stage='LISTEN' if t<3.4 else 'DISCOVER' if t<6.7 else 'SCORE' if t<10.5 else 'DELIVER'
    T(d,(1032,73),stage,F18,CYAN,1,'ra')
    a=fade(t,.3,3.9,.55)
    T(d,(47,163),'HIDDEN IN THE NOISE',F30,WHITE,a)
    T(d,(48,209),f['source_types']['display'],F15,CYAN,a)
    # Three compact right-side panels stay inside the phone-feed frame.
    panel(d,(755,281,1050,414),CYAN)
    T(d,(777,304),'01  /  INPUT',F15,CYAN)
    T(d,(776,335),f['signals']['display'],F30,WHITE,sm((t-.2)/.6))
    T(d,(777,385),f['signals_label']['display'],F15,MUTED)
    panel(d,(755,431,1050,559),CYAN)
    T(d,(777,454),'02  /  COVERAGE',F15,CYAN)
    T(d,(776,485),f['communities']['display'],F30,WHITE,sm((t-.5)/.5))
    T(d,(777,533),f['communities_label']['display'],F15,MUTED)
    panel(d,(755,576,1050,752),GOLD)
    T(d,(777,599),'03  /  DEMAND',F15,GOLD)
    posts=f['top_posts']['display'].split(' ',1)[0]
    T(d,(777,635),posts,F48,GOLD,sm((t-5.8)/.4))
    T(d,(822,650),'BUILDER POSTS ASKING',F15,WHITE,sm((t-5.8)/.4))
    T(d,(778,704),f['top_people']['display'],F22,CYAN,sm((t-6.4)/.4))
    # Score bars activate sequentially; they are named dimensions, not fake
    # numerical scores.
    panel(d,(755,768,1050,983),CYAN)
    T(d,(777,791),f['five_label']['display'],F18,CYAN)
    for i,name in enumerate(('PAIN','DEMAND','SUPPLY','TRIGGER','PAY')):
        y=836+i*29
        active=sm((t-(7.0+i*.53))/.34)
        d.ellipse((778,y+7,789,y+18),fill=C(GOLD if active>.8 else CYAN,.55+.45*active))
        T(d,(799,y),name,F18,WHITE,.48+.52*active)
        L(d,(900,y+14,1027,y+14),CYAN,.18,2)
        L(d,(900,y+14,900+127*active,y+14),GOLD,.75*active,3)
    # A source quote stays near the central transformation but never crowds it.
    qa=fade(t,1.55,9.2,.45);qb=fade(t,8.9,16,.5)
    d.rounded_rectangle((30,833,698,961),radius=13,fill=(2,11,22,190),outline=C(GOLD,.45),width=2)
    T(d,(54,854),'PUBLIC SOURCE / DISCUSSION',F15,GOLD)
    T(d,(54,891),'“'+f['quote_monetise']['display']+'”',F26,WHITE,qa)
    T(d,(54,891),'“'+f['quote_conversion']['display']+'”',F22,WHITE,qb)
    wave(d,55,943,609,t,GOLD,2)
    # Main output appears as a broad on-world finding, before the bottom data.
    result=sm((t-10.5)/.55)
    if result:
        d.rounded_rectangle((30,992,1050,1104),radius=15,fill=(2,10,20,int(232*result)),
                            outline=C(GOLD,.83*result),width=2)
        T(d,(56,1010),f['top_title']['display'],F30,WHITE,result)
        T(d,(56,1062),f['validated']['display']+'  /  '+f['top_posts']['display']+'  /  '+f['top_people']['display'],F18,GOLD,result)
    else:
        d.rounded_rectangle((30,992,1050,1104),radius=15,fill=(2,10,20,192),outline=C(CYAN,.32),width=2)
        T(d,(55,1027),f['real_signals']['display'],F30,WHITE,fade(t,.5,10.5,.5))
        T(d,(772,1042),'SIGNAL → OPPORTUNITY',F15,CYAN)
    # The lower row supplies the dense data framing visible in the reference.
    panel(d,(30,1123,355,1285),CYAN)
    T(d,(55,1146),'SOURCE ACTIVITY',F15,CYAN)
    for j in range(4):wave(d,55,1191+j*18,271,t,CYAN,j*.8)
    panel(d,(372,1123,710,1285),GOLD)
    T(d,(397,1146),'OPPORTUNITY CARDS',F15,GOLD)
    T(d,(397,1190),f['cards']['display'],F38,WHITE)
    T(d,(397,1249),f['cards_label']['display'],F15,MUTED)
    panel(d,(727,1123,1050,1285),CYAN)
    T(d,(752,1146),'SOURCE-LINKED',F15,CYAN)
    T(d,(752,1187),f['validated']['display'],F30,WHITE,sm((t-10.5)/.5))
    T(d,(752,1248),f['snapshot']['display'],F15,MUTED)
    T(d,(36,1318),'GAPMINE.COM  /  UNOFFICIAL CONCEPT',F15,MUTED)
    im.alpha_composite(layer)

def render(t,facts):
    im=hero(t)
    im.alpha_composite(SHADE)
    motion(im,t)
    hud(im,t,facts)
    return im.convert('RGB')
