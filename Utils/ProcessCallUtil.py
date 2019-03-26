import subprocess

def python_call_powershell(path):
    fdout = open("../TMP/tmp.out", 'w')
    fderr = open("../TMP/tmp.err", 'w')
    try:
        args=[r"powershell", path]
        child = subprocess.Popen(args,stdout=fdout,stderr=fderr)
        return child.pid
    except Exception:
        return -1


def python_call_python(path):
    fdout = open("../TMP/tmp.out", 'w')
    fderr = open("../TMP/tmp.err", 'w')
    try:
        args=["python", path]
        child = subprocess.Popen(args,stdout=fdout,stderr=fderr)
        return child.pid
    except Exception:
        return -1