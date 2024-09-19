from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb+srv://Nearo:aracnidea@cluster0.kcsg9.mongodb.net/') # Alterar o link com a senha depois

db = client['LibraryManager']

collectionBooks = db['books']

def insertBook(book):
    collectionBooks.insert_one(book)

def searchBooksAll():
    if (collectionBooks.count_documents({}) > 0):
        documents = collectionBooks.find()
        
        for document in documents:
            print('\n')
            print(document)

    else:
        print('\nNenhum livro cadastrado.')

def searchBookBy(key, value):
    return collectionBooks.find_one({key: value})

def removeBookBy(removeBy, removeBook):
    if (removeBook):    
        userConfirm = str(input(f'\nDigite CONFIRMAR para remover este livro:\n, {removeBook}\n>>'))

        if userConfirm.lower() == 'confirmar':
            try:
                collectionBooks.delete_one({removeBy: removeBook[removeBy]})
                print('\nLivro removido com sucesso')

            except:
                print('\nAlgo deu errado...')
        
        else:
            print('\nRemoção cancelada.')
        
    else:
        print('Livro não encontrado')
    

while True:
    userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar todos os livros\n2 - Adicionar livro\n3 - Remover livro\n10 - Sair\n>>'))

    if (userRequest == '1') or (userRequest.lower() == 'consultar'):
        searchBooksAll()

    elif (userRequest == '2') or (userRequest.lower() == 'adicionar'):
        
        userName = str(input('Digite o título do livro: '))
        userGenre = str(input('Digite o gênero do livro: '))

        documentBook = {
            'title': userName,
            'genre': userGenre,
            'rented': 0
        }
        
        insertBook(documentBook)

    elif (userRequest == '3') or (userRequest.lower() == 'remover'):
            userRemoveBy = str(input('Deseja remover por qual idenficador?\n1 - Título\n2 - Id\n>>'))

            if (userRemoveBy == '1') or (userRemoveBy.lower() == 'título'):
                userRemoveName = str(input('Título do livro:\n>>'))
                removeBook = searchBookBy('title', userRemoveName)

                removeBookBy('_id', removeBook)

            elif (userRemoveBy == '2') or (userRemoveBy.lower() == 'id'):
                userRemoveId = str(input('Id do livro\n>>'))

                try:
                    removeBook = searchBookBy('_id', ObjectId(userRemoveId))
                    removeBookBy('_id', removeBook)

                except Exception as e:
                    print(f'Id inválido: {e}')

    elif (userRequest == '10') or (userRequest.lower() == 'sair'):
        print('\nAté logo!')
        break

    else:
        print('\nOpção inválida\n')