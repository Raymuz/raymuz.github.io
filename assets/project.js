(() => { 'use strict';
  const m=name=>document.querySelector(`meta[name="portfolio:${name}"]`)?.content.trim()||'';
  const safe=(raw,kind)=>{try{const u=new URL(raw);if(u.protocol!=='https:')return '';
    if(kind==='embed'&&!(u.hostname.endsWith('.hf.space')))return '';
    return u.href;}catch{return ''}};
  const yr=document.getElementById('year');if(yr)yr.textContent=new Date().getFullYear();
  const live=safe(m('live'),'live'),repo=safe(m('repo'),'repo'),embed=safe(m('embed'),'embed');
  if(live){const btn=document.getElementById('external-demo');btn.href=live;btn.classList.remove('hide');document.getElementById('demo-state').textContent='Public link configured'}
  if(repo){const btn=document.getElementById('external-repo');btn.href=repo;btn.classList.remove('hide');document.getElementById('repo-state').textContent='Source repository linked'}
  if(embed){const div=document.getElementById('embedded-demo'),frame=document.createElement('iframe');frame.src=embed;frame.title=`Interactive demo for ${m('title')||'project'}`;frame.loading='lazy';frame.referrerPolicy='strict-origin-when-cross-origin';frame.allow='clipboard-read; clipboard-write';div.replaceChildren(frame);document.getElementById('demo-intro').textContent='Use the public application below. If the embed does not load, open it in a new tab using the live application link.';
    if(!live){const btn=document.getElementById('external-demo');btn.href=embed;btn.classList.remove('hide');document.getElementById('demo-state').textContent='Embed URL configured'}
  }
})();