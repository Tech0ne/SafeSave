import hashlib
import getpass
import shutil
import base64
import ctypes
import time
import sys
import os

############################ PIP ############################

def install_pip():
    if os.name != "nt":
        print("[!] You will have to install pip by yourself !")
        print("[-] Please refer to online documentation to see how to install \"python3-pip\" (usually just need to apt-get, dnf...)")
        sys.exit(1)
    import urllib.request
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print("[+] Fetching pypa.io to retreive get-pip.py script")
    with urllib.request.urlopen("http://bootstrap.pypa.io/get-pip.py", context=ctx) as f:
        data = f.read()

    with open("get-pip.py", 'wb+') as f:
        f.write(data)

    print("[+] Running get-pip.py")
    os.system(f"{sys.executable} get-pip.py")
    os.remove("get-pip.py")
    print("[+] pip is now installed !")

if os.system(f"{sys.executable} -m pip --version") != 0:
    print("[-] pip (Python module installer) is not installed")
    print("[+] Installing pip package manager")
    install_pip()

if os.system(f"{sys.executable} -m pip --version") != 0:
    print("[!] pip installation went wrong !")
    print("[-] Please install pip by hand and try again")
    input()
    sys.exit(1)

did_install = False

for k, v in {
        "rsa": "rsa",
        "rich": "rich",
        "Crypto": "pycryptodome"
    }.items():
    try:
        __import__(k)
    except:
        did_install = True
        print(f"========== Installing required module ({v}) ==========")
        os.system(f"{sys.executable} -m pip install {v}")

if did_install:
    sys.exit(os.system(f"{sys.executable} {' '.join(sys.argv)}"))

############################ PIP ############################

import rsa

from Crypto.Cipher import AES

from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt, Confirm

py_content = b"aW1wb3J0IG9zCmltcG9ydCBzeXMKaW1wb3J0IHJzYQppbXBvcnQgdGltZQppbXBvcnQgc2h1dGlsCmltcG9ydCBiYXNlNjQKaW1wb3J0IGhhc2hsaWIKaW1wb3J0IGdldHBhc3MKCmZyb20gcmljaCBpbXBvcnQgcHJpbnQKZnJvbSByaWNoLnBhbmVsIGltcG9ydCBQYW5lbApmcm9tIHJpY2gucHJvbXB0IGltcG9ydCBQcm9tcHQsIENvbmZpcm0KZnJvbSByaWNoLmNvbnNvbGUgaW1wb3J0IENvbnNvbGUKCmZyb20gQ3J5cHRvLkNpcGhlciBpbXBvcnQgQUVTCgprZXkgPSBiIntLRVl9Igp6aXBfZmlsZSA9IGIie1pJUH0iCgojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIFdJRkkgIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKZGVmIGRpc2FibGVfd2lmaSgpIC0+IGJvb2w6CiAgICBpZiBvcy5uYW1lID09ICJudCI6CiAgICAgICAgcmV0dXJuIG9zLnN5c3RlbSgibmV0c2ggaW50ZXJmYWNlIHNldCBpbnRlcmZhY2UgXCJXaS1GaVwiIGFkbWluPWRpc2FibGUiKSA9PSAwCiAgICBlbHNlOgogICAgICAgIHJldHVybiBvcy5zeXN0ZW0oIm5tY2xpIHJhZGlvIHdpZmkgb2ZmIikgPT0gMAoKZGVmIGVuYWJsZV93aWZpKCkgLT4gYm9vbDoKICAgIGlmIG9zLm5hbWUgPT0gIm50IjoKICAgICAgICByZXR1cm4gb3Muc3lzdGVtKCJuZXRzaCBpbnRlcmZhY2Ugc2V0IGludGVyZmFjZSBcIldpLUZpXCIgYWRtaW49ZW5hYmxlIikgPT0gMAogICAgZWxzZToKICAgICAgICByZXR1cm4gb3Muc3lzdGVtKCJubWNsaSByYWRpbyB3aWZpIG9uIikgPT0gMAoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyBXSUZJICMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMgTElTVHMgIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKZGVmIGxpc3RfZGlmZihyZWY6IGxpc3QsIG5ldzogbGlzdCkgLT4gbGlzdDoKICAgIHJldHVybiBsZW4oW2l0ZW0gZm9yIGl0ZW0gaW4gbmV3IGlmIG5vdCBpdGVtIGluIHJlZl0pCgojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIExJU1RzICMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMgT1MgT1BzICMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCmRlZiByZW1vdmUocGF0aDogc3RyKToKICAgIGlmIG9zLnBhdGguaXNmaWxlKHBhdGgpOgogICAgICAgIG9zLnJlbW92ZShwYXRoKQogICAgZWxpZiBvcy5wYXRoLmlzZGlyKHBhdGgpOgogICAgICAgIHNodXRpbC5ybXRyZWUocGF0aCkKCmRlZiBta2RpcihwYXRoOiBzdHIpOgogICAgaWYgbm90IG9zLnBhdGguaXNkaXIocGF0aCk6CiAgICAgICAgb3MubWtkaXIocGF0aCkKCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMgT1MgT1BzICMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMgUlNBICMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCmRlZiBzaWduKG1lc3NhZ2U6IGJ5dGVzLCBwcml2YXRlX2tleTogcnNhLlByaXZhdGVLZXkpIC0+IGJ5dGVzOgogICAgcmV0dXJuIHJzYS5zaWduKG1lc3NhZ2UsIHByaXZhdGVfa2V5LCAiU0hBLTI1NiIpCgpkZWYgdmVyaWZ5KG1lc3NhZ2U6IGJ5dGVzLCBzaWduYXR1cmU6IGJ5dGVzLCBwdWJsaWNfa2V5OiByc2EuUHVibGljS2V5KSAtPiBib29sOgogICAgdHJ5OgogICAgICAgIHJldHVybiByc2EudmVyaWZ5KG1lc3NhZ2UsIHNpZ25hdHVyZSwgcHVibGljX2tleSkgPT0gIlNIQS0yNTYiCiAgICBleGNlcHQ6CiAgICAgICAgcmV0dXJuIEZhbHNlCgpkZWYgcnNhX2VuY3J5cHQoZGF0YTogYnl0ZXMsIGV4dGVybl9wdWJsaWNfa2V5OiByc2EuUHVibGljS2V5LCBpbnRlcm5fcHJpdmF0ZV9rZXk6IHJzYS5Qcml2YXRlS2V5KSAtPiBieXRlczoKICAgIGNodW5rX3NpemUgPSByc2EuY29tbW9uLmJ5dGVfc2l6ZShleHRlcm5fcHVibGljX2tleS5uKSAtIDExCiAgICBpZiBjaHVua19zaXplIDwgMToKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiUHVibGljIGtleSB0b28gc21hbGwgISAoY2FuIGNyeXB0IG1heCB7Y2h1bmtfc2l6ZX0gYnl0ZXMpIikKICAgIHNwbGl0dGVkX21lc3NhZ2UgPSBbZGF0YVtpOmkrY2h1bmtfc2l6ZV0gZm9yIGkgaW4gcmFuZ2UoMCwgbGVuKGRhdGEpLCBjaHVua19zaXplKV0KICAgIGVuY3J5cHRlZF9tZXNzYWdlID0gW2Jhc2U2NC5iNjRlbmNvZGUocnNhLmVuY3J5cHQoY2h1bmssIGV4dGVybl9wdWJsaWNfa2V5KSkgZm9yIGNodW5rIGluIHNwbGl0dGVkX21lc3NhZ2VdCiAgICBmaW5hbF9tZXNzYWdlID0gYic7Jy5qb2luKGVuY3J5cHRlZF9tZXNzYWdlKQogICAgc2lnbmF0dXJlID0gc2lnbihmaW5hbF9tZXNzYWdlLCBpbnRlcm5fcHJpdmF0ZV9rZXkpCiAgICBqb2luZWRfbWVzc2FnZSA9IGZpbmFsX21lc3NhZ2UgKyBiJ3wnICsgYmFzZTY0LmI2NGVuY29kZShzaWduYXR1cmUpCiAgICByZXR1cm4gam9pbmVkX21lc3NhZ2UKCmRlZiByc2FfZGVjcnlwdChkYXRhOiBieXRlcywgaW50ZXJuX3ByaXZhdGVfa2V5OiByc2EuUHJpdmF0ZUtleSwgZXh0ZXJuX3B1YmxpY19rZXk6IHJzYS5QdWJsaWNLZXkpIC0+IGJ5dGVzOgogICAgcGlwZV9jb3VudCA9IGRhdGEuY291bnQoYid8JykKICAgIGlmIHBpcGVfY291bnQgIT0gMToKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiSW52YWxpZCBmb3JtYXRpbmcgOiBleHBlY3RpbmcgMSAnfCcgYnV0IGZvdW5kIHtwaXBlX2NvdW50fSIpCiAgICBtZXNzYWdlLCBzaWduYXR1cmUgPSBkYXRhLnNwbGl0KGInfCcpCiAgICBpZiBub3QgdmVyaWZ5KG1lc3NhZ2UsIGJhc2U2NC5iNjRkZWNvZGUoc2lnbmF0dXJlKSwgZXh0ZXJuX3B1YmxpY19rZXkpOgogICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIkNvdWxkIG5vdCB2ZXJpZnkgc2lnbmF0dXJlIG9mIG1lc3NhZ2UiKQogICAgY2h1bmtfc2l6ZSA9IHJzYS5jb21tb24uYnl0ZV9zaXplKGludGVybl9wcml2YXRlX2tleS5uKSAtIDExCiAgICBkZWNyeXB0ZWRfbWVzc2FnZSA9IFtyc2EuZGVjcnlwdChiYXNlNjQuYjY0ZGVjb2RlKGNodW5rKSwgaW50ZXJuX3ByaXZhdGVfa2V5KSBmb3IgY2h1bmsgaW4gbWVzc2FnZS5zcGxpdChiJzsnKV0KICAgIGlmIGFueShbbGVuKGNodW5rKSAhPSBjaHVua19zaXplIGZvciBjaHVuayBpbiBkZWNyeXB0ZWRfbWVzc2FnZVs6LTFdXSk6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigiSW52YWxpZCBjaHVuayBzaXplICEiKQogICAgcmV0dXJuIGInJy5qb2luKGRlY3J5cHRlZF9tZXNzYWdlKQoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyBSU0EgIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyBSSUNIICMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCmRlZiBkaXNwbGF5KHRleHQ6IHN0ciwgY29sb3I6IHN0cik6CiAgICBwcmludChQYW5lbCh0ZXh0LCBib3JkZXJfc3R5bGU9Y29sb3IpKQoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyBSSUNIICMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMgVVNCICMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCmRlZiBnZXRfbmV3X3BsdWdnZWRfdXNiKCkgLT4gc3RyOgogICAgaWYgb3MubmFtZSA9PSAibnQiOgogICAgICAgIHBsdWdfa2V5cyA9IFtjaHIoeCkgKyAnOicgZm9yIHggaW4gcmFuZ2UoNjUsIDkxKV0KICAgICAgICBwbHVnZWRfa2V5cyA9IFt4IGZvciB4IGluIHBsdWdfa2V5cyBpZiBvcy5wYXRoLmlzZGlyKHgpXQoKICAgICAgICB3aGlsZSBub3QgbGlzdF9kaWZmKHBsdWdlZF9rZXlzLCBbeCBmb3IgeCBpbiBwbHVnX2tleXMgaWYgb3MucGF0aC5pc2Rpcih4KV0pOgogICAgICAgICAgICB0aW1lLnNsZWVwKDEpCiAgICAgICAgCiAgICAgICAgcmV0dXJuIFtpdGVtIGZvciBpdGVtIGluIFt4IGZvciB4IGluIHBsdWdfa2V5cyBpZiBvcy5wYXRoLmlzZGlyKHgpXSBpZiBub3QgaXRlbSBpbiBwbHVnZWRfa2V5c11bMF0KICAgIGVsc2U6CiAgICAgICAgcGx1Z2VkX2tleXMgPSBvcy5saXN0ZGlyKGYiL21lZGlhL3tnZXRwYXNzLmdldHVzZXIoKX0vIikKCiAgICAgICAgd2hpbGUgbm90IGxpc3RfZGlmZihwbHVnZWRfa2V5cywgb3MubGlzdGRpcihmIi9tZWRpYS97Z2V0cGFzcy5nZXR1c2VyKCl9LyIpKToKICAgICAgICAgICAgdGltZS5zbGVlcCgxKQogICAgICAgIAogICAgICAgIHJldHVybiBvcy5wYXRoLmpvaW4oZiIvbWVkaWEve2dldHBhc3MuZ2V0dXNlcigpfS8iLCBbaXRlbSBmb3IgaXRlbSBpbiBvcy5saXN0ZGlyKGYiL21lZGlhL3tnZXRwYXNzLmdldHVzZXIoKX0vIikgaWYgbm90IGl0ZW0gaW4gcGx1Z2VkX2tleXNdWzBdKQoKZGVmIGdldF91bnBsdWdnZWRfdXNiKCkgLT4gc3RyOgogICAgaWYgb3MubmFtZSA9PSAibnQiOgogICAgICAgIHBsdWdfa2V5cyA9IFtjaHIoeCkgKyAnOicgZm9yIHggaW4gcmFuZ2UoNjUsIDkxKV0KICAgICAgICBwbHVnZWRfa2V5cyA9IFt4IGZvciB4IGluIHBsdWdfa2V5cyBpZiBvcy5wYXRoLmlzZGlyKHgpXQoKICAgICAgICB3aGlsZSBub3QgbGlzdF9kaWZmKFt4IGZvciB4IGluIHBsdWdfa2V5cyBpZiBvcy5wYXRoLmlzZGlyKHgpXSwgcGx1Z2VkX2tleXMpOgogICAgICAgICAgICB0aW1lLnNsZWVwKDEpCiAgICAgICAgCiAgICAgICAgcmV0dXJuIFtpdGVtIGZvciBpdGVtIGluIFt4IGZvciB4IGluIHBsdWdfa2V5cyBpZiBvcy5wYXRoLmlzZGlyKHgpXSBpZiBub3QgaXRlbSBpbiBwbHVnZWRfa2V5c11bMF0KICAgIGVsc2U6CiAgICAgICAgcGx1Z2VkX2tleXMgPSBvcy5saXN0ZGlyKGYiL21lZGlhL3tnZXRwYXNzLmdldHVzZXIoKX0vIikKCiAgICAgICAgd2hpbGUgbm90IGxpc3RfZGlmZihvcy5saXN0ZGlyKGYiL21lZGlhL3tnZXRwYXNzLmdldHVzZXIoKX0vIiksIHBsdWdlZF9rZXlzKToKICAgICAgICAgICAgdGltZS5zbGVlcCgxKQogICAgICAgIAogICAgICAgIHJldHVybiBvcy5wYXRoLmpvaW4oZiIvbWVkaWEve2dldHBhc3MuZ2V0dXNlcigpfS8iLCBbaXRlbSBmb3IgaXRlbSBpbiBwbHVnZWRfa2V5cyBpZiBub3QgaXRlbSBpbiBvcy5saXN0ZGlyKGYiL21lZGlhL3tnZXRwYXNzLmdldHVzZXIoKX0vIildWzBdKQoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyBVU0IgIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyBBRVMgIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKZGVmIGFlc19lbmNyeXB0KGRhdGE6IGJ5dGVzLCBrZXk6IGJ5dGVzKSAtPiBieXRlczoKICAgIGNpcGhlciA9IEFFUy5uZXcoaGFzaGxpYi5zaGEyNTYoa2V5KS5kaWdlc3QoKSwgQUVTLk1PREVfRUFYKQogICAgbm9uY2UgPSBjaXBoZXIubm9uY2UKICAgIGVuY3J5cHRlZCwgdGFnID0gY2lwaGVyLmVuY3J5cHRfYW5kX2RpZ2VzdChkYXRhKQogICAgcmV0dXJuIGJhc2U2NC5iNjRlbmNvZGUobm9uY2UpICsgYid8JyArIGJhc2U2NC5iNjRlbmNvZGUodGFnKSArIGInfCcgKyBiYXNlNjQuYjY0ZW5jb2RlKGVuY3J5cHRlZCkKCmRlZiBhZXNfZGVjcnlwdChkYXRhOiBieXRlcywga2V5OiBieXRlcykgLT4gYnl0ZXM6CiAgICBpZiBkYXRhLmNvdW50KGInfCcpICE9IDI6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkludmFsaWQgZm9ybWF0aW5nIDogZXhwZWN0aW5nIDEgJ3wnIGJ1dCBmb3VuZCB7ZGF0YS5jb3VudChiJ3wnKX0iKQogICAgbm9uY2UsIHRhZywgZW5jcnlwdGVkID0gW2Jhc2U2NC5iNjRkZWNvZGUoeCkgZm9yIHggaW4gZGF0YS5zcGxpdChiJ3wnKV0KICAgIGNpcGhlciA9IEFFUy5uZXcoaGFzaGxpYi5zaGEyNTYoa2V5KS5kaWdlc3QoKSwgQUVTLk1PREVfRUFYLCBub25jZT1ub25jZSkKICAgIHBsYWludGV4dCA9IGNpcGhlci5kZWNyeXB0KGVuY3J5cHRlZCkKICAgIHRyeToKICAgICAgICBjaXBoZXIudmVyaWZ5KHRhZykKICAgIGV4Y2VwdDoKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJDb3JydXB0ZWQgZGF0YSAvIEludmFsaWQgcGFzc3dvcmQiKQogICAgcmV0dXJuIHBsYWludGV4dAoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyBBRVMgIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyBNQUlOICMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCmRlZiBlcnJvcihtZXNzYWdlOiBzdHIsICppbmRpY2F0aW9ucyk6CiAgICBkaXNwbGF5KG1lc3NhZ2UsICJyZWQiKQogICAgZm9yIGluZGljYXRpb24gaW4gaW5kaWNhdGlvbnM6CiAgICAgICAgZGlzcGxheShpbmRpY2F0aW9uLCAieWVsbG93IikKICAgIGlucHV0KCkKICAgIGlmIG5vdCBlbmFibGVfd2lmaSgpOgogICAgICAgIGRpc3BsYXkoIlshXSBFcnJvciB0dXJuaW5nIG9uIFdpLUZpICEiLCAicmVkIikKICAgIHN5cy5leGl0KDEpCgojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIE1BSU4gIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKZGVmIG1haW4oKToKICAgIGNvbnNvbGUgPSBDb25zb2xlKCkKICAgIHB1YiA9IHJzYS5QdWJsaWNLZXkubG9hZF9wa2NzMShiYXNlNjQuYjY0ZGVjb2RlKGtleSksICJQRU0iKQoKICAgIGRpc3BsYXkoIlsrXSBQbGVhc2UgcGx1ZyBpbiB5b3VyIFVTQiBzdGljayB0byBsb2FkIHlvdXIgUHJpdmF0ZSBSU0Ega2V5IiwgImdyZWVuIikKCiAgICB1c2IgPSBnZXRfbmV3X3BsdWdnZWRfdXNiKCkKCiAgICBkaXNwbGF5KGYiWytdIE5ldyBVU0IgY29ubmVjdGVkIG9uIFwie3VzYn1cIiIsICJncmVlbiIpCiAgICAKICAgIGlmIG5vdCBDb25maXJtLmFzaygiW2JsdWVdWz9dIElzIGl0IHlvdXIgVVNCIHN0aWNrID8iKToKICAgICAgICBlcnJvcigiWyFdIEludmFsaWQgcGx1Z2VkIFVTQiIsICJbLV0gUGxlYXNlIGNoZWNrIGFuZCBydW4gdGhpcyBzY3JpcHQgYWdhaW4iKQoKICAgIGlmIG5vdCBvcy5wYXRoLmlzZmlsZShvcy5wYXRoLmpvaW4odXNiLCAicHJpdmF0ZV9rZXkiKSk6CiAgICAgICAgZXJyb3IoIlshXSBJbnZhbGlkIGZvcm1hdCIsICJbLV0gVGhlIGRlc2lnbmF0ZWQgVVNCIHN0aWNrIHdhcyBtaXNzaW5nIGEgXCJwcml2YXRlX2tleVwiIGZpbGUiKQoKICAgIGRpc3BsYXkoIlsrXSBSZWFkaW5nIFJTQSBwcml2YXRlIGtleSBmcm9tIFVTQiBzdGljayIsICJncmVlbiIpCgogICAgd2l0aCBvcGVuKG9zLnBhdGguam9pbih1c2IsICJwcml2YXRlX2tleSIpLCAncmInKSBhcyBmOgogICAgICAgIHByaSA9IGYucmVhZCgpCgogICAgaWYgcHJpLmNvdW50KGInfCcpICE9IDI6CiAgICAgICAgZXJyb3IoIlshXSBJbnZhbGlkIHJlYWQgUlNBIHByaXZhdGUga2V5ICEiLCAiWy1dIFBsZWFzZSBjaGVjayBmb3IgZXJyb3IsIG9yIHVzZSBhIGJhY2t1cCIpCgogICAgcGFzc3dkID0gUHJvbXB0LmFzaygiWz9dIFBhc3N3b3JkIiwgcGFzc3dvcmQ9VHJ1ZSkKCiAgICB0cnk6CiAgICAgICAgcHJpID0gYWVzX2RlY3J5cHQocHJpLCBwYXNzd2QuZW5jb2RlKCkpCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgZXJyb3IoZiJbIV0gQW4gZXJyb3Igb2NjdXJlZCA6IHtlfSIsICJbLV0gUGxlYXNlIGZpbmQgdGhlIHNvdXJjZSBvZiB0aGUgZXJyb3IgYW5kIHRyeSBhZ2FpbiIpCiAgICAKICAgIHByaSA9IHJzYS5Qcml2YXRlS2V5LmxvYWRfcGtjczEocHJpKQoKICAgIGRpc3BsYXkoIlsrXSBTdWNjZXNmdWxseSBsb2FkZWQgdGhlIFJTQSBwcml2YXRlIGtleSIsICJncmVlbiIpCgogICAgZGlzcGxheSgiWytdIFBsZWFzZSB1bnBsdWcgeW91ciBVU0Igc3RpY2siLCAiZ3JlZW4iKQoKICAgIHdoaWxlIGdldF91bnBsdWdnZWRfdXNiKCkgIT0gdXNiOgogICAgICAgIGRpc3BsYXkoIlshXSBJbnZhbGlkIHVucGx1Z2VkIGRldmljZSIsICJ5ZWxsb3ciKQogICAgCiAgICB3aXRoIGNvbnNvbGUuc3RhdHVzKCJbK10gTG9hZGluZyBzYXZlLi4uIiwgc3Bpbm5lcj0iYm91bmNpbmdCYXIiKToKICAgICAgICB0cnk6CiAgICAgICAgICAgIGRjb2RlZF96aXBfY29udGVudCA9IHJzYV9kZWNyeXB0KHppcF9maWxlLCBwcmksIHB1YikKICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgICAgIGVycm9yKGYiWyFdIEFuIGVycm9yIG9jY3VyZWQgd2hlbiBkZWNyeXB0aW5nIHRoZSBaSVAgZmlsZSA6IHtlfSIpCiAgICAgICAgCiAgICAgICAgaWYgb3MucGF0aC5pc2RpcigiU2FmZVNhdmUvIik6CiAgICAgICAgICAgIGRpc3BsYXkoIlshXSBEaXJlY3RvcnkgY2FsbGVkIFwiU2FmZVNhdmUvXCIgYWxyZWFkeSBleGlzdHMgISIsICJ5ZWxsb3ciKQogICAgICAgICAgICBkaXNwbGF5KCJbLV0gUGxlYXNlIHZlcmlmeSBpdCdzIGNvbnRlbnQgYmVmb3JlIGNvbnRpbnVpbmcgKGl0IHdpbGwgYmUgZGVsZXRlZCkiLCAieWVsbG93IikKICAgICAgICAgICAgaW5wdXQoKQogICAgICAgICAgICByZW1vdmUoIlNhZmVTYXZlLyIpCiAgICAgICAgCiAgICAgICAgbWtkaXIoIlNhZmVTYXZlLyIpCgogICAgICAgIHdpdGggb3BlbigiU2FmZVNhdmUuemlwIiwgJ3diKycpIGFzIGY6CiAgICAgICAgICAgIGYud3JpdGUoZGNvZGVkX3ppcF9jb250ZW50KQoKICAgICAgICBkZWwgZGNvZGVkX3ppcF9jb250ZW50CgogICAgICAgIHNodXRpbC51bnBhY2tfYXJjaGl2ZSgiU2FmZVNhdmUuemlwIiwgIlNhZmVTYXZlLyIpCgogICAgICAgIHJlbW92ZSgiU2FmZVNhdmUuemlwIikKICAgIAogICAgZGlzcGxheSgiWytdIExvYWQgc3VjY2Vzc2Z1bGwgISIsICJncmVlbiIpCgogICAgZGlzcGxheShmIlsrXSBZb3VyIGRhdGEgaXMgY3VycmVudGx5IG9wcGVuZWQgb24gdGhlIGZvbGRlciBcIntvcy5wYXRoLmFic3BhdGgoJ1NhZmVTYXZlLycpfVwiIiwgImdyZWVuIGJsaW5rIikKCiAgICBkaXNwbGF5KCJbK10gUHJlc3MgZW50ZXIgdG8gY2xvc2UgYW5kIHNhdmUgdGhlIGRhdGEiLCAiZ3JlZW4iKQoKICAgIHRyeToKICAgICAgICBpbnB1dCgpCiAgICBleGNlcHQ6CiAgICAgICAgcGFzcwoKICAgIHdpdGggY29uc29sZS5zdGF0dXMoIlsrXSBTYXZpbmcgY29udGVudC4uLiIsIHNwaW5uZXI9ImJvdW5jaW5nQmFyIik6CiAgICAgICAgc2h1dGlsLm1ha2VfYXJjaGl2ZSgiU2FmZVNhdmUiLCAiemlwIiwgIlNhZmVTYXZlLyIsICIuIikKICAgICAgICByZW1vdmUoIlNhZmVTYXZlLyIpCiAgICAgICAgd2l0aCBvcGVuKCJTYWZlU2F2ZS56aXAiLCAncmInKSBhcyBmOgogICAgICAgICAgICBkYXRhID0gZi5yZWFkKCkKICAgICAgICByZW1vdmUoIlNhZmVTYXZlLnppcCIpCiAgICAgICAgZW5jcnlwdGVkID0gcnNhX2VuY3J5cHQoZGF0YSwgcHViLCBwcmkpOwogICAgICAgIGRlbCBwcmkKICAgICAgICB3aXRoIG9wZW4oc3lzLmFyZ3ZbMF0sICdyYicpIGFzIGY6CiAgICAgICAgICAgIGNvbnRlbnQgPSBmLnJlYWQoKS5yZXBsYWNlKGInYiInICsgemlwX2ZpbGUgKyBiJyInLCBiJ2IiJyArIGVuY3J5cHRlZCArIGInIicpCiAgICAgICAgd2l0aCBvcGVuKHN5cy5hcmd2WzBdLCAnd2IrJykgYXMgZjoKICAgICAgICAgICAgZi53cml0ZShjb250ZW50KQogICAgCiAgICBkaXNwbGF5KCJbK10gQ29udGVudCBzYXZlZCIsICJncmVlbiBibGluayIpCiAgICAKICAgIGlucHV0KCkKICAgIGVuYWJsZV93aWZpKCkKCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICBtYWluKCk="
zip_content = b"UEsDBBQACAAIABNth1cAAAAAAAAAALMBAAAKACAAUkVBRE1FLnR4dFVUDQAHR71xZeC7cWVHvXFldXgLAAEE6AMAAAToAwAAjY89bsMwDIV3neKtBdLmEF0zZzKgCjabqrAlVT8ZCh2oOYcvlifHSQ10KQFR5OPjJwjQWmONtdooayjsqdZm0K2stPwqt8Os0DF3nLyhkrPHs356KB2OWBSFZZ/eHUm1LemN0i2Frgr/CqVeBSH6UzQTgsRJMgZBMuUsJxMHiWwTBu/cfEltNBln559Iz3zpS7S8XpQ6CD0pWfpNn4uM6L3LVlxG9iUTMW4wDzwbLh99SQie2jfMZ7PfXn23/QeJCb7c6WmHr2KRJBL/hyPFjiMhjn8yfKaEEO1EWi932BVQSwcIA2j69uAAAACzAQAAUEsBAhQDFAAIAAgAE22HVwNo+vbgAAAAswEAAAoAIAAAAAAAAAAAALSBAAAAAFJFQURNRS50eHRVVA0AB0e9cWXgu3FlR71xZXV4CwABBOgDAAAE6AMAAFBLBQYAAAAAAQABAFgAAAA4AQAAAAA="

############################ WIFI ############################

def disable_wifi() -> bool:
    if os.name == "nt":
        return os.system("netsh interface set interface \"Wi-Fi\" admin=disable") == 0
    else:
        return os.system("nmcli radio wifi off") == 0

def enable_wifi() -> bool:
    if os.name == "nt":
        return os.system("netsh interface set interface \"Wi-Fi\" admin=enable") == 0
    else:
        return os.system("nmcli radio wifi on") == 0

############################ WIFI ############################

############################ LISTs ############################

def list_diff(ref: list, new: list) -> list:
    return len([item for item in new if not item in ref])

############################ LISTs ############################

############################ OS OPs ############################

def remove(path: str):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)

def mkdir(path: str):
    if not os.path.isdir(path):
        os.mkdir(path)

############################ OS OPs ############################

############################ RSA ############################

def sign(message: bytes, private_key: rsa.PrivateKey) -> bytes:
    return rsa.sign(message, private_key, "SHA-256")

def verify(message: bytes, signature: bytes, public_key: rsa.PublicKey) -> bool:
    try:
        return rsa.verify(message, signature, public_key) == "SHA-256"
    except:
        return False

def rsa_encrypt(data: bytes, extern_public_key: rsa.PublicKey, intern_private_key: rsa.PrivateKey) -> bytes:
    chunk_size = rsa.common.byte_size(extern_public_key.n) - 11
    if chunk_size < 1:
        raise ValueError(f"Public key too small ! (can crypt max {chunk_size} bytes)")
    splitted_message = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    encrypted_message = [base64.b64encode(rsa.encrypt(chunk, extern_public_key)) for chunk in splitted_message]
    final_message = b';'.join(encrypted_message)
    signature = sign(final_message, intern_private_key)
    joined_message = final_message + b'|' + base64.b64encode(signature)
    return joined_message

def rsa_decrypt(data: bytes, intern_private_key: rsa.PrivateKey, extern_public_key: rsa.PublicKey) -> bytes:
    pipe_count = data.count(b'|')
    if pipe_count != 1:
        raise ValueError(f"Invalid formating : expecting 1 '|' but found {pipe_count}")
    message, signature = data.split(b'|')
    if not verify(message, base64.b64decode(signature), extern_public_key):
        raise ValueError("Could not verify signature of message")
    chunk_size = rsa.common.byte_size(intern_private_key.n) - 11
    decrypted_message = [rsa.decrypt(base64.b64decode(chunk), intern_private_key) for chunk in message.split(b';')]
    if any([len(chunk) != chunk_size for chunk in decrypted_message[:-1]]):
        raise ValueError("Invalid chunk size !")
    return b''.join(decrypted_message)

############################ RSA ############################

############################ RICH ############################

def display(text: str, color: str):
    print(Panel(text, border_style=color))

############################ RICH ############################

############################ USB ############################

def get_new_plugged_usb() -> str:
    if os.name == "nt":
        plug_keys = [chr(x) + ':' for x in range(65, 91)]
        pluged_keys = [x for x in plug_keys if os.path.isdir(x)]

        while not list_diff(pluged_keys, [x for x in plug_keys if os.path.isdir(x)]):
            time.sleep(1)
        
        return [item for item in [x for x in plug_keys if os.path.isdir(x)] if not item in pluged_keys][0]
    else:
        pluged_keys = os.listdir(f"/media/{getpass.getuser()}/")

        while not list_diff(pluged_keys, os.listdir(f"/media/{getpass.getuser()}/")):
            time.sleep(1)
        
        return os.path.join(f"/media/{getpass.getuser()}/", [item for item in os.listdir(f"/media/{getpass.getuser()}/") if not item in pluged_keys][0])

def get_unplugged_usb() -> str:
    if os.name == "nt":
        plug_keys = [chr(x) + ':' for x in range(65, 91)]
        pluged_keys = [x for x in plug_keys if os.path.isdir(x)]

        while not list_diff([x for x in plug_keys if os.path.isdir(x)], pluged_keys):
            time.sleep(1)
        
        return [item for item in [x for x in plug_keys if os.path.isdir(x)] if not item in pluged_keys][0]
    else:
        pluged_keys = os.listdir(f"/media/{getpass.getuser()}/")

        while not list_diff(os.listdir(f"/media/{getpass.getuser()}/"), pluged_keys):
            time.sleep(1)
        
        return os.path.join(f"/media/{getpass.getuser()}/", [item for item in pluged_keys if not item in os.listdir(f"/media/{getpass.getuser()}/")][0])

############################ USB ############################

############################ AES ############################

def aes_encrypt(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(hashlib.sha256(key).digest(), AES.MODE_EAX)
    nonce = cipher.nonce
    encrypted, tag = cipher.encrypt_and_digest(data)
    return base64.b64encode(nonce) + b'|' + base64.b64encode(tag) + b'|' + base64.b64encode(encrypted)

def aes_decrypt(data: bytes, key: bytes) -> bytes:
    if data.count(b'|') != 2:
        raise ValueError(f"Invalid formating : expecting 1 '|' but found {data.count(b'|')}")
    nonce, tag, encrypted = [base64.b64decode(x) for x in data.split(b'|')]
    cipher = AES.new(hashlib.sha256(key).digest(), AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(encrypted)
    try:
        cipher.verify(tag)
    except:
        raise ValueError("Corrupted data / Invalid password")
    return plaintext

############################ AES ############################

############################ MAIN ############################

def error(message: str, *indications):
    display(message, "red")
    for indication in indications:
        display(indication, "yellow")
    input()
    if not enable_wifi():
        display("[!] Error turning on Wi-Fi !", "red")
    sys.exit(1)

############################ MAIN ############################

def main():
    console = Console()
    display("All required modules are installed, shutting off the Wi-Fi for the installation", "green")

    if not disable_wifi():
        error("[!] Something went wrong when turning off Wi-Fi !", "[-] Please check the message, fix the error and run again")

    py_path = "./SafeSave.py"

    with console.status("[+] Generating 4096b RSA keys...", spinner="bouncingBar"):
        pub, pri = rsa.newkeys(4096)

    display("[+] RSA keys generated", "green")

    data = base64.b64decode(py_content).replace(
        b"{KEY}",
        base64.b64encode(
            pub.save_pkcs1("PEM")
        )
    ).replace(
        b"{ZIP}",
        rsa_encrypt(
            base64.b64decode(
                zip_content
            ),
            pub,
            pri
        )
    )

    with open(py_path, 'wb+') as f:
        f.write(data)

    print(Panel("[+] Please choose a password for your RSA private key", border_style="blue"))
    passw = Prompt.ask("[blue][?] Password        ", password=True)
    npass = Prompt.ask("[blue][?] Confirm password", password=True)

    if passw != npass:
        error("[!] Password does not match !", "[-] Please retry, with both of your passwords the same")

    display("[+] Please plug in your USB stick to save your private key", "green")

    usb = get_new_plugged_usb()

    display(f"New USB stick connected to \"{usb}\"", "green")

    if not Confirm.ask("[blue][?] Is it your USB stick ?"):
        error("[!] Invalid pluged USB", "[-] Please check and run this script again")
    
    display("[+] Writing RSA private key on your USB stick", "green")

    private_key = aes_encrypt(pri.save_pkcs1("PEM"), passw.encode())

    with open(os.path.join(usb, "private_key"), 'wb+') as f:
        f.write(private_key)
    
    display("[+] RSA private key wrote into your USB stick", "green")

    display("[+] Please unplug your USB stick", "green")

    while get_unplugged_usb() != usb:
        display("[!] Invalid unpluged device", "yellow")

    display("[+] All good !", "green")
    display("[+] Now, you can run the SafeSave.py file to get your crypted folder", "green blink")

    display("[+] Press enter to finish installation", "green blink")

    input()
    enable_wifi()

if __name__ == "__main__":
    main()