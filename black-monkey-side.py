import math
from PIL import Image, ImageDraw
S=3; W=512; N=36
BLACK=(18,16,24); PURP=(70,20,130); PURP2=(100,40,175); PURPL=(140,80,220)
def frame(i):
    t=i/N
    im=Image.new("RGB",(W*S,W*S),(57,255,20)); d=ImageDraw.Draw(im)
    def P(pts): return [(x*S,y*S) for x,y in pts]
    def E(cx,cy,rx,ry,fill,rot=0):
        a=math.radians(rot); pts=[]
        for k in range(40):
            u=2*math.pi*k/40; x=math.cos(u)*rx; y=math.sin(u)*ry
            pts.append((cx+x*math.cos(a)-y*math.sin(a),cy+x*math.sin(a)+y*math.cos(a)))
        d.polygon(P(pts),fill=fill)
    def limb(pts,w,fill):
        d.line(P(pts),fill=fill,width=int(w*S),joint="curve")
        for x,y in (pts[0],pts[-1]): E(x,y,w/2,w/2,fill)
    # speed streaks (drift left, seamless)
    for k,(y,l) in enumerate([(70,120),(150,80),(400,140),(470,90),(330,70)]):
        x=(k*210+60-t*W*1.0)%(W+240)-120
        d.line(P([(x,y),(x+l,y)]),fill=(200,255,150),width=6*S)
    flap=math.sin(t*2*math.pi*2)
    bob=-flap*10
    def wing(px,py,ph,far):
        f=math.sin((t+ph)*2*math.pi*2)
        c=225+55*f
        for j,(off,L) in enumerate([(-40,150),(-20,175),(0,185),(20,175),(40,150)]):
            a=math.radians(c+off*0.9)
            cx=px+math.cos(a)*L/2; cy=py+bob+math.sin(a)*L/2
            pts=[]
            for k in range(28):
                u=2*math.pi*k/28; x=math.cos(u)*L/2; y=math.sin(u)*19
                pts.append((cx+x*math.cos(a)-y*math.sin(a),cy+x*math.sin(a)+y*math.cos(a)))
            col=(PURP if j%2==0 else PURP2) if not far else (45,12,85)
            d.polygon(P(pts),fill=col)
            d.line(P(pts+[pts[0]]),fill=BLACK,width=3*S)
    wing(250,255,0.06,True)          # far wing
    # tail (wags behind)
    tail=[(170+ -k*14, 285+bob - k*10 + 14*math.sin(t*2*math.pi*2+k*0.7)) for k in range(7)]
    limb(tail,14,BLACK); E(*tail[-1],9,9,PURP)
    # far limbs
    limb([(290,300+bob),(345,330+bob),(375,315+bob)],20,(10,8,14))
    limb([(180,320+bob),(130,360+bob),(95,350+bob)],22,(10,8,14))
    # body
    E(235,290+bob,100,62,BLACK,-8)
    E(255,312+bob,60,32,PURP,-8)
    # near limbs
    limb([(165,325+bob),(115,372+bob),(80,365+bob)],24,BLACK); E(78,365+bob,15,12,PURP)
    limb([(300,290+bob),(360,325+bob),(398,305+bob)],22,BLACK); E(402,303+bob,14,12,PURP)
    # head
    hx,hy=345,225+bob
    E(hx-22,hy-8,22,22,BLACK); E(hx-22,hy-8,12,12,PURP)      # ear
    E(hx,hy,58,54,BLACK)
    E(hx+38,hy+18,36,28,PURP2)                               # muzzle
    E(hx+30,hy-2,34,22,PURP,-10)                             # brow/face patch
    # eye
    ph=(t*2)%1
    blink=0.12 if 0.46<ph<0.54 else 1
    E(hx+34,hy-6,11,11*blink+1,(255,255,255))
    if blink>0.5:
        E(hx+38,hy-5,6,6,BLACK); E(hx+40,hy-8,2,2,(255,255,255))
    else:
        d.line(P([(hx+23,hy-6),(hx+45,hy-6)]),fill=BLACK,width=3*S)
    d.line(P([(hx+25,hy-24),(hx+50,hy-16)]),fill=BLACK,width=4*S)  # brow
    E(hx+68,hy+10,4,3,BLACK)                                  # nostril
    d.arc([ (hx+28)*S,(hy+18)*S,(hx+72)*S,(hy+46)*S],10,90,fill=BLACK,width=3*S)  # smile
    wing(235,258,0.0,False)           # near wing on top of body
    return im.resize((W,W),Image.LANCZOS)
fr=[frame(i) for i in range(N)]
fr[0].save("black-monkey-side.gif",save_all=True,append_images=fr[1:],duration=60,loop=0,optimize=True)
fr[0].save("black-monkey-side-still.png")
fr[0].resize((250,250),Image.LANCZOS).save("black-monkey-side-250.png")
m=Image.new("RGB",(1536,512))
for k,i in enumerate((0,5,13)): m.paste(fr[i],(k*512,0))
m.save("../monkey2-check.png")
