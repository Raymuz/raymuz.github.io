#!/usr/bin/env python3
"""Opt-in public repo discovery: never publishes arbitrary repositories or private Spaces.

A GitHub repo must explicitly contain portfolio.json and name an owner-matching Space.
Existing curated pages can be updated; new ones get a generated project page.
Any network/API failure exits nonzero, avoiding silently removing existing links.
"""
import json, os, re, sys, urllib.request
from pathlib import Path
from html import escape
from urllib.parse import quote, urlsplit
from update_deployment import ROOT
OWNER='raymuz'; HF_OWNER='raymuz'
API='https://api.github.com'; HF_API='https://huggingface.co/api'
SLUG=re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

def get_json(url):
    headers={'Accept':'application/vnd.github+json','User-Agent':'adamou-portfolio-discovery'}
    key=os.environ.get('GH_DISCOVERY_TOKEN','')
    if key:headers['Authorization']='Bearer '+key
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=18) as response:
        return json.load(response)

def repo_list(fetch=get_json):
    repos=[]
    for page in range(1,6):
        batch=fetch(f'{API}/users/{OWNER}/repos?per_page=100&page={page}&type=owner')
        if not isinstance(batch,list):raise ValueError('GitHub API returned unexpected repository list')
        repos.extend(batch)
        if len(batch)<100:break
    return repos

def get_manifest(repo,fetch=get_json):
    from base64 import b64decode
    name=repo['name']; branch=repo.get('default_branch','main')
    # raw GitHub response is intentionally restricted to the owner's declared branch
    try:
        data=fetch(f'{API}/repos/{OWNER}/{quote(name)}/contents/portfolio.json?ref={quote(branch)}')
    except Exception as exc:
        # Only a 404 means a repo has not opted in; all other errors are surfaced.
        from urllib.error import HTTPError
        if isinstance(exc,HTTPError) and exc.code==404:return None
        raise
    if data.get('encoding')!='base64':raise ValueError('Manifest encoding unsupported')
    raw=b64decode(data['content']).decode('utf8')
    if len(raw)>12000:raise ValueError('Manifest too long')
    return json.loads(raw)

def normalize(repo,manifest,fetch=get_json):
    if not isinstance(manifest,dict) or manifest.get('portfolio') is not True:return None
    slug=manifest.get('slug','')
    if not isinstance(slug,str) or not SLUG.fullmatch(slug):raise ValueError('Invalid project slug')
    space=manifest.get('hf_space','')
    if not isinstance(space,str) or not re.fullmatch(r'raymuz/[A-Za-z0-9_.-]+',space):raise ValueError('Space owner must be raymuz')
    title=manifest.get('title',''); desc=manifest.get('description','')
    if not isinstance(title,str) or not title.strip() or len(title)>110:raise ValueError('Invalid title')
    if not isinstance(desc,str) or not desc.strip() or len(desc)>400:raise ValueError('Invalid description')
    state=fetch(f'{HF_API}/spaces/{quote(space,safe="/")}')
    # Public API success means public metadata, not necessarily a working / embeddable frontend
    if state.get('private') or state.get('disabled') or state.get('gated'):return None
    if state.get('runtime',{}).get('stage')!='RUNNING':return None
    # Inference readiness: attempt the actual public root URL, not model API assumptions
    host=space.replace('/','-').replace('_','-').lower()+'.hf.space'
    import urllib.error
    try:
        with urllib.request.urlopen(urllib.request.Request('https://'+host+'/',headers={'User-Agent':'Portfolio-health-check'}),timeout=15) as r:
            if r.status!=200:return None
    except (urllib.error.URLError,TimeoutError):return None
    return dict(slug=slug,title=title.strip(),description=desc.strip(),category=str(manifest.get('category','AI Applications'))[:70],tags=manifest.get('tags',[])[:8],repo='https://github.com/'+repo['full_name'],live='https://huggingface.co/spaces/'+space,embed='https://'+host,space=space)

def metadata(page, info):
    html=page.read_text('utf8')
    for k,v in [('repo',info['repo']),('live',info['live']),('embed',info['embed']),('status','Live demo'),('description',info['description'])]:
        pattern=r'(<meta\s+name=["\']portfolio:'+k+r'["\']\s+content=["\'])[^"\']*(["\'])'
        html,n=re.subn(pattern,lambda m:m.group(1)+escape(v,quote=True)+m.group(2),html,count=1)
        if not n:raise ValueError(f'Missing metadata field {k} on {page}')
    page.write_text(html,'utf8')

def new_page(info):
    title=escape(info['title']);desc=escape(info['description'])
    def meta(k,v):return f'<meta name="portfolio:{k}" content="{escape(str(v),quote=True)}">'
    tags=info['tags'] if isinstance(info['tags'],list) else []
    tags=', '.join(str(x)[:40] for x in tags)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | Dr. Adamou Musa</title><meta name="description" content="{desc}">
"""+''.join(meta(k,v) for k,v in [('title',info['title']),('description',info['description']),('category',info['category']),('status','Live demo'),('tags',tags),('repo',info['repo']),('live',info['live']),('embed',info['embed'])])+f"""<link rel="stylesheet" href="../../assets/style.css"></head><body><header class="topbar"><div class="wrap nav"><a class="brand" href="../../">DR. ADAMOU MUSA / PORTFOLIO</a><nav class="links"><a href="../../#projects">All projects</a></nav></div></header><main><section class="project-head"><div class="wrap"><div class="eyebrow">AI Application · Live demo</div><h1>{title}</h1><p class="lede">{desc}</p><div class="actions"><a id="external-demo" class="btn primary hide" rel="noopener noreferrer" target="_blank">Open live application</a><a id="external-repo" class="btn hide" rel="noopener noreferrer" target="_blank">View source</a></div></div></section><section class="section"><div class="wrap"><h2>Interactive application</h2><p id="demo-intro">Connect to the live application.</p><div id="embedded-demo" class="demo">Live app link awaiting build.</div><p><small>The application runs on Hugging Face, not on GitHub Pages. Public embedding depends on the app's own policies.</small></p><span id="repo-state" hidden></span><span id="demo-state" hidden></span></div></section></main><script src="../../assets/project.js" defer></script></body></html>"""

def sync(repos,fetch=get_json,get_manifest_fn=None,normalizer=None):
    get_manifest_fn=get_manifest_fn or (lambda r:get_manifest(r,fetch))
    normalizer=normalizer or (lambda r,m:normalize(r,m,fetch))
    changed=[]
    for repo in repos:
        if repo.get('fork') or repo.get('private') or repo.get('archived') or repo.get('owner',{}).get('login','').lower()!=OWNER:continue
        manifest=get_manifest_fn(repo)
        if manifest is None:continue
        info=normalizer(repo,manifest)
        if info is None:continue
        page=ROOT/'projects'/info['slug']/'index.html'
        if page.exists():
            prior=page.read_bytes();metadata(page,info)
            if page.read_bytes()!=prior:changed.append(info['slug'])
        else:
            page.parent.mkdir(parents=True,exist_ok=True)
            page.write_text(new_page(info),'utf8');changed.append(info['slug'])
    print(f'Public app discovery: {len(changed)} project page(s) added/updated: {changed}')
    return changed

if __name__=='__main__':sync(repo_list())
