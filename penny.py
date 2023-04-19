from chatterbot import ChatBot
from chatterbot.comparisons import JaccardSimilarity, LevenshteinDistance
from chatterbot.trainers import ChatterBotCorpusTrainer

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import sys


def init_chatbot():
    chatbot = ChatBot(
        'Penny',
        read_only=True,
        preprocessors=['chatterbot.preprocessors.clean_whitespace'],
        statement_comparison_function=JaccardSimilarity,
        #statement_comparison_function=LevenshteinDistance,
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, but I do not understand.',
                'maximum_similarity_threshold': 0.8
            }
        ],
        database_uri='sqlite:///database.sqlite3'
    )
    return chatbot

def train_chatbot(chatbot):
    corpus_trainer = ChatterBotCorpusTrainer(chatbot)
    corpus_trainer.train('data/greetings.yml')
    corpus_trainer.train('data/faq.yml')
    corpus_trainer.train('data/shortcuts.yml')
    corpus_trainer.train('data/user_guide.yml')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
chatbot = init_chatbot()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    response = str(chatbot.get_response(message))
    emit('response', '[Penny]: ' + response, broadcast=True)

def main(argv):
    
    print (argv)
    if len(argv) == 1 and argv[0] == 'train':
        train_chatbot(chatbot)
        print("Chatbot trained!")
        exit(0)
    else:
        socketio.run(app, debug=True)


if __name__ == "__main__":
   main(sys.argv[1:])
