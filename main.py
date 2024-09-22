from pymongo import MongoClient
from bson import ObjectId
import sys

while True:
    clusterPassword = str(input('\nDigite a senha do cluster ou SAIR para finalizar:\n>> '))

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

        keyMapping = {
            'title': 'Título',
            'author': 'Autor(a)',
            'genre': 'Gênero',
            'year': 'Ano de Publicação',
            'ISBN': 'ISBN',
            'quantity': 'Quantidade em Estoque'
        }
        # Arrumar id no search books
        print('\n')
        for document in documents:
            print(document['_id'])
            for key, friendlyName in keyMapping.items():
                value = document.get(key, 'Informação não disponível')        
                print(f'{friendlyName} : {value}')
            print('--------\n')
    else:
        print('\nNenhum livro cadastrado.')

def searchBookBy(key, value):
    return collectionBooks.find_one({key: value})

def removeBookBy(removeBy, removeBook):
    if (removeBook):    
        userConfirm = str(input(f'\nDigite CONFIRMAR para remover este livro:\n, {removeBook}\n>> '))

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

def insertUser(userInfo):
    for info in userInfo:
        if info == '':
            print('Nenhum dos campos pode ser vazio')
            return
        
    documentUser = {
        'name': userInfo[0],
        'email': userInfo[1],
        'birth_date': userInfo[2],
        'cpf': userInfo[3]
    }
    
    collectionUsers.insert_one(documentUser)
    print('\nUsuario cadastrado com sucesso!')

def searchUserBy(key, value):
    return collectionUsers.find_one({key: value})

def removeUserBy(removeBy, removeUser):
    if (removeUser):    
        userConfirm = str(input(f'\nDigite CONFIRMAR para remover este usuario:\n, {removeUser}\n>> '))

        if userConfirm.lower() == 'confirmar':
            try:
                collectionUsers.delete_one({removeBy: removeUser[removeBy]})
                print('\nUsuario removido com sucesso')

            except:
                print('\nAlgo deu errado...')
        
        else:
            print('\nRemoção cancelada.')
        
    else:
        print('Usuario não encontrado')

def searchUserAll():
    if (collectionUsers.count_documents({}) > 0):
        documents = collectionUsers.find()

        print('\n')
        for document in documents:
            print(document['_id'])
            for key, value in document.items():
                print(f'{key} : {value}')
            print('--------\n')
    else:
        print('\nNenhum usuario cadastrado.')
    

while True:
    userRequest = str(input("\nO quê deseja consultar?\n1 - Livros\n2 - Usuários\n3 - Empréstimos\n4 - Sair\n\n>> "))
    
    if (userRequest == '1') or (userRequest.lower() == 'livros'):
        while True:
            userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar todos os livros\n2 - Adicionar livro\n3 - Remover livro\n4 - Voltar\n\n>> '))

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
                    userRemoveBy = str(input('Deseja remover por qual idenficador?\n1 - Título\n2 - ISBN\n3 - Id\n>> '))

                    if (userRemoveBy == '1') or (userRemoveBy.lower() == 'título'):
                        userRemoveName = str(input('Título do livro:\n>> '))
                        removeBook = searchBookBy('title', userRemoveName)

                        removeBookBy('_id', removeBook)
                    
                    elif (userRemoveBy == '2') or (userRemoveBy.lower() == 'isbn'):
                        userRemoveISBN = str(input('ISBN do livro:\n>> '))
                        
                        try:
                            removeBook = searchBookBy('ISBN', userRemoveISBN)
                            removeBookBy('ISBN', removeBook)

                        except Exception as e:
                            print(f'ISBN inválido: {e}')

                    elif (userRemoveBy == '3') or (userRemoveBy.lower() == 'id'):
                        userRemoveId = str(input('Id do livro\n>> '))

                        try:
                            removeBook = searchBookBy('_id', ObjectId(userRemoveId))
                            removeBookBy('_id', removeBook)

                        except Exception as e:
                            print(f'Id inválido: {e}')

                    else:
                        print('\nOpção inválida\n')

            elif (userRequest == '4') or (userRequest.lower() == 'voltar'):
                break

            else:
                print('\nOpção inválida\n')

    elif (userRequest == '2') or (userRequest.lower() == 'usuários'):
        userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar todos os usuários\n2 - Voltar\n\n>> '))

        if (userRequest == '1') or (userRequest.lower() == 'consultar'):
            pass

        elif (userRequest == '2') or (userRequest.lower() == 'voltar'):
            pass

        else:
            print('\nOpção inválida\n')

    elif (userRequest == '3') or (userRequest.lower() == 'empréstimos'):
        print('\nEm desenvolvimento...\n')

    elif (userRequest == '4') or (userRequest.lower() == 'sair'):
        print('\nAté logo!')
        break

    else:
        print('\nOpção inválida\n')
