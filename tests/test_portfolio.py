from pathlib import Path
from tempfile import TemporaryDirectory
import unittest, sys, json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_portfolio import build, safe_url, ROOT
class PortfolioTests(unittest.TestCase):
    def test_safe_urls(self):
        self.assertEqual(safe_url('javascript:alert(1)','live'),'')
        self.assertEqual(safe_url('https://evil.com','embed'),'')
        self.assertEqual(safe_url('https://author-app.hf.space','embed'),'https://author-app.hf.space')
        self.assertEqual(safe_url('https://github.com/raymuz/repo','repo'),'https://github.com/raymuz/repo')
        self.assertEqual(safe_url('https://evil.com/repo','repo'),'')
    def test_all_pages_catalogued_and_safe(self):
        with TemporaryDirectory() as temp:
            out=Path(temp)/'public';projects=build(out)
            expected=list((ROOT/'projects').glob('*/index.html'))
            self.assertEqual(len(projects),len(expected))
            self.assertGreaterEqual(len(projects),30)
            self.assertEqual(json.loads((out/'projects.json').read_text()),projects)
            self.assertTrue((out/'index.html').exists())
            self.assertTrue((out/'projects/churn-intelligence-lab/index.html').exists())
            self.assertFalse((out/'Musa_Adamou_CV.docx').exists())
            for p in projects:
                self.assertTrue((out/p['page_url'].lstrip('./')/'index.html').is_file(),p['slug'])
                self.assertEqual(p['demo_url'],'') # don't invent deployments
    def test_no_secrets_or_private_cv(self):
        for file in (ROOT/'index.html',*list((ROOT/'projects').glob('*/index.html'))):
            content=file.read_text()
            self.assertNotIn('701 740 2069',content)
            self.assertNotIn('raymuz7@gmail.com',content)
            self.assertNotIn('Security Clearance: Secret',content)
if __name__=='__main__':unittest.main()
