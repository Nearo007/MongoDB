from pymongo import MongoClient
from bson import ObjectId
import sys

while True:
    clusterPassword = str(input('\nDigite a senha do cluster ou SAIR para finalizar:\n>>'))

    if (clusterPassword.lower() != 'sair'):
        try:
            client = MongoClient(f'mongodb+srv://Nearo:{clusterPassword}@cluster0.kcsg9.mongodb.net/')
            
            db_list = client.list_database_names()

            print("\nConexão bem-sucedida!")
            break
        except:
            print("\nErro de conexão: Verifique se a senha e o URI estão corretos.")
    else:
        sys.exit()

db = client['LibraryManager']

collectionBooks = db['books']
collectionUsers = db['users']

def insertBook(bookInfo):
    #bookInfo = [userTitle, userAuthor, userGenre, userYear, userISBN, userQuantity]
    for info in bookInfo:
        if info == '':
            print('Nenhum dos campos pode ser vazio')
            return
        
    documentBook = {
        'title': bookInfo[0],
        'author': bookInfo[1],
        'genre': bookInfo[2],
        'year': bookInfo[3],
        'ISBN': bookInfo[4],
        'quantity': bookInfo[5]
    }

    collectionBooks.insert_one(documentBook)
    print('\nLivro cadastrado com sucesso!')

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
        userTitle = str(input('\nDigite o título do livro: '))
        userAuthor = str(input('Digite o autor do livro: '))
        userGenre = str(input('Digite o gênero do livro: '))
        userYear = str(input('Digite o ano de publicação: '))
        userISBN = str(input('Digite o ISBN do livro: '))
        userQuantity = str(input('Digite a quantidade de exemplares disponíveis: '))
        
        insertBook([userTitle, userAuthor, userGenre, userYear, userISBN, userQuantity])

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