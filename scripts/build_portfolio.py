#!/usr/bin/env python3
"""Discover projects/<slug>/index.html and build a standalone GitHub Pages artifact.
No third-party packages, no tokens. Actions runs this on every push.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json, argparse, shutil, sys, re

ROOT=Path(__file__).resolve().parents[1]
class MetaReader(HTMLParser):
    def __init__(self):super().__init__();self.meta={};self.title='';self.in_title=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='meta' and d.get('name','').startswith('portfolio:'):self.meta[d['name'][10:]]=d.get('content','').strip()
        if tag=='title':self.in_title=True
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
    def handle_data(self,data):
        if self.in_title:self.title+=data

def safe_url(raw,kind):
    if not raw:return ''
    v=urlsplit(raw.strip())
    if v.scheme!='https' or not v.hostname or v.username or v.password:return ''
    if kind=='embed' and not v.hostname.endswith('.hf.space'):return ''
    if kind=='repo' and v.hostname!='github.com':return ''
    return raw.strip()

def build(output):
    projects=[]
    for page in sorted((ROOT/'projects').glob('*/index.html')):
        slug=page.parent.name
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):
            raise ValueError(f'Unsafe project folder name: {slug}')
        p=MetaReader();p.feed(page.read_text(encoding='utf-8'))
        m=p.meta
        title=m.get('title') or (p.title.split('|')[0].strip()) or slug.replace('-',' ').title()
        desc=m.get('description') or f'Explore the {title} project page.'
        tags=[x.strip() for x in m.get('tags','').split(',') if x.strip()]
        live=safe_url(m.get('live'),'live');embed=safe_url(m.get('embed'),'embed');repo=safe_url(m.get('repo'),'repo')
        projects.append({'slug':slug,'title':title,'description':desc,'category':m.get('category') or 'Other Projects','status':m.get('status') or 'Project page','tags':tags,'page_url':f'./projects/{slug}/','demo_url':live or embed,'repo_url':repo})
    articles=[]
    for page in sorted((ROOT/'articles').glob('*/index.html')):
        slug=page.parent.name
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError(f'Unsafe article slug: {slug}')
        a=MetaReader();a.feed(page.read_text(encoding='utf8'));m=a.meta
        title=m.get('title') or a.title or slug.replace('-',' ').title()
        articles.append({'slug':slug,'title':title,'description':m.get('description',''),'date':m.get('date',''), 'category':m.get('category','Article'), 'url':f'./articles/{slug}/'})
    if not projects:raise ValueError('No projects found. At least one projects/<slug>/index.html is required.')
    output=output.resolve()
    if output==ROOT.resolve() or ROOT.resolve() in output.parents and output.name in ('projects','assets'):raise ValueError('Refusing unsafe output path')
    if output.exists():shutil.rmtree(output)
    output.mkdir(parents=True)
    for name in ('index.html','assets','projects','articles'):
        src=ROOT/name;dst=output/name
        if src.is_dir():shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','.DS_Store'))
        else:shutil.copy2(src,dst)
    (output/'articles.json').write_text(json.dumps(articles,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (output/'projects.json').write_text(json.dumps(projects,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (output/'.nojekyll').write_text('',encoding='utf8')
    print(f'PORTFOLIO BUILD PASSED: {len(projects)} project pages → {output}')
    return projects
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',default=str(ROOT/'dist'));arg=parser.parse_args()
    build(Path(arg.out))
