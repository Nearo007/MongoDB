from pymongo import MongoClient

client = MongoClient('mongodb+srv://Nearo:aracnidea@cluster0.kcsg9.mongodb.net/') # Alterar o link com a senha depois

db = client['LibraryManager']

collectionBooks = db['books']

def insertDocument(collection, document):
    collection.insert_one(document)

def searchAll(collection):
    documents = collection.find()
    
    for document in documents:
        print('\n')
        print(document)
    
    return collection.find() 

while True:
    userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar livro\n2 - Adicionar livros\n4 - Remover livro\n3 - Sair\n>>'))

    if (userRequest == '1') or (userRequest == 'consultar'):
        searchAll(collectionBooks)

    elif (userRequest == '2') or (userRequest.lower() == 'adicionar'):
        
        userName = str(input('Digite o título do livro: '))
        userGenre = str(input('Digite o gênero do livro: '))

        documentBook = {
            'name': userName,
            'genre': userGenre,
            'rented': 0
        }
        
        insertDocument(collectionBooks, documentBook)
        
        print('acho que deu certo')

    elif (userRequest == '3') or (userRequest.lower() == 'sair'):
        print('\nAté logo!')
        break

    elif (userRequest == '4') or (userRequest == 'remover'):
        pass

    else:
        print('\nOpção inválida\n')