#!/usr/bin/env python3
"""Apply a trusted repository_dispatch payload, rejecting unknown projects or URLs.
Require repository allowlist to prevent project impersonation.
"""
import json,os,re,sys
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
ALLOWED={
  # Add slug: "github-owner/repository" after the first verified deployment.
  "churn-intelligence-lab":"raymuz/churn-intelligence-lab",
}

def valid_https(value,host=None):
    if not value:return ''
    x=urlsplit(value)
    if x.scheme!='https' or not x.hostname or x.username or x.password or x.fragment:return ''
    if host and x.hostname!=host:return ''
    return value

def update(payload):
    slug=payload.get('slug','');repo=payload.get('repo','');live=payload.get('live','');embed=payload.get('embed','')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError('Invalid slug')
    page=ROOT/'projects'/slug/'index.html'
    if not page.exists():raise ValueError('Unknown project: '+slug)
    if slug not in ALLOWED:raise ValueError('Project not added to trusted deployment allowlist: '+slug)
    owner_repo=ALLOWED[slug]
    if repo!=f'https://github.com/{owner_repo}':raise ValueError('Repository not an approved source')
    if not valid_https(live) or urlsplit(live).hostname not in ('huggingface.co',):raise ValueError('Invalid Hugging Face Space link')
    if urlsplit(live).path != '/spaces/raymuz/Customer_Churn_Intelligence_Lab' and slug == 'churn-intelligence-lab':raise ValueError('Unexpected Churn Space')
    if '/spaces/' not in urlsplit(live).path:raise ValueError('Invalid Space path')
    if embed and (not valid_https(embed) or not urlsplit(embed).hostname.endswith('.hf.space')):raise ValueError('Invalid embed domain')
    html=page.read_text('utf8')
    for key,val in [('repo',repo),('live',live),('embed',embed)]:
        pattern=r'(<meta\s+name=[\"\']portfolio:'+key+r'[\"\']\s+content=[\"\'])[^\"\']*([\"\'])'
        html,n=re.subn(pattern,lambda m:m.group(1)+escape(val,quote=True)+m.group(2),html,count=1)
        if n!=1:raise ValueError('Missing required portfolio:'+key+' metadata')
    page.write_text(html,encoding='utf8')
    print('Updated verified deployment:',slug)
if __name__=='__main__':update(json.loads(os.environ.get('DEPLOYMENT_JSON','{}')))
