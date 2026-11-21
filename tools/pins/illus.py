from PIL import Image, ImageDraw
NAVY=(29,43,58); MAR=(124,45,55); PINK=(232,196,200); CREAM=(250,247,242); SAND=(241,232,227)
def frame(d,box): d.rounded_rectangle(box,radius=40,fill=SAND)
def alarm(d,cx,cy):
    d.arc([cx-90,cy-150,cx+90,cy+10],200,340,fill=NAVY,width=10)
    d.ellipse([cx-90,cy-60,cx+90,cy+120],fill=NAVY); d.ellipse([cx-50,cy-20,cx+50,cy+80],fill=MAR)
    for r in (150,190): d.arc([cx-r,cy-r+30,cx+r,cy+r+30],-40,40,fill=PINK,width=8); d.arc([cx-r,cy-r+30,cx+r,cy+r+30],140,220,fill=PINK,width=8)
def house(d,cx,cy):
    d.polygon([(cx,cy-150),(cx+170,cy-20),(cx-170,cy-20)],fill=MAR); d.rectangle([cx-130,cy-20,cx+130,cy+140],fill=NAVY)
    d.rectangle([cx-25,cy+50,cx+25,cy+140],fill=PINK); d.rectangle([cx-100,cy+10,cx-50,cy+60],fill=CREAM); d.rectangle([cx+50,cy+10,cx+100,cy+60],fill=CREAM)
    d.line([cx-220,cy+140,cx+220,cy+140],fill=NAVY,width=8)
def stairs(d,cx,cy):
    x0,y0=cx-220,cy+150
    for i in range(5): d.rectangle([x0+i*80,y0-(i+1)*60,x0+(i+1)*80+400-i*80- (400-80),y0],fill=NAVY) if False else d.rectangle([x0+i*80,y0-(i+1)*60,cx+220,y0-i*60],fill=NAVY)
    d.line([x0,y0-100,cx+220,y0-330],fill=MAR,width=14)
    d.rounded_rectangle([cx-40,cy-90,cx+40,cy-10],radius=12,fill=MAR); d.rectangle([cx-40,cy-140,cx-20,cy-60],fill=MAR)
def doc(d,cx,cy):
    d.rectangle([cx-120,cy-170,cx+120,cy+150],fill=CREAM,outline=NAVY,width=8)
    for i in range(5): d.line([cx-80,cy-110+i*45,cx+80 if i<4 else cx,cy-110+i*45],fill=NAVY,width=8)
    d.line([cx+40,cy+120,cx+190,cy-30],fill=MAR,width=22); d.polygon([(cx+40,cy+120),(cx+30,cy+150),(cx+58,cy+136)],fill=NAVY)
def cup(d,cx,cy):
    d.rounded_rectangle([cx-130,cy-80,cx+90,cy+120],radius=30,fill=NAVY); d.arc([cx+50,cy-40,cx+170,cy+80],-90,90,fill=NAVY,width=22)
    for k in (-60,0,60): d.arc([cx+k-25,cy-150,cx+k+25,cy-90],100,260,fill=MAR,width=8)
    d.ellipse([cx-200,cy+110,cx+200,cy+150],fill=PINK)
def bill(d,cx,cy):
    d.ellipse([cx-150,cy-150,cx+150,cy+150],fill=NAVY); d.ellipse([cx-115,cy-115,cx+115,cy+115],outline=PINK,width=8)
    from PIL import ImageFont
    d.text((cx,cy+5),"£",font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',170),fill=CREAM,anchor="mm")
    d.polygon([(cx+170,cy-40),(cx+250,cy-40),(cx+210,cy+30)],fill=MAR)
FUN=[alarm,house,stairs,doc,cup,bill]
import json
L=json.load(open('pins_layout.json'))
for i,f in enumerate(FUN,1):
    im=Image.open(f'pins/pin{i}.png'); d=ImageDraw.Draw(im)
    top=L[i-1]['_y']+30; frame(d,[80,top,920,1310]); f(d,500,(top+1310)//2+10); im.save(f'pins/pin{i}.png')
    print(i,top)
s=Image.new('RGB',(6*250,375),'white')
for i in range(6): s.paste(Image.open(f'pins/pin{i+1}.png').resize((250,375)),(i*250,0))
s.save('contact3.png')
