
    ## uses the vision api from google for ocr. it's fairly fast, very accurate.
import base64, cStringIO, requests
url = "https://vision.googleapis.com/v1/images:annotate?key=

def request_body(image):
    return {
        "requests" : [{
            "image": image_obj(image),
            "features": [{"type": "TEXT_DETECTION"}]
        }]
    }

def image_obj(contents):
    bufferr = cStringIO.StringIO()
    contents.save(bufferr, format='JPEG')
    return { "content": base64.b64encode(bufferr.getvalue()) }


def make_recognition(image, key):
    req = requests.post(url+key, json=request_body(image))
    return req.json()["responses"][0]["textAnnotations"][0]["description"]
