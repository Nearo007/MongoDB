from pymongo import MongoClient  # Biblioteca para interagir com o MongoDB
from bson import ObjectId  # Para trabalhar com ObjectId do MongoDB
from datetime import datetime  # Para manipulação de datas
from dateutil.relativedelta import relativedelta  # Para calcular intervalos de tempo
from dotenv import load_dotenv  # Carregar variáveis de ambiente de arquivos .env
import os  # Para acessar variáveis de ambiente
import sys  # Para sair do programa em caso de erro

def main():
    load_dotenv()  # Carrega variáveis de ambiente a partir do arquivo .env
    clusterPassword = os.getenv('CLUSTER_PASSWORD')  # Pega a senha do cluster a partir das variáveis de ambiente
    try:  # Tenta conectar ao cluster MongoDB
        client = MongoClient(f'mongodb+srv://Nearo:{clusterPassword}@cluster0.kcsg9.mongodb.net/')
        db_list = client.list_database_names()   # Lista os bancos de dados disponíveis
        print("\nConexão bem-sucedida!")

    except:
        print("\nErro de conexão: Verifique se a senha e o URI estão corretos.")  # Encerra o programa se houver erro de conexão
        sys.exit()

    db = client['LibraryManager']  # Seleciona o banco de dados 'LibraryManager'
    
    # Seleciona as coleções de livros, usuários e empréstimos
    collectionBooks = db['books']
    collectionUsers = db['users']
    collectionLoans = db['loans']

    # Mapeamentos das chaves do banco para nomes mais amigáveis
    bookKeyMapping = {
        '_id': 'ID',
        'title': 'Título',
        'author': 'Autor(a)',
        'genre': 'Gênero',
        'year': 'Ano de Publicação',
        'ISBN': 'ISBN',
        'quantity': 'Quantidade em Estoque'
    }

    userKeyMapping = {
        '_id': 'Id',
        'name': 'Nome',
        'email': 'E-mail',
        'birth_date': 'Data de Nascimento',
        'CPF': 'CPF'
    }

    loanKeyMapping = {
        '_id': 'Id',
        'user_id': 'Id do Usuário',
        'book_id': 'Id do Livro',
        'loan_date': 'Data de Empréstimo',
        'to_return_date': 'Data prevista de Devolução',
    }

    # Função para exibir documentos de forma amigável usando o mapeamento de chaves
    def friendlyPrint(document, keyMapping):
        info = [f'{friendlyName} : {document.get(databaseName, "Informação não disponível")}' 
                for databaseName, friendlyName in keyMapping.items()]
        print("\n".join(info))

    # Função para atualizar um documento de uma coleção
    def updateCollection(database, updateDocument, databaseName, userNewInfo, friendlyName):
        resultado = database.update_one(
            {databaseName: updateDocument[databaseName]},
            {'$set': {databaseName: userNewInfo}}
        )

        # Verifica se o documento foi modificado
        if resultado.modified_count > 0:
            print(f"\n{friendlyName} atualizado com sucesso")
        
        else:
            if friendlyName.isupper():
                print(f"\nNenhum {friendlyName} encontrado")
            
            else:
                print(f"\nNenhum {friendlyName.lower()} encontrado")


    # Funções para inserir, buscar, atualizar e remover livros, usuários e empréstimos
    # O código a seguir implementa essas operações em cada coleção específica
    def insertBook():

        # Pede ao usuário os dados do livro e os insere na coleção
        try:
            userTitle = str(input('\nDigite o título do livro: '))
            userAuthor = str(input('Digite o autor do livro: '))
            userGenre = str(input('Digite o gênero do livro: '))
            userYear = int(input('Digite o ano de publicação: '))

            # Validação do ano de publicação
            if (userYear > datetime.now().year) or (userYear < 0):
                raise ValueError('Ano de publicação inválido')
            
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
            
        # Cria o documento e insere na coleção
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

        # Outras funções seguem o mesmo padrão: inserção, busca, atualização e remoção.
        # Cada uma delas manipula os dados da coleção apropriada e fornece feedback para o usuário.

    def searchBookBy():
        userSearchBy = str(input('\nDeseja pesquisar o livro por qual idenficador?\n1 - Título\n2 - ISBN\n3 - Id\n\nDeixe em branco para cancelar:\n>> '))
        if (userSearchBy == '1') or (userSearchBy.lower() == 'título'):
            userSearchTitle = str(input('\nTítulo do livro:\n>> '))

            searchBook = collectionBooks.find_one({'title': userSearchTitle})

        elif (userSearchBy == '2') or (userSearchBy.lower() == 'isbn'):
            userSearchISBN = str(input('\nISBN do livro:\n>> '))

            searchBook = collectionBooks.find_one({'ISBN': userSearchISBN})

        elif (userSearchBy == '3') or (userSearchBy.lower() == 'id'):
            userSearchId = str(input('\nId do livro:\n>> '))

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

            for document in documents:
                friendlyPrint(document, bookKeyMapping)
                print('--------\n')
        else:
            print('\nNenhum livro cadastrado.')

    def showAvailableBooks():
        if (collectionBooks.count_documents({}) > 0):
            documents = collectionBooks.find()

            print('\n')
            for document in documents:
                if document['quantity'] > 0:
                    friendlyPrint(document, bookKeyMapping)
                    print('--------\n')
        else:
            print('\nNenhum livro cadastrado.')

    def updateBookBy(updateBook):
        if (updateBook):
                print('\n')
                friendlyPrint(updateBook, bookKeyMapping)

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
            print('\n')
            friendlyPrint(removeBook, bookKeyMapping)

            userConfirm = str(input('\nDigite CONFIRMAR para remover o livro acima:\n>> '))

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
            if (collectionUsers.count_documents({'CPF': userCPF}) > 0):
                raise ValueError('CPF ja existente')

            userCPFcheck = userCPF.replace('.', '')
            userCPFcheck = userCPFcheck.replace('-', '')

            if (len(userCPFcheck) != 11) or not (userCPFcheck.isnumeric()):
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
            userSearchName = str(input('\nNome do usuário:\n>> '))

            searchUser = collectionUsers.find_one({'name': userSearchName})

        elif (userSearchBy == '2') or (userSearchBy.lower() == 'email'):
            userSearchEmail = str(input('\nEmail do usuário:\n>> '))

            searchUser = collectionUsers.find_one({'email': userSearchEmail})

        elif (userSearchBy == '3') or (userSearchBy.lower() == 'cpf'):
            userSearchCPF = str(input('\nCPF do usuário:\n>> '))

            searchUser = collectionUsers.find_one({'CPF': userSearchCPF})

        elif (userSearchBy == '4') or (userSearchBy.lower() == 'id'):
            userSearchId = str(input('\nId do usuario:\n>> '))

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

            for document in documents:
                friendlyPrint(document, userKeyMapping)
                print('--------\n')
        else:
            print('\nNenhum usuario cadastrado.')

    def searchUserLoans(user):
        if (user):
            loanDocuments = collectionLoans.find({'user_id': user['_id']})

            print('\n')

            for document in loanDocuments:
                userId = document['user_id']
                userName = collectionUsers.find_one({'_id': userId})['name']

                bookId = document['book_id']
                bookTitle = collectionBooks.find_one({'_id': bookId})['title']

                friendlyPrint(document, loanKeyMapping)
                print(f'Nome do Usuário : {userName}')
                print(f'Título do Livro : {bookTitle}')
                checkLoanPending(document)

                print('--------\n')
            
    def searchUserExpired():
        if (collectionUsers.count_documents({}) > 0):
            loanDocuments = collectionLoans.find({'returned_date': None,'to_return_date': {'$lt': datetime.now()}})
            
            usersSet = set()

            for document in loanDocuments:    
                usersSet.add(document['user_id'])

            if len(usersSet) == 0:
                print('\nNenhum usuario com empréstimo pendente.')
                return
            
            print('\n')
            for userId in usersSet:
                userDocument = collectionUsers.find_one({'_id': userId})
                friendlyPrint(userDocument, userKeyMapping)
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
                    userCPFcheck = userCPFcheck.replace('-', '')

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
            print('\n')
            friendlyPrint(removeUser, userKeyMapping)

            userConfirm = str(input('\nDigite CONFIRMAR para remover o usuario acima:\n>> '))

            if userConfirm.lower() == 'confirmar':
                try:
                    collectionUsers.delete_one({'_id': removeUser['_id']})
                    print('\nUsuario removido com sucesso')

                except Exception as e:
                    print(f'\nAlgo deu errado: {e}')
            
            else:
                print('\nRemoção cancelada.')
        
    def checkLoanPending(loanDocument):
        if (loanDocument['returned_date'] == None) and (loanDocument['to_return_date'] > datetime.now()):
            print(f'O empréstimo está ativo, aguardando devolução. Restam {abs((loanDocument['to_return_date'] - datetime.now()).days)} dias para o prazo de devolução.')
        
        elif (loanDocument['returned_date'] == None) and (loanDocument['to_return_date'] < datetime.now()):
            print(f'O empréstimo expirou e não foi devolvido. {abs((datetime.now() - loanDocument['to_return_date']).days)} dias de atraso.')

        elif (loanDocument['returned_date'] != None) and (loanDocument['to_return_date'] > loanDocument['returned_date']):
            print(f'O empréstimo foi devolvido dentro do prazo. Em {loanDocument['returned_date']}.')

        elif (loanDocument['returned_date'] != None) and (loanDocument['to_return_date'] < loanDocument['returned_date']):
            print(f'O empréstimo foi devolvido fora do prazo. Em {loanDocument['returned_date']}. {abs((loanDocument['returned_date'] - loanDocument['to_return_date']).days)} dias de atraso.')
        
        else:
            print('Houve um erro na busca.')

    def insertLoan():
        try:
            print('\nInsira os dados do emprestimo:')
            user = searchUserBy()
            print(user)
            loanUserId = user['_id']
            
            book = searchBookBy()
            print(book)
            loanBookId = book['_id']

            loanDate = datetime.now().replace(microsecond=0)
            toReturnDate = datetime.now().replace(microsecond=0) + relativedelta(months=1)
            returnedDate = None

        except:
            print('\nAlgum dos valores digitados é inválido, tente novamente.')
            return

        loanInfo = [loanUserId, loanBookId, loanDate, toReturnDate, returnedDate]

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
            'loan_date': loanInfo[2],
            'to_return_date': loanInfo[3],
            'returned_date': loanInfo[4]
        }
        
        collectionLoans.insert_one(documentLoan)
        print('\nEmprestimo realizado com sucesso!')

    def searchLoanByPeriod():
        try:
            print('\nDigite o intervalo de tempo:\n>> ')
            
            fromDate = input('Data inicial (DD-MM-AAAA) ou (DD/MM/AAAA): ')
            fromDate = fromDate.replace('/', '-')
            fromDate = datetime.strptime(fromDate, '%d-%m-%Y')

            toDate = input('Data final (DD-MM-AAAA) ou (DD/MM/AAAA): ')
            toDate = toDate.replace('/', '-')
            toDate = datetime.strptime(toDate, '%d-%m-%Y')

            if fromDate > toDate:
                raise ValueError('Intervalo de tempo inválido')

            documents = collectionLoans.find({})
            
            print('\n')
            for document in documents:
                userId = document['user_id']
                userName = collectionUsers.find_one({'_id': userId})['name']

                bookId = document['book_id']
                bookTitle = collectionBooks.find_one({'_id': bookId})['title']

                loan_date = document['loan_date']
                if fromDate <= loan_date <= toDate:
                    friendlyPrint(document, loanKeyMapping)
                    print(f'Nome do Usuário : {userName}')
                    print(f'Título do Livro : {bookTitle}')
                    checkLoanPending(document)                
                    print('--------\n')
        
        except Exception as e:
            print(f'\nAlgo deu errado: {str(e)}')

    def searchLoanBy():
        try:
            loanId = str(input('\nDigite o Id do emprestimo: '))
            documentLoan = collectionLoans.find_one({'_id': ObjectId(loanId)})
            return documentLoan
        
        except:
            print('\nId inválido')

            documentLoan = None
            return documentLoan

    def searchLoanAll():
        if (collectionLoans.count_documents({}) > 0):
            documents = collectionLoans.find()

            print('\n')
            for document in documents:
                userId = document['user_id']
                userName = collectionUsers.find_one({'_id': userId})['name']

                bookId = document['book_id']
                bookTitle = collectionBooks.find_one({'_id': bookId})['title']

                friendlyPrint(document, loanKeyMapping)
                print(f'Nome do Usuário : {userName}')
                print(f'Título do Livro : {bookTitle}')
                checkLoanPending(document)

                print('--------\n')
        else:
            print('\nNenhum empréstimo cadastrado.')

    def finishLoanBy(finishLoan):
        if (finishLoan):
            userId = finishLoan['user_id']
            userName = collectionUsers.find_one({'_id': userId})['name']

            bookId = finishLoan['book_id']
            bookTitle = collectionBooks.find_one({'_id': bookId})['title']

            print('\n')
            friendlyPrint(finishLoan, loanKeyMapping)
            print(f'Nome do Usuário : {userName}')
            print(f'Título do Livro : {bookTitle}')

            checkLoanPending(finishLoan)

            userConfirm = str(input('\nDigite CONFIRMAR para finalizar o empréstimo acima:\n>> '))

            if (userConfirm.lower() == 'confirmar'):
                try:
                    bookId = finishLoan['book_id']
                    currentQuantity = collectionBooks.find_one({'_id': bookId})['quantity']

                    collectionBooks.update_one({'_id': bookId}, {'$set': {'quantity': currentQuantity + 1}})

                    collectionLoans.update_one({'_id': finishLoan['_id']}, {'$set': {'returned_date': datetime.now().replace(microsecond=0)}})
                    print('\nEmprestimo finalizado com sucesso!')
                
                except:
                    print('\nAlgo deu errado, tente novamente.')

    def removeLoanBy(removeLoan):
        if (removeLoan):
            userId = removeLoan['user_id']
            userName = collectionUsers.find_one({'_id': userId})['name']

            bookId = removeLoan['book_id']
            bookTitle = collectionBooks.find_one({'_id': bookId})['title']

            print('\n')
            friendlyPrint(removeLoan, loanKeyMapping)
            print(f'Nome do Usuário : {userName}')
            print(f'Título do Livro : {bookTitle}')

            checkLoanPending(removeLoan)
            
            userConfirm = str(input('\nDigite CONFIRMAR para remover o empréstimo acima:\n>> '))

            if userConfirm.lower() == 'confirmar':
                try:
                    bookId = removeLoan['book_id']
                    currentQuantity = collectionBooks.find_one({'_id': bookId})['quantity']

                    collectionBooks.update_one({'_id': bookId}, {'$set': {'quantity': currentQuantity + 1}})
                    collectionLoans.delete_one({'_id': removeLoan['_id']})
                    print('\nEmprestimo removido com sucesso')

                except Exception as e:
                    print(f'\nAlgo deu errado: {e}')

    while True:
        try:
            userRequest = str(input("\nO quê deseja consultar?\n1 - Livros\n2 - Usuários\n3 - Empréstimos\n\nDeixe em branco para sair:\n\n>> "))

            # Baseado na escolha do usuário, executa as funções de livros, usuários ou empréstimos            
            if (userRequest == '1') or (userRequest.lower() == 'livros'):
                
                # Chama funções relacionadas a livros
                while True:
                    userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar livros disponíveis\n2 - Listar todos os livros\n3 - Adicionar livro\n4 - Atualizar livro\n5 - Remover livro\n\nDeixe em branco para voltar:\n\n>> '))
                    
                    if (userRequest == '1') or (userRequest.lower() == 'consultar'):
                        showAvailableBooks()

                    elif (userRequest == '2') or (userRequest.lower() == 'listar'):
                        searchBooksAll()

                    elif (userRequest == '3') or (userRequest.lower() == 'adicionar'):
                        insertBook()

                    elif (userRequest == '4') or (userRequest.lower() == 'atualizar'):
                        updateBook = searchBookBy()
                        updateBookBy(updateBook)

                    elif (userRequest == '5') or (userRequest.lower() == 'remover'):
                        removeBook = searchBookBy()
                        removeBookBy(removeBook)

                    elif (userRequest.strip() == ''):
                        break

                    else:
                        print('\nOpção inválida\n')

            elif (userRequest == '2') or (userRequest.lower() == 'usuários'):
                
                # Chama funções relacionadas a usuários
                while True:
                    userRequest = str(input('\nQual função deseja realizar?\n1 - Listar todos os usuários\n2 - Empréstimos de um usuário específico\n3 - Consultar usuários com empréstimos vencidos\n4 - Adicionar usuário\n5 - Atualizar usuário\n6 - Remover usuário\n\nDeixe em branco para voltar:\n\n>> '))

                    if (userRequest == '1') or (userRequest.lower() == 'Listar'):
                        searchUserAll()

                    elif (userRequest == '2') or (userRequest.lower() == 'especifico'):
                        specificUser = searchUserBy()
                        searchUserLoans(specificUser)
                    
                    elif (userRequest == '3') or (userRequest.lower() == 'vencidos'):
                        searchUserExpired()

                    elif (userRequest == '4') or (userRequest.lower() == 'adicionar'):
                        insertUser()

                    elif (userRequest == '5') or (userRequest.lower() == 'atualizar'):
                        updateUser = searchUserBy()
                        updateUserBy(updateUser)

                    elif (userRequest == '6') or (userRequest.lower() == 'remover'):
                        removeUser = searchUserBy()
                        removeUserBy(removeUser)

                    elif (userRequest.strip() == ''):
                        break

                    else:
                        print('\nOpção inválida\n')

            elif (userRequest == '3') or (userRequest.lower() == 'empréstimos'):

                # Chama funções relacionadas a empréstimos
                while True:
                    userRequest = str(input('\nQual função deseja realizar?\n1 - Consultar todos os empréstimos\n2 - Consultar empréstimos por período\n3 - Abrir empréstimo\n4 - Finalizar empréstimo\n5 - Remover empréstimo do sistema\n\nDeixe em branco para voltar:\n\n>> '))

                    if (userRequest == '1') or (userRequest.lower() == 'consultar'):
                        searchLoanAll()

                    elif (userRequest == '2') or (userRequest.lower() == 'periodo'):
                        searchLoanByPeriod()

                    elif (userRequest == '3') or (userRequest.lower() == 'abrir'):
                        insertLoan()

                    elif (userRequest == '4') or (userRequest.lower() == 'finalizar'):
                        finishLoan = searchLoanBy()
                        finishLoanBy(finishLoan)

                    elif (userRequest == '5') or (userRequest.lower() == 'remover'):
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

    client.close()

if __name__ == '__main__':
    main()
