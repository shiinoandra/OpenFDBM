from scipy.io import loadmat
import numpy.matlib as nplib
import alsaaudio as audio
import scipy as scp
import numpy as np
import time as tm
import threading
from flask_cors import CORS, cross_origin
import json

# How long do you want to run the code?
minutes = 120

# Input & Output Settings
with_FDBM = 0 #0=noFDBM, 1=front, 2=left, 3=rigth
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
nfft = 512; Fcut = 1000; WinLen = nfft; drt=9
Win = nplib.repmat(np.sin(np.pi*(np.arange(WinLen))/WinLen),2,1).T
FrmShf = np.int(WinLen/2)
indx = F<Fcut
IPDmaxmin = IPDmaxmin[indx]; ILDmaxmin = ILDmaxmin[~indx]
IPDtargetF = IPDtargetF[indx]; ILDtargetF = ILDtargetF[~indx]
IPDtargetL = IPDtargetL[indx]; ILDtargetL = ILDtargetL[~indx]
IPDtargetR = IPDtargetR[indx]; ILDtargetR = ILDtargetR[~indx]
count = 0; end_signal = np.int(np.ceil(60.0*minutes*framerate/periodsize))
x = np.zeros((WinLen,2))
xbuf = np.zeros((WinLen,2))

def FDBM_process():
    global count
    global with_FDBM
    while True:
        l,data = inp.read()

        if count == end_signal:
            break
        if len(data) != WinLen*2:
            print("skip this data %i samples" % (len(data)))
            continue

        xi = np.fromstring(data,dtype=np.int16)
        xi = np.reshape(np.float32(xi),(np.int16(xi.shape[0]/2),2))

        if with_FDBM > 0:
            x[FrmShf::,:] = xi

            Xbuf = scp.fft((x*Win).T,nfft)

            XIS = Xbuf[1,0:np.int(nfft/2)]/Xbuf[0,0:np.int(nfft/2)]
            IPDtest = np.angle(XIS[indx])
            ILDtest = 20*np.log10(np.abs(XIS[~indx]))
            
            if with_FDBM == 1:
                muIPD = np.abs(IPDtest-IPDtargetF)/IPDmaxmin
                muILD = np.abs(ILDtest-ILDtargetF)/ILDmaxmin
            elif with_FDBM == 2:
                muIPD = np.abs(IPDtest-IPDtargetL)/IPDmaxmin
                muILD = np.abs(ILDtest-ILDtargetL)/ILDmaxmin
            elif with_FDBM == 3:
                muIPD = np.abs(IPDtest-IPDtargetR)/IPDmaxmin
                muILD = np.abs(ILDtest-ILDtargetR)/ILDmaxmin

            mu = np.concatenate((muIPD,muILD))
            mu[mu>0.95]=0.95;

            G = (1-mu)**drt
            G = G/np.max(G)
            G = np.concatenate((G,G[::-1]))

            sig_fdbm = np.real(scp.ifft(Xbuf*nplib.repmat(G,2,1)))[:,0:WinLen].T*Win

            xbuf[0:FrmShf,:] = xbuf[FrmShf::,:] + sig_fdbm[0:FrmShf,:]
            xbuf[FrmShf::,:] = sig_fdbm[FrmShf::,:]
            data = bytes(np.int16(xbuf[0:FrmShf,:]))
            out.write(data)
            x[0:FrmShf,:] = xi
        else:
            x[FrmShf::,:] = xi*0.6
            data = bytes(np.int16(x[0:FrmShf,:]))
            out.write(data)
            x[0:FrmShf,:] = x[FrmShf::,:]
        
        count += 1


## web app section ##
from flask import Flask, render_template, Response, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
@cross_origin()
def index():
    return "" #render_template('main.html');

@app.route('/switch')
@cross_origin()
def switch():
    global with_FDBM
    if with_FDBM == 0:
        with_FDBM = 1
    else:
        with_FDBM = 0
   
    data={'status':'ok'}
    response = app.response_class(
    response=json.dumps(data),
    status=200,
    mimetype='application/json'
    )
    return response

@app.route('/front')
@cross_origin()
def front():
    global with_FDBM
    with_FDBM = 1
    
    data={'status':'ok'}
    response = app.response_class(
    response=json.dumps(data),
    status=200,
    mimetype='application/json'
    )
    return response

@app.route('/left')
@cross_origin()
def left():
    global with_FDBM
    with_FDBM = 2
    
    data={'status':'ok'}
    response = app.response_class(
    response=json.dumps(data),
    status=200,
    mimetype='application/json'
    )
    return response

@app.route('/right')
@cross_origin()
def right():
    global with_FDBM
    with_FDBM = 3
    
    data={'status':'ok'}
    response = app.response_class(
    response=json.dumps(data),
    status=200,
    mimetype='application/json'
    )
    return response


@app.route('/test_connection')
@cross_origin()
def test_connection():

    data={'status':'ok'}
    response = app.response_class(
    response=json.dumps(data),
    status=200,
    mimetype='application/json'
    )
    return response

threads = []
t = threading.Thread(target=FDBM_process)
threads.append(t)

t.start()
app.run(host= '0.0.0.0')