# ServerTest

### Developers
YuHyun7, brain1219

### Opportunity
Create and run server for CatAndDog prediction model

### Libraries
Django, Rest_Framework, widget_tweaks, for django server<br/>
pytorch, torchvision, pillow, numpy, pandas, for cat and dog prediction model
 
### API list
get_Recent_predict_restlt_api = 'http://127.0.0.1:8000/cat_and_dogs/'<br/>
post_image_api = 'http://127.0.0.1:8000/blog/catdogapi/'

to upload image to the server, you need to encrypt the image with base64
```python

def get_recent_predict_result():
    data = (requests.get(get_Recent_predict_restlt_api)).json()
    print(data[len(data)-1])

def post_image(image_file):
    with open(image_file, "rb") as f:
        im_bytes =f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf-8")

    headers = {'Content-type': 'application/json'}

    payload = json.dumps({"check_image":im_b64, "file_name":image_file})
    response = requests.post(post_image_api, data=payload, headers=headers)
    try:
        data = response.json()
        print(data)
    except :
        print(response.text)
        
print('Upload Cat image')
post_image('cat.jpg')
print('done')
print('Upload Dog Image')
post_image('dog.jpg')
print('done')
```
