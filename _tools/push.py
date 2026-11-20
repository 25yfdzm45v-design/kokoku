#!/usr/bin/env python3
"""使い方: python3 _tools/push.py "<コミット文>" [セッションURL]  変更があればコミットして push する。"""
import subprocess,sys,os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g=lambda *a:subprocess.run(['git','-C',R,*a],check=True,capture_output=True,text=True).stdout
g('add','-A')
if not g('diff','--cached','--name-only').strip():print('no change');sys.exit(0)
msg=sys.argv[1]+'\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'+('\nClaude-Session: '+sys.argv[2] if len(sys.argv)>2 else '')
g('-c','user.name=Claude','-c','user.email=noreply@anthropic.com','commit','-q','-m',msg)
g('-c','push.negotiate=true','push','-q','origin','HEAD:main');print('pushed')
