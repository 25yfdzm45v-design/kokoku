const C='kokoku-e8877b0a84',P='kokoku-',FC='gfonts',F=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','apple-touch-icon.png'];
const S=new URL('./',self.location).href,SP=new URL(S).pathname,IDX=S+'index.html';
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(F)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith(P)&&k!==C).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
 if(u.hostname==='fonts.googleapis.com'||u.hostname==='fonts.gstatic.com'){e.respondWith(caches.open(FC).then(c=>c.match(r).then(x=>x||fetch(r).then(y=>{if(y.ok||y.type==='opaque')c.put(r,y.clone());return y}))));return}
 if(u.origin!==location.origin||!u.pathname.startsWith(SP))return;const rel=u.pathname.slice(SP.length);if(rel.includes('/'))return;
 if(r.mode==='navigate'){if(rel!==''&&rel!=='index.html')return;
  e.respondWith((async()=>{const net=fetch(r).then(x=>{if(x.ok){const y=x.clone();caches.open(C).then(c=>c.put(IDX,y))}return x});
   const x=await Promise.race([net.catch(()=>null),new Promise(s=>setTimeout(()=>s(null),4000))]);if(x)return x;
   return (await caches.match(IDX))||net})());return}
 e.respondWith(caches.match(r,{ignoreSearch:true}).then(x=>x||fetch(r)))});
