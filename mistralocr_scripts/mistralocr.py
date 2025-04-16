import os
from mistralai import Mistral
from dotenv import load_dotenv

ocr = open('zinc.md', 'r', encoding='utf-8').read() # Replace zinc.md with name of the file you want to process

def get_mistral_response(prompt, model="mistral-large-latest"):
    """
    Get a response from the Mistral AI model for the  prompt
    
    Args:
        prompt (str): The prompt to send to the model.
        model (str): The model to use. Default is "mistral-large-latest"
    
    Returns:
        str: The model's response.
    """
    try:
        # Load API key from .env file
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please set the MISTRAL_API_KEY environment variable.")

        # Initialize the Mistral client
        client = Mistral(api_key=api_key)
        
        # Send the prompt to the model
        chat_response = client.chat.complete(
            model=model,
            messages=[
            {
                "role": "user",
                "content": prompt
            }
       ]
    )
       
        # Extract the model's response from the chat response
        return chat_response.choices[0].message.content

    except Exception as e:
           return f"An error occurred: {str(e)}"

def main():
        # Load environment variables from .env file
        load_dotenv()

        # Hardcoded prompt - modify as needed
        prompt = f"""
        Extracted text:
        \n\n
        {ocr}
       \n\n
        List the authors of the research paper, a summary of the abstract and the main findings of the paper: """ # Replace with your own prompt/instructions

        # Model to use
        model = "mistral-large-latest"

        print(f"Sending prompt to Mistral {model}...")

        # Get the response from the model
        response = get_mistral_response(prompt, model)

        # Print the response
        print('\nMistral\'s Response:')
        print("_" * 50)
        print(response)
        print("_" * 50)
        print("End of Mistral's Response")
        print("_" * 50)

if __name__ == "__main__":
    main()
