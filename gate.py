import sys,subprocess
infile,outfile,title=sys.argv[1],sys.argv[2],sys.argv[3]
pt=b'PN_UNLOCKED'+open(infile,'rb').read()
cipher=subprocess.run(['openssl','enc','-aes-256-cbc','-md','md5','-salt','-a','-A','-pass','pass:phantom'],input=pt,capture_output=True).stdout.decode().strip()
tpl=open("gate_template.html").read().replace("__CIPHER__",cipher).replace("__TITLE__",title)
open(outfile,'w').write(tpl)
print(f"gated {outfile} ({len(cipher)} cipher bytes)")
