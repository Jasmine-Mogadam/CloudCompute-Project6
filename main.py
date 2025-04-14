import os
from flask import Flask, request, render_template
from google.cloud import dialogflow_v2 as dialogflow

app = Flask(__name__)

# Load environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("DIALOGFLOW_CREDENTIALS")
PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")

@app.route('/')
def start_menu():
    return '''
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    text-align: center;
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                button {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to the Chatbot</h1>
                <p>Click below to start chatting!</p>
                <button onclick="window.location.href='/chat'">Start Chat</button>
            </div>
        </body>
        </html>
    '''

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return '''
            <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .chat-container {
                        width: 400px;
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                    .chat-box {
                        width: 100%;
                        height: 300px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        padding: 10px;
                        overflow-y: auto;
                        margin-bottom: 10px;
                    }
                    input[type="text"] {
                        width: calc(100% - 80px);
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                    }
                    button {
                        background-color: #007BFF;
                        color: white;
                        border: none;
                        padding: 10px;
                        border-radius: 5px;
                        cursor: pointer;
                    }
                    button:hover {
                        background-color: #0056b3;
                    }
                }
                </style>
            </head>
            <body>
                <div class="chat-container">
                    <div class="chat-box" id="chat-box"></div>
                    <form method="post">
                        <input type="text" name="message" placeholder="Type your message here...">
                        <button type="submit">Send</button>
                    </form>
                </div>
            </body>
            </html>
        '''
    elif request.method == 'POST':
        user_message = request.form.get('message')
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(PROJECT_ID, "unique_session_id")

        text_input = dialogflow.types.TextInput(text=user_message, language_code="en")
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        bot_reply = response.query_result.fulfillment_text

        return f"<div class='chat-box'><p>User: {user_message}</p><p>Bot: {bot_reply}</p></div>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)