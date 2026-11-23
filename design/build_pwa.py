"""Builds the standalone iPhone home-screen app (PWA) from index.html into ./pwa

The same index.html runs as the claude.ai artifact; this wraps it in a full document with
the iOS home-screen metadata, a web manifest and an offline service worker."""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'index.html')).read()
cut = src.index('<div class="haze"')
head, body = src[:cut], src[cut:]
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')

GSAP = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js'
assert GSAP in body, 'GSAP script tag missing from index.html'

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Dil Se">
<meta name="application-name" content="Dil Se">
<meta name="format-detection" content="telephone=no">
<meta name="description" content="Learn Hindi for the one you love: lessons, stories, conversations and spaced repetition.">
<meta name="theme-color" content="#F7F5FB" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#15102E" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="icons/icon-32.png">
<style>:root{{color-scheme:light dark;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<script>window.__PWA=true;</script>
{head.strip()}
</head>
<body>
{body.strip()}
<script>if("serviceWorker" in navigator) addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{{}}));</script>
</body>
</html>
'''
out = os.path.join(here, 'pwa')
os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'index.html'), 'w').write(page)

manifest = {
    "id": "./", "name": "Dil Se Hindi", "short_name": "Dil Se",
    "description": "Learn Hindi for the one you love.",
    "start_url": "./", "scope": "./", "display": "standalone", "orientation": "portrait",
    "background_color": "#15102E", "theme_color": "#15102E", "lang": "en",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icons/maskable-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
        {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
json.dump(manifest, open(os.path.join(out, 'manifest.webmanifest'), 'w'), indent=1, ensure_ascii=False)

open(os.path.join(out, 'sw.js'), 'w').write('''// Offline support for Dil Se.
// The page is fetched fresh when online (so updates arrive at once) and falls back to the cached copy offline.
// Everything else (icons, GSAP, fonts) is served from cache first and refreshed in the background.
const C="dilse-v3";
const SHELL=["./","index.html","manifest.webmanifest","icons/apple-touch-icon.png","icons/icon-192.png","icons/icon-512.png","icons/icon-32.png"];
const EXTRA=["''' + GSAP + '''"];
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
''')
print("built", os.path.join(out, 'index.html'), len(page), "bytes")
