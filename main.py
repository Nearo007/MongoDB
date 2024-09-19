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

def searchBookBy(key, value):
    return collectionBooks.find_one({key: value})

def removeBookBy(removeBook, removeBy):
    if (removeBook):    
        userConfirm = str(input(f'\nDigite CONFIRMAR para remover este livro:\n, {removeBook}\n>>'))

        if userConfirm.lower() == 'confirmar':
            try:
                collectionBooks.delete_one({removeBy: removeBook[removeBy]})
                print('\nLivro removido com sucesso')

            except:
                print('\nAlgo deu errado...')
        
    else:
        print('Livro não encontrado')
    

while True:
    userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar livro\n2 - Adicionar livros\n3 - Remover livro\n10 - Sair\n>>'))

    if (userRequest == '1') or (userRequest.lower() == 'consultar'):
        searchAll(collectionBooks)

    elif (userRequest == '2') or (userRequest.lower() == 'adicionar'):
        
        userName = str(input('Digite o título do livro: '))
        userGenre = str(input('Digite o gênero do livro: '))

        documentBook = {
            'title': userName,
            'genre': userGenre,
            'rented': 0
        }
        
        insertDocument(collectionBooks, documentBook)
        
        print('acho que deu certo')

    elif (userRequest == '3') or (userRequest.lower() == 'remover'):
            userRemoveBy = str(input('Deseja remover por qual idenficador?\n1 - Título\n2 - Gênero\n3 - ID\n>>'))

            if (userRemoveBy == '1') or (userRemoveBy.lower() == 'título'):
                userRemoveName = str(input('Título do livro:\n>>'))
                removeBook = searchBookBy('name', userRemoveName)

                removeBookBy(removeBook, '_id')

    elif (userRequest == '10') or (userRequest.lower() == 'sair'):
        print('\nAté logo!')
        break

    else:
        print('\nOpção inválida\n')