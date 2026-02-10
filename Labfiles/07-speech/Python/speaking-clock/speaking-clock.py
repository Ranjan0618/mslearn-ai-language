from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient 
import azure.cognitiveservices.speech as speechsdk

def main():

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        global speech_config

        # Get config settings
        load_dotenv()
        speech_key = os.getenv('KEY')
        speech_region = os.getenv('REGION')

        # Configure speech service
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        print("Speech service configured with region '{}'".format(speech_config.region))
        
        

        # Get spoken input
        command = TranscribeCommand()
        if command.lower() == 'what time is it?':
            TellTime()

    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ''

    # Configure speech recognition
    current_dir = os.getcwd()
    audioFile = current_dir + '/time.wav'
    audio_config = speechsdk.audio.AudioConfig(filename=audioFile)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    


    # Process speech input
    print("Listening...")
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speechsdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        print(speech.reason)
        if speech.reason == speechsdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)
    

    # Return the command
    return command


def TellTime():
    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)
    response_text = "I live in Kloten Switzerland and the current time is {}:{:02d}".format(now.hour,now.minute)
    response_text = "मैं रंजन जैन हूँ। मैं वास्तव में अच्छा इंसान हूँ लेकिन मेरी पत्नी इससे सहमत नहीं हैं। कृपया मुझे बताएं कि मुझे क्या करना चाहिए? मुझे कहाँ जाना चाहिए? क्या आपके पास कोई रास्ता या संकेत हैं जो मेरी मदद कर सकते हैं?"
    # Configure speech synthesis
    output_file = "output.wav"
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    speech_config.speech_synthesis_voice_name = "hi-IN-SwaraNeural"
    speech_config.speech_synthesis_voice_name = "hi-IN-MadhurNeural"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    

    # Synthesize spoken output
    print("Speaking...")
    speak = speech_synthesizer.speak_text_async(response_text).get()
    if speak.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    else:
        print("Spoken output saved in " + output_file)
        print(speak.reason)


    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()