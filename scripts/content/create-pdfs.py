from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from pathlib import Path
from reportlab.lib.utils import ImageReader
import subprocess,shutil
out=Path('public/files');out.mkdir(exist_ok=True)
W,H=A4
navy=HexColor('#173a56');blue=HexColor('#2262cc')
def page(c,title,sub,n):
 c.setFillColor(HexColor('#fffdf8'));c.rect(0,0,W,H,fill=1,stroke=0)
 c.setFillColor(HexColor('#fff0c9'));c.roundRect(24,718,W-48,100,16,fill=1,stroke=0)
 c.setFillColor(HexColor('#6d43b8'));c.setFont('Helvetica-Bold',11);c.drawString(40,794,'LITTLE PLAY LAB')
 c.setFont('Helvetica-Bold',25);c.drawString(40,750,title)
 c.setFont('Helvetica',10);c.drawString(40,730,sub)
 c.setFillColor(HexColor('#ef7b8c'));c.roundRect(40,657,W-80,35,10,fill=1,stroke=0)
 c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica-Bold',10);c.drawString(54,671,'My name: _______________________   Date: ______________')
 c.setFillColor(HexColor('#6946db'));c.roundRect(24,15,W-48,25,8,fill=1,stroke=0)
 c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica',9);c.drawString(40,24,f'Print A4 at 100% | Grown-up support where needed | Page {n}')
 art=Path('public/art/flower-pink.png')
 if art.exists():c.drawImage(str(art),W-94,770,42,42,mask='auto',preserveAspectRatio=True,anchor='c')
 c.setFillColor(navy)
def text(c,x,y,t,size=14,bold=False):c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,t)
def lines(c,y,count=3):
 c.setStrokeColor(HexColor('#b4bbc4'))
 for i in range(count):c.line(40,y-i*42,W-40,y-i*42)
def box(c,x,y,w,h):
 c.setStrokeColor(HexColor('#c8afe9'));c.setFillColor(HexColor('#faf5ff'));c.roundRect(x,y,w,h,8,fill=1);c.setFillColor(navy)
titles={'alphabet':'My alphabet adventure','numbers':'Count, spot & play','nature':'Little nature detectives','feelings':'Big feelings, little journal','puzzles':'The puzzle playground','shop':'My pretend play shop'}
for key,title in titles.items():
 c=canvas.Canvas(str(out/(key+'.pdf')),pagesize=A4);c.setTitle(title)
 if key=='alphabet':
  page(c,'Trace & try','Ages 3-5 | Say each letter, trace it, then write your own.',1)
  for i,a in enumerate(['A a','B b','C c','D d','E e']):
   y=610-i*95;text(c,42,y,a,40,True);c.setFillColor(HexColor('#c5aadf'));text(c,180,y,a+'    '+a,36);c.setFillColor(navy);c.line(180,y-14,540,y-14)
  c.showPage();page(c,'Listen to the first sound','Say each word. Circle its beginning letter.',2)
  for i,(word,choices) in enumerate([('apple','A   B   C'),('ball','C   A   B'),('cat','B   C   D'),('dog','D   E   A'),('egg','B   E   D')]):
   y=610-i*83;text(c,50,y,word,26,True);c.setFillColor(HexColor('#6946db'));text(c,300,y,choices,26);c.setFillColor(navy)
  text(c,40,145,'Draw something that begins with A.');box(c,40,55,510,75)
  c.showPage();page(c,'Alphabet hunt','Find things at home. Draw or write one for each letter.',3)
  for i,a in enumerate(['A','B','C','D']):x=40+(i%2)*264;y=405-(i//2)*220;box(c,x,y,245,200);text(c,x+15,y+165,a,28,True)
  text(c,40,150,'Grown-up guide: accept sounds, drawings and spoken answers.',11);text(c,40,126,'Sound match answers: apple A, ball B, cat C, dog D, egg E.',11)
  for j,a in enumerate(['bunny','fox','bear','butterfly']):
   art=Path('public/art/'+a+'.png')
   if art.exists():c.drawImage(str(art),60+j*120,48,70,70,mask='auto',preserveAspectRatio=True)
 elif key=='numbers':
  page(c,'Count the flowers','Ages 4-6 | Count each group and write its number.',1)
  for i,n in enumerate([2,4,6,8,10]):
   y=605-i*96
   for j in range(n):
    art=Path('public/art/flower-yellow.png')
    if art.exists():c.drawImage(str(art),45+(j%5)*46,y-15-(j//5)*35,30,34,mask='auto')
    else:c.circle(60+(j%5)*35,y-(j//5)*30,8,fill=0)
   box(c,380,y-26,105,52)
  c.showPage();page(c,'Number writing','Trace each number. Write it twice on the line.',2)
  for i,n in enumerate(range(1,7)):
   y=610-i*80;text(c,50,y,str(n),34,True);c.setFillColor(HexColor('#c5aadf'));text(c,150,y,f'{n}      {n}',34);c.setFillColor(navy);c.line(320,y-10,535,y-10)
  c.showPage();page(c,'Number bingo','Two players | A grown-up calls numbers 1-9 in any order.',3)
  text(c,40,640,'Cover a number when it is called. Three in a row wins!',12)
  for board,nums in enumerate([[1,6,3,8,2,5,4,9,7],[4,2,8,1,7,9,6,3,5]]):
   y0=380 if board==0 else 95;text(c,40,y0+235,'Board '+str(board+1),16,True)
   for i,n in enumerate(nums):x=40+(i%3)*72;y=y0+(2-i//3)*72;box(c,x,y,72,72);text(c,x+28,y+25,str(n),24)
  text(c,300,540,'How to play',18,True);text(c,300,505,'Use buttons or paper counters.',11);text(c,300,480,'Swap who calls each round.',11);text(c,300,455,'Counting answers: 2, 4, 6, 8, 10.',11)
 elif key=='nature':
  page(c,'Outdoor scavenger hunt','Ages 5-8 | Explore with a grown-up. Look; leave living things alone.',1)
  for i,t in enumerate(['A leaf with a bumpy edge','Something yellow','A bird or a bird sound','A small stone','A shadow','Something that smells nice']):
   y=610-i*72;box(c,42,y-6,24,24);text(c,83,y,t,15)
   art=Path('public/art/'+['bunny','flower-yellow','butterfly','fox','bear','flower-pink'][i]+'.png')
   if art.exists():c.drawImage(str(art),460,y-20,56,56,mask='auto',preserveAspectRatio=True)
  text(c,40,130,'My favourite find was:');lines(c,105,1);text(c,40,55,'Wash hands after exploring. Do not taste plants or berries.',11)
  c.showPage();page(c,'My nature notebook','Choose one thing to observe. Draw it in the frame.',2);box(c,40,365,510,285);text(c,40,330,'I noticed these colours:');lines(c,300,1);text(c,40,250,'It feels or looks like:');lines(c,220,1);text(c,40,170,'I wonder:');lines(c,140,2)
  c.showPage();page(c,'Colour the garden friends','Give every flower and animal your favourite colours.',3)
  art=Path('public/art/colouring-garden.png')
  if art.exists():c.drawImage(str(art),40,88,510,555,preserveAspectRatio=True,anchor='c',mask='auto')
  text(c,40,60,'Can you spot the bunny, fox and butterfly? Tell a grown-up.',12)
  c.showPage();page(c,'Garden animal memory game','Cut with a grown-up. Turn cards face down and find the pairs.',4)
  for i,a in enumerate(['bunny','fox','bear','butterfly']*2):
   x=40+(i%4)*128;y=397-(i//4)*208
   c.setFillColor(HexColor(['#ffe3b7','#ffd7e3','#dfd0ff','#c8ecdd'][i%4]));c.setStrokeColor(HexColor('#b5a0cc'));c.roundRect(x,y,115,182,13,fill=1)
   art=Path('public/art/'+a+'.png')
   if art.exists():c.drawImage(str(art),x+10,y+35,95,132,mask='auto',preserveAspectRatio=True,anchor='c')
   c.setFillColor(navy);text(c,x+18,y+15,a.upper(),11,True)
  text(c,40,137,'How to play',15,True);text(c,40,110,'Take turns turning over two cards. A match? Keep the pair!',12)
  text(c,40,88,'No match? Turn them back over. Remember where your friends hide.',12)


 elif key=='feelings':
  page(c,'How do I feel today?','Ages 5-8 | All feelings are welcome. Share with a trusted grown-up.',1);text(c,40,630,'Circle a word, or add your own.',16)
  for i,t in enumerate(['Happy','Sad','Worried','Excited','Angry','Calm']):x=40+(i%2)*260;y=540-(i//2)*72;c.setFillColor(HexColor(['#ffe598','#c8e8ff','#e4d6ff','#ffcfda','#ffd6b7','#c5ecda'][i]));c.setStrokeColor(HexColor('#c8afe9'));c.roundRect(x,y,245,55,10,fill=1);c.setFillColor(navy);text(c,x+18,y+18,t,21)
  text(c,40,340,'Draw your feeling as weather. Is it sunny, stormy or something else?');box(c,40,110,510,205)
  c.showPage();page(c,'My calm-down toolkit','Try one idea with a grown-up. Pick what helps you.',2)
  for i,t in enumerate(['Take five slow breaths.','Ask for a hug or some quiet space.','Stretch your arms and shoulders.','Draw how you feel.','Tell a trusted grown-up what you need.']):text(c,45,610-i*62,str(i+1)+'. '+t,16)
  text(c,40,245,'What helped me today?');lines(c,215,3)
  c.showPage();page(c,'A little kindness journal','Small kind moments count.',3)
  for i,t in enumerate(['Someone was kind to me when...','I was kind when...','Tomorrow I could...']):y=620-i*175;text(c,40,y,t,18,True);lines(c,y-35,3)
 elif key=='puzzles':
  page(c,'Word search explorers','Ages 6-10 | Find the five words. They go across or down.',1)
  grid=['PLANTQRT','GXPLAYOB','ASUNBCDO','MLEAFGHO','EFLOWERS','KLMNOPQT','UVWXYZAB','CDEFGHIJ']
  for i,row in enumerate(grid):
   for j,l in enumerate(row):x=90+j*48;y=570-i*48;c.setFillColor(HexColor('#fff1c9' if (i+j)%2==0 else '#e4f4ec'));c.setStrokeColor(HexColor('#b8d5c8'));c.roundRect(x,y,48,48,6,fill=1);c.setFillColor(navy);text(c,x+16,y+14,l,23)
  text(c,40,130,'Find: PLANT, PLAY, SUN, FLOWER, GAME',16,True)
  c.showPage();page(c,'Crack the secret code','Use A=1, B=2, C=3 ... Z=26 to decode the messages.',2)
  for i,(code,answer) in enumerate([('16 - 12 - 1 - 25','PLAY'),('2 - 5   11 - 9 - 14 - 4','BE KIND'),('5 - 24 - 16 - 12 - 15 - 18 - 5','EXPLORE')]):y=595-i*140;text(c,40,y,code,22,True);lines(c,y-45,1)
  text(c,40,155,'Create a secret word for a friend to solve.');lines(c,120,2)
  c.showPage();page(c,'Number detective','Solve each clue. Check the answers with a grown-up.',3)
  for i,t in enumerate(['I am 3 more than 7. What number am I?','Double me and you get 12. What number am I?','Continue the pattern: 2, 4, 6, __, __.','You have 15 buttons. Give away 4. How many remain?']):y=615-i*100;text(c,40,y,t,14);lines(c,y-40,1)
  text(c,40,190,'Answer guide',16,True);text(c,40,162,'Numbers: 10; 6; 8 and 10; 11.',12);text(c,40,137,'Code: PLAY; BE KIND; EXPLORE.',12);text(c,40,112,'Word search: PLANT row 1, PLAY row 2, SUN row 3,',11);text(c,40,94,'FLOWER row 5; GAME column 1, rows 2-5.',11)
 elif key=='shop':
  page(c,'Welcome to my shop','Ages 5-8 | Use pretend items and play money only.',1);text(c,40,630,'My shop is called:');box(c,40,405,510,195);text(c,40,375,'Draw your shop sign in the box.');text(c,40,315,'I will sell:');lines(c,280,4)
  c.showPage();page(c,'Price tags & play money','Cut with grown-up help. Prices are in rupees.',2)
  for i,n in enumerate([5,10,15,20,25,30]):x=40+(i%3)*175;y=520-(i//3)*95;c.setFillColor(HexColor(['#ffe0ec','#e5d9ff','#d6f1e3'][i%3]));c.setStrokeColor(HexColor('#ad90cc'));c.roundRect(x,y,155,70,10,fill=1);c.setFillColor(navy);text(c,x+20,y+28,'Rs '+str(n),24,True)
  text(c,40,385,'PLAY MONEY - NOT REAL CURRENCY',14,True)
  for i,n in enumerate([5,5,10,10,20,20]):x=40+(i%2)*265;y=265-(i//2)*82;box(c,x,y,245,66);text(c,x+15,y+32,'Rs '+str(n),20,True);text(c,x+15,y+12,'PRETEND PLAY ONLY',10)
  c.showPage();page(c,'My shopping list','Take turns as shopkeeper and customer.',3)
  text(c,40,625,'Item',18,True);text(c,290,625,'Price',18,True);text(c,420,625,'Quantity',18,True)
  for i in range(4):y=575-i*65;c.line(40,y,550,y)
  text(c,40,295,'My total: Rs __________________');text(c,40,240,'I paid: Rs ____________________');text(c,40,185,'My change: Rs ________________');text(c,40,110,'Challenge: buy two things for less than Rs 30.',14)
 c.save()
 subprocess.run(['pdftoppm','-f','1','-singlefile','-scale-to','900','-png',str(out/(key+'.pdf')),'public/previews/'+key],check=True,stdout=subprocess.DEVNULL)
# Protected PDFs ship outside public asset paths.
Path('private-pdfs').mkdir(exist_ok=True)
for f in out.glob('*.pdf'):shutil.move(str(f),'private-pdfs/'+f.name)
out.rmdir()
