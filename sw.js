// Offline support for Dil Se.
// The page is fetched fresh when online (so updates arrive at once) and falls back to the cached copy offline.
// Everything else (icons, GSAP, fonts) is served from cache first and refreshed in the background.
const C="dilse-v3";
const SHELL=["./","index.html","manifest.webmanifest","icons/apple-touch-icon.png","icons/icon-192.png","icons/icon-512.png","icons/icon-32.png"];
const EXTRA=["https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"];
self.addEventListener("install",e=>{ e.waitUntil(caches.open(C).then(c=>c.addAll(SHELL).then(()=>Promise.all(EXTRA.map(u=>c.add(new Request(u,{mode:"cors"})).catch(()=>{}))))));
  self.skipWaiting(); });
self.addEventListener("activate",e=>{ e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k))))); self.clients.claim(); });
self.addEventListener("fetch",e=>{
  const r=e.request; if(r.method!=="GET") return;
  if(r.mode==="navigate"){
    e.respondWith(fetch(r).then(res=>{ const cp=res.clone(); caches.open(C).then(c=>c.put("index.html",cp)); return res; })
      .catch(()=>caches.match("index.html").then(h=>h||caches.match("./"))));
    return;
  }
  e.respondWith(caches.match(r).then(hit=>{
    const net=fetch(r).then(res=>{ if(res && (res.ok||res.type==="opaque")){ const cp=res.clone(); caches.open(C).then(c=>c.put(r,cp)); } return res; }).catch(()=>hit);
    return hit||net;
  }));
});
