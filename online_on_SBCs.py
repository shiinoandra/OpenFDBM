from scipy.io import loadmat
import numpy.matlib as nplib
import alsaaudio as audio
import scipy as scp
import numpy as np
import time as tm

# How long do you want to run the code?
minutes = 120

# Input & Output Settings
with_FDBM = 1 #0=noFDBM, 1=front, 2=left, 3=rigth
audioformat = audio.PCM_FORMAT_S16_LE
channels_inp = 2
channels_out = 2
framerate = 16000
periodsize = 256
print('BufferSize = %i samples and FrameLength = %.3f ms'% (periodsize,2*periodsize*1000/framerate))

# Input Device, ADC-USB
inp = audio.PCM(audio.PCM_CAPTURE,audio.PCM_NORMAL,device='plughw:1,0')
inp.setchannels(channels_inp)
inp.setrate(framerate)
inp.setformat(audioformat)
inp.setperiodsize(periodsize)


# Output Device, SBC or Laptop
out = audio.PCM(audio.PCM_PLAYBACK,audio.PCM_NORMAL,device='plughw:1,0')
out.setchannels(channels_out)
out.setrate(framerate)
out.setformat(audioformat)
out.setperiodsize(periodsize)

# Load ILD-and-IPD DataBase
for k,v in loadmat('IPDILDopen.mat').items(): exec(k+'=v[:,0]') if k[0]!='_' else None

# Frequency Domain Binaural Model (FDBM)
nfft = 512; Fcut = 1000; WinLen = nfft
Win = nplib.repmat(np.sin(np.pi*(np.arange(WinLen))/WinLen),2,1).T
FrmShf = np.int(WinLen/2)
indx = F<Fcut
IPDmaxmin = IPDmaxmin[indx]
ILDmaxmin = ILDmaxmin[~indx]
IPDtargetF = IPDtargetF[indx]
ILDtargetF = ILDtargetF[~indx]
IPDtargetL = IPDtargetL[indx]
ILDtargetL = ILDtargetL[~indx]
IPDtargetR = IPDtargetR[indx]
ILDtargetR = ILDtargetR[~indx]
count = 0; end_signal = np.int(np.ceil(60.0*minutes*framerate/periodsize))
x = np.zeros((WinLen,2))
xbuf = np.zeros((WinLen,2))

while True:
    l,data = inp.read()
    
    if count == end_signal:
        break
    if len(data) != WinLen*2:
        print("skip this data %i samples" % (len(data)))
        continue
    
    if with_FDBM == 1:
        xi = np.fromstring(data,dtype=np.int16)
        xi = np.reshape(np.float32(xi),(np.int16(xi.shape[0]/2),2))
        #xi = xi[:,[1,0]]
        x[FrmShf::,:] = xi
        
        Xbuf = scp.fft((x*Win).T,nfft)
        
        XIS = Xbuf[1,0:np.int(nfft/2)]/Xbuf[0,0:np.int(nfft/2)]
        IPDtest = np.angle(XIS[indx])
        ILDtest = 20*np.log10(np.abs(XIS[~indx]))
        
        muIPD = np.abs(IPDtest-IPDtargetF)/IPDmaxmin
        muILD = np.abs(ILDtest-ILDtargetF)/ILDmaxmin
        
        mu = np.concatenate((muIPD,muILD))
        mu[mu>1]=1;
        
        G = (1-mu)**16
        G = G/np.max(G)
        G = np.concatenate((G,G[::-1]))
        
        sig_fdbm = np.real(scp.ifft(Xbuf*nplib.repmat(G,2,1)))[:,0:WinLen].T*Win
        
        xbuf[0:FrmShf,:] = xbuf[FrmShf::,:] + sig_fdbm[0:FrmShf,:]
        xbuf[FrmShf::,:] = sig_fdbm[FrmShf::,:]
        data = bytes(np.int16(xbuf[0:FrmShf,:]))
        out.write(data)
        x[0:FrmShf,:] = xi
    elif with_FDBM == 2:
        xi = np.fromstring(data,dtype=np.int16)
        xi = np.reshape(np.float32(xi),(np.int16(xi.shape[0]/2),2))
        #xi = xi[:,[1,0]]
        x[FrmShf::,:] = xi
        
        Xbuf = scp.fft((x*Win).T,nfft)
        
        XIS = Xbuf[1,0:np.int(nfft/2)]/Xbuf[0,0:np.int(nfft/2)]
        IPDtest = np.angle(XIS[indx])
        ILDtest = 20*np.log10(np.abs(XIS[~indx]))
        
        muIPD = np.abs(IPDtest-IPDtargetL)/IPDmaxmin
        muILD = np.abs(ILDtest-ILDtargetL)/ILDmaxmin
        
        mu = np.concatenate((muIPD,muILD))
        mu[mu>1]=1;
        
        G = (1-mu)**16
        G = G/np.max(G)
        G = np.concatenate((G,G[::-1]))
        
        sig_fdbm = np.real(scp.ifft(Xbuf*nplib.repmat(G,2,1)))[:,0:WinLen].T*Win
        
        xbuf[0:FrmShf,:] = xbuf[FrmShf::,:] + sig_fdbm[0:FrmShf,:]
        xbuf[FrmShf::,:] = sig_fdbm[FrmShf::,:]
        data = bytes(np.int16(xbuf[0:FrmShf,:]))
        out.write(data)
        x[0:FrmShf,:] = xi
    elif with_FDBM == 3:
        xi = np.fromstring(data,dtype=np.int16)
        xi = np.reshape(np.float32(xi),(np.int16(xi.shape[0]/2),2))
        #xi = xi[:,[1,0]]
        x[FrmShf::,:] = xi
        
        Xbuf = scp.fft((x*Win).T,nfft)
        
        XIS = Xbuf[1,0:np.int(nfft/2)]/Xbuf[0,0:np.int(nfft/2)]
        IPDtest = np.angle(XIS[indx])
        ILDtest = 20*np.log10(np.abs(XIS[~indx]))
        
        muIPD = np.abs(IPDtest-IPDtargetR)/IPDmaxmin
        muILD = np.abs(ILDtest-ILDtargetR)/ILDmaxmin
        
        mu = np.concatenate((muIPD,muILD))
        mu[mu>1]=1;
        
        G = (1-mu)**16
        G = G/np.max(G)
        G = np.concatenate((G,G[::-1]))
        
        sig_fdbm = np.real(scp.ifft(Xbuf*nplib.repmat(G,2,1)))[:,0:WinLen].T*Win
        
        xbuf[0:FrmShf,:] = xbuf[FrmShf::,:] + sig_fdbm[0:FrmShf,:]
        xbuf[FrmShf::,:] = sig_fdbm[FrmShf::,:]
        data = bytes(np.int16(xbuf[0:FrmShf,:]))
        out.write(data)
        x[0:FrmShf,:] = xi
    else:
        xi = np.fromstring(data,dtype=np.int16)
        xi = np.reshape(np.float32(xi),(np.int16(xi.shape[0]/2),2))
        xi = xi[:,[0,1]]*0.6
        x[FrmShf::,:] = xi
        
        Xbuf = scp.fft((x*Win).T,nfft)
                
        sig_fdbm = np.real(scp.ifft(Xbuf))[:,0:WinLen].T*Win
        
        xbuf[0:FrmShf,:] = xbuf[FrmShf::,:] + sig_fdbm[0:FrmShf,:]
        xbuf[FrmShf::,:] = sig_fdbm[FrmShf::,:]
        data = bytes(np.int16(xbuf[0:FrmShf,:]))
        out.write(data)
        x[0:FrmShf,:] = xi
    count += 1
