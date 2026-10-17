import unittest,sys,tempfile,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import discover_public_apps as d

class DiscoveryTests(unittest.TestCase):
 def test_opt_in_only(self):
  sample={'name':'demo','full_name':'raymuz/demo','owner':{'login':'raymuz'},'private':False}
  self.assertEqual(d.sync([sample],get_manifest_fn=lambda r:None),[])
  self.assertEqual(d.sync([{**sample,'private':True}],get_manifest_fn=lambda r: {'portfolio':True},normalizer=lambda r,m: self.fail('private repo was evaluated')),[])
 def test_metadata_changes_and_idempotence(self):
  src=(Path(__file__).resolve().parents[1]/'projects/googlesaada/index.html').read_text()
  with tempfile.TemporaryDirectory() as tmp:
   old=d.ROOT;d.ROOT=Path(tmp)
   try:
    page=Path(tmp)/'projects/googlesaada/index.html';page.parent.mkdir(parents=True);page.write_text(src)
    app={'name':'google','full_name':'raymuz/google','owner':{'login':'raymuz'}}
    m={'portfolio':True,'slug':'googlesaada'}
    payload={'slug':'googlesaada','title':'GoogleSaada','description':'Soccer analytics demo','category':'AI Applications','tags':['AI'],'repo':'https://github.com/raymuz/google','live':'https://huggingface.co/spaces/raymuz/GoogleSaada','embed':'https://raymuz-googlesaada.hf.space'}
    run=lambda:d.sync([app],get_manifest_fn=lambda r:m,normalizer=lambda r,x:payload)
    self.assertEqual(run(),['googlesaada']);self.assertEqual(run(),[])
    t=page.read_text();self.assertIn('https://raymuz-googlesaada.hf.space',t)
   finally:d.ROOT=old
 def test_create_new(self):
  with tempfile.TemporaryDirectory() as tmp:
   old=d.ROOT;d.ROOT=Path(tmp)
   try:
    app={'name':'new','full_name':'raymuz/new','owner':{'login':'raymuz'}}
    item={'slug':'new-model','title':'New Model','description':'Public demonstration','category':'AI','tags':['ML'],'repo':'https://github.com/raymuz/new','live':'https://huggingface.co/spaces/raymuz/new','embed':'https://raymuz-new.hf.space'}
    self.assertEqual(d.sync([app],get_manifest_fn=lambda r:{'portfolio':True},normalizer=lambda r,m:item),['new-model'])
    self.assertIn('New Model',(Path(tmp)/'projects/new-model/index.html').read_text())
   finally:d.ROOT=old
 def test_invalid(self):
  with self.assertRaises(ValueError):d.normalize({'full_name':'raymuz/test'}, {'portfolio':True,'slug':'../escape','hf_space':'raymuz/app','title':'Title','description':'Desc'})
  with self.assertRaises(ValueError):d.normalize({'full_name':'raymuz/test'}, {'portfolio':True,'slug':'safe','hf_space':'other/app','title':'Title','description':'Desc'})
if __name__=='__main__':unittest.main()
