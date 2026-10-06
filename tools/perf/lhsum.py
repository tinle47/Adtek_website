import json,sys
for f in sys.argv[1:]:
    d=json.load(open(f)); a=d['audits']
    print("=====",f.split('/')[-1], "score", round(d['categories']['performance']['score']*100), d.get('runtimeError'))
    for k in ['first-contentful-paint','largest-contentful-paint','total-blocking-time','cumulative-layout-shift','speed-index','interactive']:
        print(f"  {k}: {a[k]['displayValue']}")
    print("  LCP element:", json.dumps(a.get('largest-contentful-paint-element',{}).get('details',{}))[:600])
    opps=[(k,v) for k,v in a.items() if v.get('details',{}).get('type')=='opportunity' and (v.get('score') or 1)<0.9]
    for k,v in sorted(opps,key=lambda x:-(x[1]['details'].get('overallSavingsMs') or 0)):
        print(f"  OPP {k}: {v.get('displayValue','')} ms={v['details'].get('overallSavingsMs')}")
        for it in v['details'].get('items',[])[:6]:
            print("     ", str(it.get('url',''))[:110], it.get('wastedMs',''), it.get('wastedBytes',''), it.get('totalBytes',''))
    for k in ['total-byte-weight','bootup-time','mainthread-work-breakdown','third-party-summary','server-response-time','dom-size','font-display','layout-shifts','unsized-images','uses-long-cache-ttl']:
        v=a.get(k); 
        if v: print(f"  {k}: score={v.get('score')} {v.get('displayValue','')}")
    for it in a['bootup-time']['details']['items'][:8]: print("     boot", it['url'][:100], round(it['total']), round(it.get('scripting',0)))
    for it in a['third-party-summary'].get('details',{}).get('items',[])[:6]: print("     3p", it['entity'], it.get('transferSize'), round(it.get('blockingTime',0)))
