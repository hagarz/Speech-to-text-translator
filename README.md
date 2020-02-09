# Speech to Text Translator for Client-Server
Client uses **PyAudio** to stream audio to server.  
Server converts audio stream to text using [**GCP Speech-to-Text**](https://cloud.google.com/speech-to-text) and translats it using [**Google Cloud Translation**](https://cloud.google.com/translate).

The software has only been tested in Python3.6.


### Prerequisites
1. Follow the the instructions in [Google Cloud documentation](https://cloud.google.com/docs/authentication/getting-started)
  The JSON file you downloaded the the end of above instructions contains your key, GOOGLE_APPLICATION_CREDENTIALS
2. Copy full  file path (***examle:*** *C:\Users\yourname\Documents\subfoldername\google-app-credentials.json*) to servers code line 20
 
   ***example:***
    > *credential_path = r"C:\Users\yourname\Documents\subfoldername\google-app-credentials.json"*
3. In not run locally, HOST should be '0.0.0.0'.


