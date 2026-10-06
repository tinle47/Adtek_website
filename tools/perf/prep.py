import re,os,subprocess,sys,glob,urllib.parse
S=os.environ.get('PERF_WORK') or os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','build','perf'); site=S+'/site'
def fetch(path):
    dst=site+path
    if os.path.exists(dst): return dst
    os.makedirs(os.path.dirname(dst),exist_ok=True)
    r=subprocess.run(['curl','-sS','--compressed','-f','-o',dst,'https://adtek.agency'+urllib.parse.quote(path)])
    return dst if r.returncode==0 else None
def crawl_css(path,seen):
    if path in seen: return
    seen.add(path); f=fetch(path)
    if not f: print('MISS',path); return
    css=open(f,errors='ignore').read()
    d=path.rsplit('/',1)[0]+'/'
    for m in re.finditer(r'@import\s+(?:url\(\s*)?["\']?([^"\')\s;]+)',css):
        t=os.path.normpath(d+m.group(1)) if not m.group(1).startswith('/') else m.group(1)
        crawl_css(t,seen)
seen=set()
for page in glob.glob(S+'/pages/*.orig.html'):
    h=open(page).read()
    for m in re.finditer(r'<link[^>]+rel=["\']stylesheet["\'][^>]*>',h):
        href=re.search(r'href=["\']([^"\']+)',m.group(0)).group(1)
        u=urllib.parse.urlparse(href)
        if u.netloc in ('','adtek.agency'): crawl_css(u.path,seen)
    for m in re.finditer(r'<script[^>]+src=["\']https://adtek\.agency(/template(?:-v2)?/js/[^"\']+)',h):
        if '/libs/' not in m.group(1): fetch(m.group(1))
print(len(seen),'css files')
