import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft
from task3_exciter import exciter
W='../w/'
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
R={}
for nm in ('5cm','1m'):
    sr,a=wavfile.read(W+nm+'.wav'); R[nm]=a/2**31
def mag(x):
    n=len(x); return np.arange(n//2)*sr/n, 20*np.log10(np.abs(fft(x)[:n//2]/n)+1e-12)
# --- Task 1 time + frequency
for nm,lab in (('5cm','5 cm'),('1m','1 m')):
    x=R[nm]; n=len(x); t=np.linspace(0,n/sr,n); f,m=mag(x)
    fig,ax=plt.subplots(1,2,figsize=(10,3.6))
    ax[0].plot(t,x,lw=.5,color='tab:blue'); ax[0].set_xlabel('time (s)'); ax[0].set_ylabel('normalised amplitude'); ax[0].set_title('time domain')
    ax[1].plot(f,m,lw=.4,color='tab:blue'); ax[1].set_xscale('log'); ax[1].set_xlim(20,24000); ax[1].set_xlabel('frequency (Hz)'); ax[1].set_ylabel('magnitude (dBFS)'); ax[1].set_title('frequency domain')
    plt.tight_layout(); plt.savefig(f'figures/task1_{nm}.pdf'); plt.close()
# --- Task 1 annotated
cons={'5cm':(2000,12000),'1m':(2000,10000)}; noise={'5cm':(16000,24000),'1m':(14000,24000)}
fig,ax=plt.subplots(2,1,figsize=(9,8),sharex=True)
for a,nm,lab in zip(ax,('5cm','1m'),('5 cm','1 m')):
    f,m=mag(R[nm]); a.plot(f,m,lw=.4,color='tab:blue'); a.set_xscale('log'); a.set_xlim(20,24000)
    lo,hi=a.get_ylim(); ytop=m[(f>50)].max()
    a.axvspan(90,110,color='tab:red',alpha=.25); a.text(100,ytop+4,'vowel $f_0$ ≈ 93–104 Hz\n(harmonics at $kf_0$)',color='tab:red',ha='left',va='bottom',fontsize=8)
    a.axvspan(*cons[nm],color='tab:orange',alpha=.15); a.text(np.sqrt(cons[nm][0]*cons[nm][1]),ytop+4,'consonants\n%g–%g kHz'%(cons[nm][0]/1e3,cons[nm][1]/1e3),color='tab:orange',ha='center',va='bottom',fontsize=8)
    a.axvspan(*noise[nm],color='tab:gray',alpha=.3); a.text(23500,ytop+4,'noise only\n>%g kHz'%(noise[nm][0]/1e3),color='dimgray',ha='right',va='bottom',fontsize=8)
    a.set_ylim(lo,ytop+22); a.set_ylabel('magnitude (dBFS)'); a.set_title(lab)
ax[1].set_xlabel('frequency (Hz)'); plt.tight_layout(); plt.savefig('figures/task1_annotated.pdf'); plt.close()
# --- Task 3
x=R['5cm']; n=len(x)
def sm(y,k=200):
    X=np.abs(np.fft.rfft(y))/len(y)*2; p=np.convolve(X**2,np.ones(k)/k,'same'); return np.arange(len(X))*sr/len(y),10*np.log10(p+1e-18)
f,md=sm(x)
cfg={'1: 1750–2250 Hz, keep 5–7 kHz, drive 10, mix 0.5':(1750,2250,5000,7000,10,0.5),
     '2: same bands, drive 3, mix 0.1':(1750,2250,5000,7000,3,0.1),
     '3: 2–4 kHz, keep 4–12 kHz, drive 3, mix 0.25':(2000,4000,4000,12000,3,0.25),
     '4: keep 5.5–12 kHz, drive 6, mix 0.15':(2000,4000,5500,12000,6,0.15),
     'final: keep 5.5–10 kHz, drive 4, mix 0.25':(2000,4000,5500,10000,4,0.25)}
fig,ax=plt.subplots(figsize=(9,5)); s=(f>=2000)&(f<=14000)
ax.plot(f[s],md[s],color='k',lw=1.6,label='dry voice')
cols=['tab:red','tab:orange','tab:olive','tab:green','tab:blue']
H={}
for (k,c),col in zip(cfg.items(),cols):
    y,nl,h=exciter(x,sr,*c); H[k]=(y,h); fh,mh=sm(h); ax.plot(f[s],mh[s],color=col,lw=1,label='added harmonics, iteration '+k)
ax.axvline(6000,color='gray',ls=':'); ax.text(6050,-57,'3rd harmonic of 2 kHz',fontsize=8,va='top')
ax.set_xlabel('frequency (Hz)'); ax.set_ylabel('power spectral level (dBFS, smoothed over 50 Hz)'); ax.set_xscale('log'); ax.set_xticks([2000,3000,4000,6000,8000,12000]); ax.set_xticklabels(['2k','3k','4k','6k','8k','12k'])
ax.set_ylim(-125,-55); ax.legend(fontsize=7,loc='lower left'); plt.tight_layout(); plt.savefig('figures/exciter_iterations.pdf'); plt.close()
# before/after
y,h=H['final: keep 5.5–10 kHz, drive 4, mix 0.25']; fy,my=sm(y); fh,mh=sm(h)
fig,ax=plt.subplots(figsize=(9,4.5))
ax.axvspan(2000,4000,color='tab:orange',alpha=.15); ax.text(2800,max(md[s])+3,'sidechain\n2–4 kHz',ha='center',fontsize=8,color='tab:orange')
ax.axvspan(5500,10000,color='tab:blue',alpha=.1); ax.text(7400,max(md[s])+3,'harmonics kept\n5.5–10 kHz',ha='center',fontsize=8,color='tab:blue')
s2=(f>=2000)&(f<=12000)
ax.plot(f[s2],md[s2],color='k',lw=1.4,label='before (dry)'); ax.plot(f[s2],my[s2],color='tab:green',lw=1.1,label='after (dry + harmonics)'); ax.plot(f[s2],mh[s2],color='tab:blue',lw=.8,ls='--',label='added harmonics only')
ax.set_xscale('log'); ax.set_xticks([2000,3000,4000,6000,8000,12000]); ax.set_xticklabels(['2k','3k','4k','6k','8k','12k']); ax.set_ylim(-125,max(md[s2])+12)
ax.set_xlabel('frequency (Hz)'); ax.set_ylabel('power spectral level (dBFS, smoothed over 50 Hz)'); ax.legend(fontsize=8,loc='lower left'); plt.tight_layout(); plt.savefig('figures/exciter_before_after.pdf'); plt.close()
# drive compare at final bands
fig,ax=plt.subplots(figsize=(9,4.5)); ax.plot(f[s2],md[s2],color='k',lw=1.4,label='dry voice')
for d,col in ((2,'tab:green'),(4,'tab:blue'),(6,'tab:red')):
    y2,nl,h2=exciter(x,sr,2000,4000,5500,10000,d,0.25); fh,mh=sm(h2); ax.plot(f[s2],mh[s2],color=col,lw=1,label=f'added harmonics, drive {d}')
ax.set_xscale('log'); ax.set_xticks([2000,3000,4000,6000,8000,12000]); ax.set_xticklabels(['2k','3k','4k','6k','8k','12k'])
ax.set_ylim(-125,-70); ax.set_xlabel('frequency (Hz)'); ax.set_ylabel('power spectral level (dBFS, smoothed over 50 Hz)'); ax.legend(fontsize=8,loc='lower left'); plt.tight_layout(); plt.savefig('figures/exciter_drive_compare.pdf'); plt.close()
for d in (2,4,6):
    y2,nl,h2=exciter(x,sr,2000,4000,5500,10000,d,0.25); fh,mh=sm(h2); ss=(f>=5500)&(f<=7000); print('drive',d,'harm vs dry @5.5-7k',round(float(mh[ss].mean()-md[ss].mean()),1),'peak',np.abs(y2).max(),'rms',np.sqrt(np.mean(y2**2)))
