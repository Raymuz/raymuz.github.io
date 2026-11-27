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
  for(const p of data){
    const details=el('details','project-entry');
    const summary=el('summary','project-summary');
    const info=el('span','project-heading');
    info.append(el('span','project-category',p.category),el('strong','',p.title));
    const right=el('span','project-right');
    right.append(el('span','project-status',p.status),el('span','entry-plus','+'));
    summary.append(info,right);
    const body=el('div','project-body');body.append(el('p','',p.description));
    const tags=el('div','chips');for(const t of p.tags.slice(0,5))tags.append(el('span','chip',t));body.append(tags);
    const act=el('div','actions');act.append(link('Read full case study ↗',p.page_url,true));
    if(p.demo_url)act.append(link('Launch application ↗',p.demo_url,false));
    if(p.repo_url)act.append(link('View source ↗',p.repo_url,false));
    body.append(act);details.append(summary,body);grid.append(details);
  }
  }
  fetch('./projects.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('Catalogue unavailable');return r.json()}).then(items=>{
    if(!Array.isArray(items))throw Error('Invalid project catalogue');projects=items;
    for(const cat of [...new Set(items.map(x=>x.category))].sort()){const o=document.createElement('option');o.value=cat;o.textContent=cat;category.append(o)}
    [search,category,status].forEach(e=>e.addEventListener('input',render));render();
  }).catch(()=>{grid.replaceChildren(el('div','empty','The project catalogue could not be loaded. Check the Pages deployment workflow in GitHub Actions.'));counter.textContent='Catalogue unavailable'});
})();

/* Published AHFE research and Google Scholar links. Additive, idempotent homepage enhancement. */
(() => {
  'use strict';
  const scholar='https://scholar.google.com/citations?user=bejW4rMAAAAJ&hl=en';
  const paper='./articles/threshold-based-multicloud-key-management/';
  const doi='https://doi.org/10.54941/ahfe1008425';
  const addLink=(parent,text,href,external=false)=>{
    const a=document.createElement('a');a.href=href;a.textContent=text;
    if(external){a.target='_blank';a.rel='noopener noreferrer'}
    parent.append(a);return a;
  };
  const style=document.createElement('style');
  style.id='published-research-scholar-styles';
  style.textContent=`
    .published-research-feature{background:linear-gradient(125deg,#132945,#174969);color:#fff;border:1px solid #3b7992;border-radius:18px;padding:24px;margin:12px 0 24px;box-shadow:0 12px 35px rgba(5,20,38,.16)}
    .published-research-feature h3{margin:7px 0 10px;color:#fff;font-size:clamp(1.15rem,2.1vw,1.5rem);line-height:1.35}
    .published-research-feature p{color:#dbeaf7;max-width:880px}
    .published-research-feature .research-overline{color:#9be9e0;font-size:.77rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase}
    .published-research-feature .research-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:17px}
    .published-research-feature .research-actions a{display:inline-flex;align-items:center;border:1px solid #a6c5da;border-radius:9px;padding:9px 13px;color:#fff;text-decoration:none;font-weight:700;font-size:.9rem}
    .published-research-feature .research-actions a:first-child{background:#eff8fd;color:#102b48;border-color:#eff8fd}
    .scholar-profile-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 18px}
    .scholar-profile-row a{padding:9px 14px;border-radius:9px;background:#e8f5fc;color:#10466e;font-weight:800;text-decoration:none}
    .mega-col .scholar-mega-link{font-weight:800!important}
  `;
  if(!document.getElementById(style.id))document.head.append(style);
  const megacol=[...document.querySelectorAll('.mega-col')].find(x=>x.textContent.includes('RESEARCH & PROJECT LIBRARY'));
  if(megacol && !megacol.querySelector('.scholar-mega-link')){
    const link=addLink(megacol,'Published research: multi-cloud key management ↗',paper);
    link.className='scholar-mega-link';
    const profile=addLink(megacol,'Google Scholar profile ↗',scholar,true);
    profile.className='scholar-mega-link';
  }
  const section=document.querySelector('#articles .accordion-content');
  if(section && !section.querySelector('#ahfe-published-paper-feature')){
    const card=document.createElement('div');card.id='ahfe-published-paper-feature';card.className='published-research-feature';
    const overline=document.createElement('div');overline.className='research-overline';overline.textContent='Published open-access conference research · AHFE';card.append(overline);
    const title=document.createElement('h3');title.textContent='Threshold-Based Key Management Across Heterogeneous Multi-Cloud Key Management Systems';card.append(title);
    const author=document.createElement('p');author.textContent='Musa Adamou · Ivan Nkwawir · Amir Schur';card.append(author);
    const desc=document.createElement('p');desc.textContent='Benzene Ring Secure Cross-Cloud System (BRSCCS): a threshold-based architecture for distributed cryptographic trust across heterogeneous cloud key management services, with a 2-of-3 key-share policy.';card.append(desc);
    const actions=document.createElement('div');actions.className='research-actions';
    addLink(actions,'Read publication ↗',paper);
    addLink(actions,'Publisher DOI ↗',doi,true);
    addLink(actions,'Google Scholar ↗',scholar,true);
    card.append(actions);section.prepend(card);
  }
  const research=document.querySelector('#research .accordion-content');
  if(research && !research.querySelector('.scholar-profile-row')){
    const row=document.createElement('div');row.className='scholar-profile-row';
    addLink(row,'Published AHFE research ↗',paper);
    addLink(row,'Google Scholar profile ↗',scholar,true);
    research.prepend(row);
  }
})();
