from ollama import Client

try:
    # Create client with the host URL
    client = Client(host="http://localhost:11434")
    
    # List models
    models = client.list()
    print("Available models:", [model for model in models])
    print("Ollama is working correctly.")
except Exception as e:
    print(f"Error connecting to Ollama: {str(e)}")