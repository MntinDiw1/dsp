import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft
from task2_enhance import gain_ctrl
W='../w/'
sr,e5=wavfile.read(W+'enhanced_5cm.wav'); e5=e5/2**31
sr1,e1=wavfile.read(W+'enhanced_1m.wav'); e1=e1/2**31
# gain curves, same settings as run_tasks.py
g5=np.ones(len(e5)); g1=np.ones(len(e1))
gain_ctrl(0,80,-16,sr,g5,q=0.1); gain_ctrl(95,400,4,sr,g5,q=0.1); gain_ctrl(3000,10000,6,sr,g5,q=0.1); gain_ctrl(12200,sr//2-1,-12,sr,g5,q=0.1)
gain_ctrl(0,sr1//2-1,21,sr1,g1); gain_ctrl(0,85,-12,sr1,g1,q=0.3); gain_ctrl(95,180,6,sr1,g1,q=0.3); gain_ctrl(480,505,-12,sr1,g1,q=0.25)
gain_ctrl(2200,2800,-4,sr1,g1,q=0.25); gain_ctrl(3000,10000,7,sr1,g1,q=0.1); gain_ctrl(13000,sr1//2-1,-30,sr1,g1,q=0.1)
fig,ax=plt.subplots(1,2,figsize=(10,3.6),sharey=True)
for a,g,t in ((ax[0],g5,'5 cm'),(ax[1],g1,'1 m')):
    n=len(g); f=np.arange(n//2)*sr/n
    a.plot(f,20*np.log10(g[:n//2]),color='tab:green'); a.set_xscale('log'); a.set_title(t)
    a.set_xlabel('frequency (Hz)'); a.grid(which='both',ls='--',lw=0.5)
ax[0].set_ylabel('gain (dB)'); plt.tight_layout(); plt.savefig('figures/gain_curves.pdf')
# overlay
plt.figure(figsize=(8,4.5))
for lab,x in (('5 cm',e5),('1 m',e1)):
    n=len(x); m=20*np.log10(np.abs(fft(x)/n)[:n//2]+1e-12); plt.plot(np.arange(n//2)*sr/n,m,alpha=0.6,label=lab)
plt.xscale('log'); plt.xlabel('frequency (Hz)'); plt.ylabel('magnitude (dBFS)'); plt.legend(); plt.xlim(20,24000); plt.tight_layout()
plt.savefig('figures/overlay_enhanced.pdf')
print(20*np.log10(g5.max()),20*np.log10(g1.max()))
