from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
#from chatterbot.comparisons import jaccard_similarity
#from chatterbot.comparisons import levenshtein_distance
from data import faq, shortcuts


chatbot = ChatBot(
    'Penny',
    read_only=True,
    preprocessors=['chatterbot.preprocessors.clean_whitespace'],
    #statement_comparison_function=jaccard_similarity, #levenshtein_distance
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.60
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)


trainer = ListTrainer(chatbot)

trainer.train(faq)
trainer.train(shortcuts)


exit_conditions = (":q", "quit", "exit")

while True:

    query = input("> ")

    if query in exit_conditions:

        break

    else:

        print(f"[P] {chatbot.get_response(query)}")
