#!/usr/bin/env python3
"""使い方: python3 _tools/build.py <key> <元のHTML>   (key は games.json の名前)
元のHTMLから <dir>/index.html, sw.js, manifest.webmanifest, アイコンを作る。"""
import json,re,sys,os,hashlib
T=os.path.dirname(os.path.abspath(__file__));R=os.path.dirname(T)
G=json.load(open(T+'/games.json',encoding='utf-8'))
SK=re.compile(r'^\s*<!doctype html><html><head><meta charset=utf8><meta name=viewport[^>]*><style>.*?</style></head><body>',re.S|re.I)
RESET=(':root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
 'html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000}'
 'img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}')
REG=("<script>if('serviceWorker' in navigator&&(location.protocol==='https:'||location.hostname==='localhost')){"
 "addEventListener('load',()=>{navigator.serviceWorker.register('sw.js').catch(()=>{})})}</script>")
def icons(g,d):
  from PIL import Image,ImageDraw,ImageFont
  fp='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
  for n,sz in (('icon-512.png',512),('icon-192.png',192),('apple-touch-icon.png',180)):
    p=os.path.join(d,n)
    if os.path.exists(p):continue
    im=Image.new('RGB',(sz,sz),g['bg']);dr=ImageDraw.Draw(im);f=None
    for i in range(10):
      try:
        t=ImageFont.truetype(fp,int(sz*.66),index=i)
        if 'JP' in t.getname()[0]:f=t;break
      except Exception:break
    f=f or ImageFont.truetype(fp,int(sz*.66))
    x0,y0,x1,y1=dr.textbbox((0,0),g['ch'],font=f)
    dr.text(((sz-(x1-x0))/2-x0,(sz-(y1-y0))/2-y0),g['ch'],font=f,fill=g['fg'])
    im.save(p)
def build(key,src):
  g=G[key];d=os.path.normpath(os.path.join(R,g['dir']));os.makedirs(d,exist_ok=True)
  c=open(src,encoding='utf-8').read().replace('\r\n','\n')
  m=SK.match(c)
  if m:c=re.sub(r'</body></html>\s*$','',c[m.end():])
  c=c.strip('\n')
  pwa=('<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
   f'<meta name="apple-mobile-web-app-status-bar-style" content="{g["status"]}"><meta name="apple-mobile-web-app-title" content="{g["name"]}">'
   f'<meta name="theme-color" content="{g["bg"]}"><link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="apple-touch-icon.png">')
  if re.match(r'\s*<!doctype',c,re.I) and re.search(r'</head>',c,re.I):
    c=re.sub(r'</head>',lambda _:pwa+'</head>',c,count=1,flags=re.I)
    i=c.lower().rfind('</body>')
    if i<0:i=c.lower().rfind('</html>')
    out=(c[:i]+REG+c[i:] if i>=0 else c+REG)+'\n'
  else:
    out=('<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'
     f'<style>{RESET}</style>{pwa}</head><body>\n{c}\n{REG}</body></html>\n')
  man=json.dumps({"name":g['name'],"short_name":g['name'],"start_url":"./","scope":"./","display":"standalone",
   "background_color":g['bg'],"theme_color":g['bg'],"lang":"ja",
   "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"}]},ensure_ascii=False,indent=1)
  h=hashlib.sha1((out+man).encode()).hexdigest()[:10]
  sw=open(T+'/sw.tpl.js',encoding='utf-8').read().replace('%C%',f'{key}-{h}').replace('%P%',key)
  for n,t in (('index.html',out),('manifest.webmanifest',man),('sw.js',sw)):
    open(os.path.join(d,n),'w',encoding='utf-8').write(t)
  icons(g,d)
  print(key,'built',h,len(out))
if __name__=='__main__':build(sys.argv[1],sys.argv[2])
