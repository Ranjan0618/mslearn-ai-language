import os
import requests
import base64
from dotenv import load_dotenv

# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient



def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        project_endpoint = os.getenv("PROJECT_ENDPOINT")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")

        # Initialize the project client
        project_client = AIProjectClient(endpoint=project_endpoint, credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
          ))      

        # Get a chat client
        
        openai_client = project_client.get_openai_client(api_version="2024-10-21")

        # Initialize prompts
        system_message = "You are an AI assistant for a produce supplier company."
        prompt = ""

        # Loop until the user types 'quit'
        while True:
            prompt = input("\nAsk a question about the audio\n(or type 'quit' to exit)\n")
            if prompt.lower() == "quit":
                break
            elif len(prompt) == 0:
                    print("Please enter a question.\n")
            else:
                print("Getting a response ...\n")

                # Encode the audio file
                file_path = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/avocados.mp3"
                response = requests.get(file_path)
                response.raise_for_status()
                audio_data = base64.b64encode(response.content).decode('utf-8')

                # Get a response to audio input
                
                response = openai_client.chat.completions.create(
                    model=model_deployment,
                    modalities=["text", "audio"],
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt},
                        {"role": "user", "content": audio_data, "modality": "audio"},
                    ],          
                   max_tokens=10, 
                )       
                print("Response:\n")
                print(response.choices[0].message.content)      
                

    except Exception as ex:
        print(ex)


if __name__ == '__main__': 
    main()