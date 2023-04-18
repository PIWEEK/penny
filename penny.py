from chatterbot import ChatBot
from chatterbot.comparisons import JaccardSimilarity, LevenshteinDistance
from chatterbot.trainers import ChatterBotCorpusTrainer




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


corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train('data/greetings.yml')
corpus_trainer.train('data/faq.yml')
corpus_trainer.train('data/shortcuts.yml')
corpus_trainer.train('data/user_guide.yml')


exit_conditions = (":q", "quit", "exit")

while True:

    query = input("> ")

    if query in exit_conditions:

        break

    else:

        print(f"[P] {chatbot.get_response(query)}")
