import subprocess, re, sys
def silences(path, db=-38, d=0.12):
    out = subprocess.run(["ffmpeg","-i",path,"-af",f"silencedetect=noise={db}dB:d={d}","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",out)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",out)]
    return list(zip(st,en))
if __name__=="__main__":
    s=silences(sys.argv[1]); print(len(s)); print([(round(a,2),round(b-a,2)) for a,b in s])
