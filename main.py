from fastapi import Request, FastAPI, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils import *
import os
from scipy.io import wavfile
import io
import json

app = FastAPI() 
template = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

'''
class trans(BaseModel):
    file: UploadFile
    kind = str
'''

@app.get('/')
async def root(request: Request):
    return template.TemplateResponse('index.html', {"request": request})

@app.post('/transform')
async def transform_audio(file: UploadFile = File(...), kind: str = Form(...)):
    try: 
        binary_data = await file.read() 
        wav_io = io.BytesIO(binary_data)

        rate, audio = wavfile.read(wav_io)
        if kind == 'waveform':
            photo = plot_waveform(rate, audio, "Waveform")
            bmp_photo = bmp_one(photo)
            return JSONResponse(content={"status": "successfully", "photo": photo, "bmp_photo": bmp_photo})
        else:
            photo = plot_frequency_spectrum(rate, audio, "frequency_spectrum")
            bmp_photo = bmp_one(photo)
            return JSONResponse(content={"status": "successfully", "photo": photo, "bmp_photo": bmp_photo})
    except Exception as e:
        return JSONResponse(content={"status": "falied", "message": f"{e}"})
     
@app.post('/compare')
async def compare_audio(file1: UploadFile = File(...), file2: UploadFile = File(...), kind: str = Form(...)):
    try: 
        binary_data1, binary_data2 = await file1.read(), await file2.read() 
        wav_io1, wav_io2 = io.BytesIO(binary_data1), io.BytesIO(binary_data2)

        rate1, audio1= wavfile.read(wav_io1) 
        rate2, audio2= wavfile.read(wav_io2)

        if kind == 'data':
            l = ['0% ~ 0%\n危險程度 : Risk-free', '20% ~ 40%\n危險程度 : Secure', '40% ~ 60%\n危險程度 : Moderate', '60% ~ 80%\n危險程度 : Dangerous', '80% ~ 100%\n危險程度 : Hazardous']
            rate_check = [[0, 20], [21, 40], [41, 60], [61, 80], [81, 100]]
            another, final = compare_two_audio(wav_io1, wav_io2)
            
            for i in range(5):
                if rate_check[i][1] >= float(final) >= rate_check[i][0]:
                    print(f'{another}\n總平均{l[i]}')
                    return JSONResponse(content={"status": "successfully", "result": f'{another}\n總平均{l[i]}'})
        elif kind == 'waveform':
            photo = plot_waveform_compare(audio1, rate1, audio2, rate2, 'aaa')
            bmp_photo = bmp_two(photo)
            return JSONResponse(content={"status": "successfully", "photo": photo, "bmp_photo": bmp_photo})
 
        elif kind == 'spectrogram':
            photo = plot_spectrogram_compare(audio1, rate1, audio2, rate2, 'aaa')
            bmp_photo = bmp_two(photo)
            return JSONResponse(content={"status": "successfully", "photo": photo, "bmp_photo": bmp_photo})
        
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "failed", "message": f'{e}'})

encryption_id = ''
@app.post('/encode')
async def encode_audio(file: UploadFile = File(...)):
    global encryption_id
    try:
        binary_data = await file.read() 
        wav_io = io.BytesIO(binary_data)

        rate, audio = wavfile.read(wav_io)
        encryption_id = generate_encryption_id()
        accelerated_audio = speed_up_audio(audio, 2.0)
        return JSONResponse(content={"status": "successfully", "photo": save_audio(accelerated_audio, rate//2+1), "key": encryption_id})
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "failed", "message": f'{e}'})

@app.post('/decode')
async def decode_audio(file: UploadFile = File(...), psw: str = Form(...)):
    global encryption_id
    try: 
        binary_data = await file.read() 
        wav_io = io.BytesIO(binary_data)

        rate, audio = wavfile.read(wav_io)
        #extracted_id = extract_watermark(audio)

        print(encryption_id)
        if psw == encryption_id:
            audio = remove_watermark(audio)
            return JSONResponse(content={"status": "successfully", "photo": save_audio(audio, rate//2+1)})
        else:
             return JSONResponse(content={"status": "failed", "message": 'input format error'})
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "failed", "message": f'{e}'})