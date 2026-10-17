(() => {
  'use strict';
  const year=document.getElementById('year');if(year)year.textContent=new Date().getFullYear();
  const grid=document.getElementById('project-grid');if(!grid)return;
  const search=document.getElementById('search'),category=document.getElementById('category'),status=document.getElementById('status'),counter=document.getElementById('count');
  let projects=[];
  const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!=null)n.textContent=text;return n};
  const link=(text,url,primary)=>{const a=el('a',`btn${primary?' primary':''}`,text);a.href=url;if(/^https:\/\//.test(url)){a.target='_blank';a.rel='noopener noreferrer'}return a};
  function render(){const q=search.value.trim().toLowerCase(),cat=category.value,sd=status.value;const data=projects.filter(p=>(!q||[p.title,p.description,p.category,p.tags.join(' ')].join(' ').toLowerCase().includes(q))&&(!cat||p.category===cat)&&(!sd||(sd==='demo'?Boolean(p.demo_url):!p.demo_url)));
  grid.replaceChildren();counter.textContent=`Showing ${data.length} of ${projects.length} projects`;
  if(!data.length){grid.append(el('div','empty','No projects match these filters.'));return}
  for(const p of data){const box=el('article','card'),hd=el('div','card-head');hd.append(el('span','tag',p.category),el('span','status',p.status));box.append(hd);
  const h=el('h3');h.append(link(p.title,p.page_url,false));h.firstChild.className='';box.append(h,el('p','',p.description));
  const tags=el('div','chips');for(const t of p.tags.slice(0,3))tags.append(el('span','chip',t));box.append(tags);
  const act=el('div','actions');act.append(link('Project details ↗',p.page_url,true));if(p.demo_url)act.append(link('Use live app ↗',p.demo_url,false));if(p.repo_url)act.append(link('Source ↗',p.repo_url,false));box.append(act);grid.append(box)} }
  fetch('./projects.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('Catalogue unavailable');return r.json()}).then(items=>{
    if(!Array.isArray(items))throw Error('Invalid project catalogue');projects=items;
    for(const cat of [...new Set(items.map(x=>x.category))].sort()){const o=document.createElement('option');o.value=cat;o.textContent=cat;category.append(o)}
    [search,category,status].forEach(e=>e.addEventListener('input',render));render();
  }).catch(()=>{grid.replaceChildren(el('div','empty','The project catalogue could not be loaded. Check the Pages deployment workflow in GitHub Actions.'));counter.textContent='Catalogue unavailable'});
})();