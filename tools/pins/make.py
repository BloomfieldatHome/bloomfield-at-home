from PIL import Image, ImageDraw, ImageFont
import textwrap, json
TEAL=(29,43,58); CREAM=(250,247,242); INK=(29,43,58); ACC=(124,45,55); WHITE=(255,255,255)
SB='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'; S='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F=lambda p,s: ImageFont.truetype(p,s)
# Logo 800x800
im=Image.new('RGB',(800,800),TEAL); d=ImageDraw.Draw(im)
# simple house outline
d.polygon([(400,170),(590,330),(210,330)],outline=CREAM,width=0,fill=CREAM)
d.rectangle([250,330,550,520],fill=CREAM)
d.rectangle([370,410,430,520],fill=TEAL)
d.text((400,600),"Bloomfield",font=F(SB,72),fill=CREAM,anchor="mm")
d.text((400,680),"at Home",font=F(SB,60),fill=(232,196,200),anchor="mm")
im.save('logo.png')
pins=json.load(open('pins.json'))
for i,p in enumerate(pins,1):
    im=Image.new('RGB',(1000,1500),CREAM); d=ImageDraw.Draw(im)
    d.rectangle([0,0,1000,360],fill=TEAL)
    d.text((80,120),p['kicker'].upper(),font=F(S,34),fill=(232,196,200))
    d.text((80,200),"FREE PLAIN-ENGLISH GUIDE",font=F(S,30),fill=CREAM)
    y=440
    for line in textwrap.wrap(p['headline'],19):
        d.text((80,y),line,font=F(SB,76),fill=INK); y+=92
    y+=30; d.rectangle([80,y,200,y+8],fill=ACC); y+=50
    for line in textwrap.wrap(p['sub'],40):
        d.text((80,y),line,font=F(S,36),fill=INK); y+=50
    d.rectangle([0,1340,1000,1500],fill=TEAL)
    d.text((500,1420),"bloomfieldathome.com",font=F(SB,48),fill=CREAM,anchor="mm")
    p['_y']=y
    im.save(f'pins/pin{i}.png')
json.dump(pins,open('pins_layout.json','w'))
print('ok')
