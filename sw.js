'use strict';
const PREFIX = 'world-picker:' + self.registration.scope + ':';
const CACHE = PREFIX + '__BUILD_VERSION__';
const ROOT = new URL('./', self.registration.scope);
const HOME = new URL('index.html', ROOT).href;
const ASSETS = ['index.html','manifest.webmanifest','icons/icon-192.png','icons/icon-512.png','icons/icon-180.png'].map(path => new URL(path, ROOT).href);
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await cache.addAll(ASSETS.map(url => new Request(url, {cache:'reload'})));
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) {
      if (key.startsWith(PREFIX) && key !== CACHE) await caches.delete(key);
    }
    await self.clients.claim();
  })());
});
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== 'GET' || !url.href.startsWith(ROOT.href)) return;
  if (request.mode === 'navigate' && (url.pathname === ROOT.pathname || url.pathname === new URL(HOME).pathname)) {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE);
      try {
        const response = await fetch(request);
        if (response.ok) await cache.put(HOME, response.clone());
        return response;
      } catch (error) {
        return await cache.match(HOME) || Response.error();
      }
    })());
  } else if (ASSETS.includes(url.href)) {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE);
      return await cache.match(request) || fetch(request);
    })());
  }
});
