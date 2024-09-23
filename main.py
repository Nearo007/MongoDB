from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import os
import sys

load_dotenv()
clusterPassword = os.getenv('CLUSTER_PASSWORD')
try:
    client = MongoClient(f'mongodb+srv://Nearo:{clusterPassword}@cluster0.kcsg9.mongodb.net/')
    db_list = client.list_database_names()
    print("\nConexão bem-sucedida!")

except:
    print("\nErro de conexão: Verifique se a senha e o URI estão corretos.")
    sys.exit()

db = client['LibraryManager']

collectionBooks = db['books']
collectionUsers = db['users']
collectionLoans = db['loans']

def insertBook():
    while True:
        try:
            userTitle = str(input('\nDigite o título do livro: '))
            userAuthor = str(input('Digite o autor do livro: '))
            userGenre = str(input('Digite o gênero do livro: '))
            userYear = int(input('Digite o ano de publicação: '))
            userISBN = str(input('Digite o ISBN do livro: '))
            userQuantity = int(input('Digite a quantidade de exemplares disponíveis: '))
            break
        
        except:
            print('\nAlgum dos valores digitados é inválido, tente novamente.')
    
    bookInfo = [userTitle, userAuthor, userGenre, userYear, userISBN, userQuantity]
                
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

def searchBookBy(key, value):
    return collectionBooks.find_one({key: value})

def searchBooksAll():
    if (collectionBooks.count_documents({}) > 0):
        documents = collectionBooks.find()

        keyMapping = {
            '_id': 'ID',
            'title': 'Título',
            'author': 'Autor(a)',
            'genre': 'Gênero',
            'year': 'Ano de Publicação',
            'ISBN': 'ISBN',
            'quantity': 'Quantidade em Estoque'
        }
        print('\n')
        for document in documents:
            for databaseName, friendlyName in keyMapping.items():
                bookValue = document.get(databaseName, 'Informação não disponível')
                print(f'{friendlyName} : {bookValue}')
            print('--------\n')
    else:
        print('\nNenhum livro cadastrado.')

def updateBookBy(updateBy, updateBook):
    if (updateBook):
        userConfirm = str(input(f'\nDigite CONFIRMAR para atualizar este livro:\n, {updateBook}\n>> '))

        if userConfirm.lower() == 'confirmar':
            try:
                dataType = type(updateBook[updateBy])
                updateBook[updateBy] = dataType(input('Digite o novo valor: '))

            except ValueError:
                print('\nErro de conversão. Verifique o dado inserido e tente novamente.')

            except Exception as e:
                print(f'\nAlgo deu errado: {str(e)}')

def removeBookBy(removeBy, removeBook):
    if (removeBook):    
        userConfirm = str(input(f'\nDigite CONFIRMAR para remover este livro:\n, {removeBook}\n>> '))

        if userConfirm.lower() == 'confirmar':
            try:
                collectionBooks.delete_one({removeBy: removeBook[removeBy]})
                print('\nLivro removido com sucesso')

            except:
                print(f'\nAlgo deu errado: {str(e)}')
        
        else:
            print('\nRemoção cancelada.')
        
    else:
        print('\nLivro não encontrado')

def insertUser():
    while True:
        try:
            userName = str(input('\nDigite o nome do usuário: '))
            userEmail = str(input('Digite o E-mail : '))

            userDate = str(input('Digite a data de nascimento (DD-MM-AAAA) ou (DD/MM/AAAA): '))
            userDate = userDate.replace('/', '-')

            userBirth = datetime.strptime(userDate, '%d-%m-%Y')
            userCPF = str(input('Digite o CPF do usuário: '))
            break

        except:
            print('\nAlgum dos valores digitados é inválido, tente novamente.')

    userInfo = [userName, userEmail, userBirth, userCPF]

    for info in userInfo:
        if info == '':
            print('Nenhum dos campos pode ser vazio')
            return
        
    documentUser = {
        'name': userInfo[0],
        'email': userInfo[1],
        'birth_date': userInfo[2],
        'CPF': userInfo[3]
    }
    
    collectionUsers.insert_one(documentUser)
    print('\nUsuario cadastrado com sucesso!')

def searchUserBy(key, value):
    return collectionUsers.find_one({key: value})

def searchUserAll():
    if (collectionUsers.count_documents({}) > 0):
        documents = collectionUsers.find()

        keyMapping = {
            '_id': 'Id',
            'name': 'Nome',
            'email': 'E-mail',
            'birth_date': 'Data de Nascimento',
            'CPF': 'CPF'
        }

        for document in documents:
            for databaseName, friendlyName in keyMapping.items():
                userValue = document.get(databaseName, 'Informação não disponível')
                print(f'{friendlyName} : {userValue}')
            print('--------\n')
    else:
        print('\nNenhum usuario cadastrado.')

def updateUserBy(updateBy, updateUser):
    if (updateUser):
        userConfirm = str(input(f'\nDigite CONFIRMAR para atualizar este usuário:\n, {updateUser}\n>> '))

        if userConfirm.lower() == 'confirmar':
            try:
                dataType = type(updateUser[updateBy])
                updateUser[updateBy] = dataType(input('Digite o novo valor: '))

            except ValueError:
                print('\nErro de conversão. Verifique o dado inserido e tente novamente.')

            except Exception as e:
                print(f'\nAlgo deu errado: {str(e)}')

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
        print('\nUsuario não encontrado')
    
def insertLoan():
    pass

def searchLoanBy(key, value):
    pass

def searchLoanAll():
    pass

def updateLoanBy(updateBy, updateLoan):
    pass

def removeLoanBy(removeBy, removeLoan):
    pass

while True:
    userRequest = str(input("\nO quê deseja consultar?\n1 - Livros\n2 - Usuários\n3 - Empréstimos\n4 - Sair\n\n>> "))
    
    if (userRequest == '1') or (userRequest.lower() == 'livros'):
        while True:
            userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar todos os livros\n2 - Adicionar livro\n3 - Remover livro\n4 - Voltar\n\n>> '))

            if (userRequest == '1') or (userRequest.lower() == 'consultar'):
                searchBooksAll()

            elif (userRequest == '2') or (userRequest.lower() == 'adicionar'):
                insertBook()

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
        while True:
            userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar todos os usuários\n2 - Adicionar usuário\n3 - Remover usuário\n4 - Voltar\n\n>> '))

            if (userRequest == '1') or (userRequest.lower() == 'consultar'):
                searchUserAll()

            elif (userRequest == '2') or (userRequest.lower() == 'adicionar'):
                insertUser()

            elif (userRequest == '3') or (userRequest.lower() == 'remover'):
                userRemoveBy = str(input('Deseja remover por qual idenficador?\n1 - Nome\n2 - Email\n3 - CPF\n4 - Id\n>> '))

                if (userRemoveBy == '1') or (userRemoveBy.lower() == 'nome'):
                    userRemoveName = str(input('Nome do usuário:\n>> '))
                    removeUser = searchUserBy('name', userRemoveName)

                    removeUserBy('name', removeUser)

                elif (userRemoveBy == '2') or (userRemoveBy.lower() == 'email'):
                    userRemoveEmail = str(input('Email do usuário:\n>> '))
                    removeUser = searchUserBy('email', userRemoveEmail)

                    removeUserBy('email', removeUser)

                elif (userRemoveBy == '3') or (userRemoveBy.lower() == 'cpf'):
                    userRemoveCPF = str(input('CPF do usuário:\n>> '))
                    removeUser = searchUserBy('CPF', userRemoveCPF)

                    removeUserBy('CPF', removeUser)

                elif (userRemoveBy == '4') or (userRemoveBy.lower() == 'id'):
                    userRemoveId = str(input('Id do usuário\n>> '))
                    removeUser = searchUserBy('_id', ObjectId(userRemoveId))

                    removeUserBy('_id', removeUser)

                else:
                    print('\nOpção inválida\n')

            elif (userRequest == '4') or (userRequest.lower() == 'voltar'):
                break

            else:
                print('\nOpção inválida\n')

    elif (userRequest == '3') or (userRequest.lower() == 'empréstimos'):
        while True:
            userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar todos os empréstimos\n2 - Adicionar empréstimo\n3 - Remover empréstimo\n4 - Voltar\n\n>> '))

            if (userRequest == '1') or (userRequest.lower() == 'consultar'):
                searchLoanAll()

            elif (userRequest == '2') or (userRequest.lower() == 'adicionar'):
                insertLoan()

            elif (userRequest == '3') or (userRequest.lower() == 'remover'):
                removeLoanBy()

            elif (userRequest == '4') or (userRequest.lower() == 'voltar'):
                break

    elif (userRequest == '4') or (userRequest.lower() == 'sair'):
        print('\nAté logo!')
        break

    else:
        print('\nOpção inválida\n')
