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

def updateCollection(database, updateDocument, databaseName, userNewInfo, friendlyName):
    resultado = database.update_one(
        {databaseName: updateDocument[databaseName]},
        {'$set': {databaseName: userNewInfo}}
    )

    if resultado.modified_count > 0:
        print(f"\n{friendlyName} atualizado com sucesso")
    
    else:
        if friendlyName.isupper():
            print(f"\nNenhum {friendlyName} encontrado")
        
        else:
            print(f"\nNenhum {friendlyName.lower()} encontrado")

def insertBook():
    try:
        userTitle = str(input('\nDigite o título do livro: '))
        userAuthor = str(input('Digite o autor do livro: '))
        userGenre = str(input('Digite o gênero do livro: '))
        userYear = int(input('Digite o ano de publicação: '))

        if userYear > datetime.now().year:
            raise ValueError
        
        elif userYear < 0:
            raise ValueError
        
        userISBN = str(input('Digite o ISBN do livro: '))

        if (collectionBooks.count_documents({'ISBN': userISBN}) > 0):
            raise ValueError('Este livro já está cadastrado no sistema')

        userQuantity = int(input('Digite a quantidade de exemplares disponíveis: '))
    
    except:
        print('\nAlgum dos valores digitados é inválido, tente novamente.')
        return
    
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

def searchBookBy():
    userSearchBy = str(input('\nDeseja pesquisar o livro por qual idenficador?\n1 - Título\n2 - ISBN\n3 - Id\n\nDeixe em branco para cancelar:\n>> '))
    if (userSearchBy == '1') or (userSearchBy.lower() == 'título'):
        userSearchTitle = str(input('Título do livro:\n>> '))

        searchBook = collectionBooks.find_one({'title': userSearchTitle})

    elif (userSearchBy == '2') or (userSearchBy.lower() == 'isbn'):
        userSearchISBN = str(input('ISBN do livro:\n>> '))

        searchBook = collectionBooks.find_one({'ISBN': userSearchISBN})

    elif (userSearchBy == '3') or (userSearchBy.lower() == 'id'):
        userSearchId = str(input('Id do livro:\n>> '))

        try:
            searchBook = collectionBooks.find_one({'_id': ObjectId(userSearchId)})

        except:
            print('\nId inválido')
            searchBook = None

    elif userSearchBy.strip() == '':
        searchBook = None
        return searchBook

    else:
        print('\nOpção inválida')
        searchBook = None
        return searchBook

    if not searchBook:
        print('\nLivro não encontrado')
        searchBook = None
        
    return searchBook

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

def updateBookBy(updateBook):
    if (updateBook):
            print(f'\n{updateBook}') 

            userUpdateBy = str(input('\nDeseja atualizar qual informação?\n1 - Título\n2 - Autor\n3 - Gênero\n4 - Data de publicação\n5 - ISBN\n6 - Quantidade\n>> '))

            try:
                if (userUpdateBy == '1') or (userUpdateBy.lower() == 'título'):
                    userNewInfo = str(input('Digite o novo título: '))
                    updateCollection(collectionBooks, updateBook, 'title', userNewInfo, 'Título')

                elif (userUpdateBy == '2') or (userUpdateBy.lower() == 'autor'):
                    userNewInfo = str(input('Digite o novo autor: '))
                    updateCollection(collectionBooks, updateBook, 'author', userNewInfo, 'Autor(a)')

                elif (userUpdateBy == '3') or (userUpdateBy.lower() == 'gênero'):
                    userNewInfo = str(input('Digite o novo gênero: '))
                    updateCollection(collectionBooks, updateBook, 'genre', userNewInfo, 'Gênero')

                elif (userUpdateBy == '4') or (userUpdateBy.lower() == 'data'):
                    userNewInfo = int(input('Digite a novo ano (AAAA): '))

                    if userNewInfo > datetime.now().year:
                        raise ValueError
                    
                    elif userNewInfo < 0:
                        raise ValueError

                    updateCollection(collectionBooks, updateBook, 'year', userNewInfo, 'Ano de Publicação')

                elif (userUpdateBy == '5') or (userUpdateBy.lower() == 'isbn'):
                    userNewInfo = str(input('Digite o novo ISBN: '))

                    if (collectionBooks.count_documents({'ISBN': userNewInfo}) > 0):
                        raise ValueError('ISBN ja existente')

                    updateCollection(collectionBooks, updateBook, 'ISBN', userNewInfo, 'ISBN')

                elif (userUpdateBy == '6') or (userUpdateBy.lower() == 'quantidade'):
                    userNewInfo = int(input('Digite a nova quantidade: '))
                    updateCollection(collectionBooks, updateBook, 'quantity', userNewInfo, 'Quantidade em Estoque')

            except Exception as e:
                print(f'\nAlgo deu errado: {str(e)}')

def removeBookBy(removeBook):
    if (removeBook):    
        userConfirm = str(input(f'\nDigite CONFIRMAR para remover este livro:\n, {removeBook}\n>> '))

        if userConfirm.lower() == 'confirmar':
            try:
                collectionBooks.delete_one({'_id': removeBook['_id']})
                print('\nLivro removido com sucesso')

            except Exception as e:
                print(f'\nAlgo deu errado: {str(e)}')
        
        else:
            print('\nRemoção cancelada.')

def insertUser():
    try:
        userName = str(input('\nDigite o nome do usuário: '))
        userEmail = str(input('Digite o E-mail : '))

        userDate = str(input('Digite a data de nascimento (DD-MM-AAAA) ou (DD/MM/AAAA): '))
        userDate = userDate.replace('/', '-')

        userBirth = datetime.strptime(userDate, '%d-%m-%Y')
        
        userCPF = str(input('Digite o CPF do usuário: '))
        userCPFcheck = userCPF.replace('.', '')
        userCPFcheck = userCPFcheck.replace('-', '')

        if (collectionUsers.count_documents({'CPF': userCPF}) > 0):
            raise ValueError('CPF ja existente')

        if len(userCPFcheck) != 11:
            raise ValueError('CPF inválido')

    except Exception as e:
        print(f'\nAlgo deu errado: {str(e)}')
        return

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

def searchUserBy():
    userSearchBy = str(input('\nDeseja pesquisar o usuário por qual idenficador?\n1 - Nome\n2 - Email\n3 - CPF\n4 - Id\n>> '))

    if (userSearchBy == '1') or (userSearchBy.lower() == 'nome'):
        userSearchName = str(input('Nome do usuário:\n>> '))

        searchUser = collectionUsers.find_one({'name': userSearchName})

    elif (userSearchBy == '2') or (userSearchBy.lower() == 'email'):
        userSearchEmail = str(input('Email do usuário:\n>> '))

        searchUser = collectionUsers.find_one({'email': userSearchEmail})

    elif (userSearchBy == '3') or (userSearchBy.lower() == 'cpf'):
        userSearchCPF = str(input('CPF do usuário:\n>> '))

        searchUser = collectionUsers.find_one({'CPF': userSearchCPF})

    elif (userSearchBy == '4') or (userSearchBy.lower() == 'id'):
        userSearchId = str(input('Id do livro:\n>> '))

        try:
            searchUser = collectionUsers.find_one({'_id': ObjectId(userSearchId)})

        except:
            print('\nId inválido')
            searchUser = None

    else:
        print('\nOpção inválida')
        searchUser = None
        return

    if not searchUser:
        print('\nUsuario não encontrado')
        searchUser = None
        
    return searchUser


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

def updateUserBy(updateUser):
    if (updateUser):
        print(updateUser)

        userUpdateBy = str(input('\nDeseja atualizar qual informação?\n1 - Nome\n2 - E-mail\n3 - Data de nascimento\n4 - CPF\n>> '))

        try:
            if (userUpdateBy == '1') or (userUpdateBy.lower() == 'nome'):
                userNewInfo = str(input('Digite o novo nome: '))
                updateCollection(collectionUsers, updateUser, 'name', userNewInfo, 'Nome')

            elif (userUpdateBy == '2') or (userUpdateBy.lower() == 'email'):
                userNewInfo = str(input('Digite o novo e-mail: '))
                updateCollection(collectionUsers, updateUser, 'email', userNewInfo, 'E-mail')

            elif (userUpdateBy == '3') or (userUpdateBy.lower() == 'data de nascimento'):
                userDate = str(input('Digite a nova data de nascimento (DD-MM-AAAA) ou (DD/MM/AAAA): '))
                userDate = userDate.replace('/', '-')
                userNewInfo = datetime.strptime(userDate, '%d-%m-%Y')

                if userNewInfo > datetime.now():
                    raise ValueError
                
                elif userNewInfo < datetime.min:
                    raise ValueError
            
                updateCollection(collectionUsers, updateUser, 'birth_date', userNewInfo, 'Data de Nascimento')

            elif (userUpdateBy == '4') or (userUpdateBy.lower() == 'cpf'):
                userNewInfo = str(input('Digite o novo CPF: '))
                userCPFcheck = userNewInfo.replace('.', '')
                userCPFcheck = userNewInfo.replace('-', '')

                if (collectionUsers.count_documents({'CPF': userNewInfo}) > 0):
                    raise ValueError('Este CPF está sendo usado por outro usuário')

                if len(userCPFcheck) != 11:
                    raise ValueError('CPF inválido')

                updateCollection(collectionUsers, updateUser, 'CPF', userNewInfo, 'CPF')

            else:
                raise ValueError
        
        except Exception as e:
            print(f'\nAlgo deu errado: {str(e)}')

def removeUserBy(removeUser):
    if (removeUser):    
        userConfirm = str(input(f'\nDigite CONFIRMAR para remover este usuario:\n, {removeUser}\n>> '))

        if userConfirm.lower() == 'confirmar':
            try:
                collectionUsers.delete_one({'_id': removeUser['_id']})
                print('\nUsuario removido com sucesso')

            except Exception as e:
                print(f'\nAlgo deu errado: {e}')
        
        else:
            print('\nRemoção cancelada.')
    
def insertLoan():
    try:
        print('\nInsira os dados do emprestimo:')
        user = searchUserBy()
        print(user)
        loanUserId = user['_id']
        
        book = searchBookBy()
        print(book)
        loanBookId = book['_id']

        loanDate = datetime.now()

    except:
        print('\nAlgum dos valores digitados é inválido, tente novamente.')
        return

    loanInfo = [loanUserId, loanBookId, loanDate]

    for info in loanInfo:
        if info == '':
            print('Nenhum dos campos pode ser vazio')
            return
    
    if (book['quantity'] == 0):
        print('\nLivro indisponível')
        return
    
    book['quantity'] -= 1
    collectionBooks.update_one({'_id': book['_id']}, {'$set': {'quantity': book['quantity']}})

    documentLoan = {
        'user_id': loanInfo[0],
        'book_id': loanInfo[1],
        'loan_date': loanInfo[2]
    }
    
    collectionLoans.insert_one(documentLoan)
    print('\nEmprestimo realizado com sucesso!')

def userSearchLoanBy():
    pass

def searchLoanBy():
    userSearchBy = str(input('\nDeseja pesquisar o emprestimo por qual idenficador?\nDigite o Id do empréstimo\n\n>> '))

    if (userSearchBy == '1') or (userSearchBy.lower() == 'empréstimo'):
        try:
            loanId = str(input('\nDigite o Id do emprestimo: '))
            documentLoan = collectionLoans.find_one({'_id': ObjectId(loanId)})
            return documentLoan
        except:
            print('\nId inválido')

    else:
        print('\nOpção inválida')
        documentLoan = None
        return

def searchLoanAll():
    if (collectionLoans.count_documents({}) > 0):
        documents = collectionLoans.find()

        keyMapping = {
            '_id': 'Id',
            'user_id': 'Id do Usuário',
            'book_id': 'Id do Livro',
            'loan_date': 'Data de Empréstimo',
        }

        for document in documents:
            userId = document['user_id']
            userName = collectionUsers.find_one({'_id': userId})['name']

            bookId = document['book_id']
            bookTitle = collectionBooks.find_one({'_id': bookId})['title']

            for databaseName, friendlyName in keyMapping.items():
                loanValue = document.get(databaseName, 'Informação não disponível')
                print(f'{friendlyName} : {loanValue}')
            print(f'Nome do Usuário : {userName}')
            print(f'Título do Livro : {bookTitle}')
            print('--------\n')
    else:
        print('\nNenhum empréstimo cadastrado.')

def removeLoanBy(removeLoan):
    if (removeLoan):
        loanConfirm = str(input(f'\nDigite CONFIRMAR para remover este empréstimo:\n{removeLoan}\n>> '))

        if loanConfirm.lower() == 'confirmar':
            try:
                bookId = removeLoan['book_id']
                currentQuantity = collectionBooks.find_one({'_id': bookId})['quantity']

                collectionBooks.update_one({'_id': bookId}, {'$set': {'quantity': currentQuantity + 1}})
                collectionLoans.delete_one({'_id': removeLoan['_id']})
                print('\nEmprestimo removido com sucesso')

            except Exception as e:
                print(f'\nAlgo deu errado: {e}')

def main():
    while True:
        try:
            userRequest = str(input("\nO quê deseja consultar?\n1 - Livros\n2 - Usuários\n3 - Empréstimos\n\nDeixe em branco para sair:\n\n>> "))
            
            if (userRequest == '1') or (userRequest.lower() == 'livros'):
                while True:
                    userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar todos os livros\n2 - Adicionar livro\n3 - Atualizar livro\n4 - Remover livro\n\nDeixe em branco para voltar:\n\n>> '))

                    if (userRequest == '1') or (userRequest.lower() == 'consultar'):
                        searchBooksAll()

                    elif (userRequest == '2') or (userRequest.lower() == 'adicionar'):
                        insertBook()

                    elif (userRequest == '3') or (userRequest.lower() == 'atualizar'):
                        updateBook = searchBookBy()
                        updateBookBy(updateBook)

                    elif (userRequest == '4') or (userRequest.lower() == 'remover'):
                        removeBook = searchBookBy()
                        removeBookBy(removeBook)

                    elif (userRequest.strip() == ''):
                        break

                    else:
                        print('\nOpção inválida\n')

            elif (userRequest == '2') or (userRequest.lower() == 'usuários'):
                while True:
                    userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar todos os usuários\n2 - Adicionar usuário\n3 - Atualizar usuário\n4 - Remover usuário\n\nDeixe em branco para voltar:\n\n>> '))

                    if (userRequest == '1') or (userRequest.lower() == 'consultar'):
                        searchUserAll()

                    elif (userRequest == '2') or (userRequest.lower() == 'adicionar'):
                        insertUser()

                    elif (userRequest == '3') or (userRequest.lower() == 'atualizar'):
                        updateUser = searchUserBy()
                        updateUserBy(updateUser)

                    elif (userRequest == '4') or (userRequest.lower() == 'remover'):
                        removeUser = searchUserBy()
                        removeUserBy(removeUser)

                    elif (userRequest.strip() == ''):
                        break

                    else:
                        print('\nOpção inválida\n')

            elif (userRequest == '3') or (userRequest.lower() == 'empréstimos'):
                while True:
                    userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar todos os empréstimos\n2 - Abrir empréstimo\n3 - Encerrar empréstimo\n\nDeixe em branco para voltar:\n\n>> '))

                    if (userRequest == '1') or (userRequest.lower() == 'consultar'):
                        searchLoanAll()

                    elif (userRequest == '2') or (userRequest.lower() == 'abrir'):
                        insertLoan()

                    elif (userRequest == '3') or (userRequest.lower() == 'encerrar'):
                        removeLoan = searchLoanBy()
                        removeLoanBy(removeLoan)

                    elif (userRequest.strip() == ''):
                        break

                    else:
                        print('\nOpção inválida\n')

            elif (userRequest.strip() == ''):
                print('\nAté logo!')
                break

            else:
                print('\nOpção inválida\n')

        except KeyboardInterrupt:
            print('\nAté logo!')
            break

        except Exception as e:
            print(f'\nAlgo deu errado: {e}')

if __name__ == '__main__':
    main()