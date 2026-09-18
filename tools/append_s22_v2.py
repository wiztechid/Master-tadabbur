from pathlib import Path
src=Path('tools/append_s22.py').read_text(encoding='utf-8')
old='''    end="</div>\\n<footer>❖ Master Tadabbur Al-Qur\'an • Sesi 001–021 ❖"\n    if end not in s: raise SystemExit(f'{path}: footer marker missing')\n    s=s.replace(end,ID+'\\n\\n'+EN+"\\n</div>\\n<footer>❖ Master Tadabbur Al-Qur\'an • Sesi 001–022 ❖",1)'''
new='''    if owner:\n        end="<footer>❖ Master Tadabbur Al-Qur'an • Sesi 001–021 ❖"\n        if end not in s: raise SystemExit(f'{path}: OWNER footer marker missing')\n        s=s.replace(end,ID+'\\n\\n'+EN+"\\n<footer>❖ Master Tadabbur Al-Qur'an • Sesi 001–022 ❖",1)\n    else:\n        end="</div>\\n<footer>❖ Master Tadabbur Al-Qur'an • Sesi 001–021 ❖"\n        if end not in s: raise SystemExit(f'{path}: USER footer marker missing')\n        s=s.replace(end,ID+'\\n\\n'+EN+"\\n</div>\\n<footer>❖ Master Tadabbur Al-Qur'an • Sesi 001–022 ❖",1)'''
if old not in src:
    raise SystemExit('v2 patch target missing')
src=src.replace(old,new,1)
exec(compile(src,'append_s22_v2_runtime.py','exec'))
