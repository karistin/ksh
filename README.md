# ksh

> simple shell project!!  
> shell for study how shell works

## 프로젝트 소개  

### [노션 링크](https://living-light-8ce.notion.site/Bash-61bb870ee1db4a95b034ddf1a412b4ce)



``` bash
.  
├── README.md  
├── bash.py  # ksh 프로그램  
└── term.py  #  vt 100 cusrer program
```

---

### Example VT100
```python
#!/usr/bin/env python

import os
import sys
import time
'''
Up: \u001b[{n}A
Down: \u001b[{n}B
Right: \u001b[{n}C
Left: \u001b[{n}D
n is count
'''
sys.stdout.write(u"Hello_World\u001b[1D")
sys.stdout.flush()
# Hello_Worl*d

time.sleep(10000)

```