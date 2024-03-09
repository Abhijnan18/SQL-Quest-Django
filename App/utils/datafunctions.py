import mysql.connector as m
connection = m.connect(host='localhost', user='root',
                       password='189@2003ihba', database='sqlquest2')
cursor = connection.cursor()


def OnSignUP_AddDataToUsersTable(username, email, password):
    add_user = f"INSERT INTO users (Username, Email, Password) VALUES ('{username}', '{email}', '{password}')"
    try:
        result = cursor.execute(add_user)
        print("Execution Result:", result)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error occurred while adding user: {e}")
        return False


def OnSignIN_CheckForValidUserPassword(username, password):
    try:
        query = f"SELECT * FROM users WHERE Username = '{username}' AND Password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            return user[0]
        else:
            return 0
    except Exception as e:
        print(f"Error occurred while checking user credentials: {e}")
        return 0


def On_LoginLogout_AddDataToLogsTable(userid, logValue):
    try:
        cursor.callproc("InsertLoginLogoutLog", [userid, logValue])
        connection.commit()
        print("Stored procedure called successfully")
    except mysql.connector.Error as error:
        print(f"Error calling stored procedure: {error}")
        connection.rollback()


def GetUserTotalModuleProgressDetails(userID):
    query = f"select sum(CompletedQuestions) as TotalCompletedQuestions,sum(TotalQuestions) as OverallTotalQuestions,(sum(CompletedQuestions)/sum(TotalQuestions))*100 as OverallProgress from usermoduleprogress where UserID = {userID}"
    cursor.execute(query)
    result = cursor.fetchall()
    # Convert list of tuples to list of dictionaries
    columns = [col[0] for col in cursor.description]  # Get column names
    data = dict(zip(columns, result[0])) if result else {}
    """
    #This is how the "data" looks after getting from database
        data= {'TotalCompletedQuestions': <sum(CompletedQuestions)>,
               'OverallTotalQuestions': <sum(TotalQuestions)>,
               'OverallProgress': <Overall_percentage_progress>}
    """
    return data


def GetUserEachModuleProgressDetails(userID):
    query = f"select A.ModuleID,A.Description,B.CompletedQuestions,B.TotalQuestions,B.ProgressPercentage from modules A,usermoduleprogress B where A.ModuleID = B.ModuleID and UserID = {userID}"
    cursor.execute(query)
    result = cursor.fetchall()
    # Convert list of tuples to list of dictionaries
    columns = [col[0] for col in cursor.description]  # Get column names
    alldata = [dict(zip(columns, row)) for row in result]
    return alldata
    """
    #This is how the "alldata" looks after getting from database
        alldata = [
                    {
                        'ModuleID': <value_of_ModuleID_1>,
                        'Description': <value_of_Description_1>,
                        'CompletedQuestions': <value_of_CompletedQuestions_1>,
                        'TotalQuestions': <value_of_TotalQuestions_1>,
                        'ProgressPercentage': <value_of_ProgressPercentage_1>
                    },
                    {
                        'ModuleID': <value_of_ModuleID_2>,
                        'Description': <value_of_Description_2>,
                        'CompletedQuestions': <value_of_CompletedQuestions_2>,
                        'TotalQuestions': <value_of_TotalQuestions_2>,
                        'ProgressPercentage': <value_of_ProgressPercentage_2>
                    },
                    # and so on for each module
                ]
    """


def GetAllQuestionsDetails():
    getSideBarInfo = f"select A.ModuleID,A.Description,B.QuestionID from modules A, questions B where A.ModuleID = B.ModuleID"
    cursor.execute(getSideBarInfo)
    result = cursor.fetchall()
    # Convert list of tuples to list of dictionaries
    columns = [col[0] for col in cursor.description]  # Get column names
    sideBarInfoDict = [dict(zip(columns, row)) for row in result]
    # Initialize a dictionary to group by ModuleID and Description
    grouped_data = {}
    # Group the data by ModuleID and Description
    for item in sideBarInfoDict:
        key = (item['ModuleID'], item['Description'])
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(item['QuestionID'])
    # Convert grouped data to the desired format
    sideBar = [{'ModuleID': key[0], 'Description': key[1],
                'QuestionID': value} for key, value in grouped_data.items()]

    return sideBar
    """
    sideBar = [
                {
                    'ModuleID': 1,
                    'Description': 'Module 1 Description',
                    'QuestionID': [1, 2, 3]  # List of question IDs for Module 1
                },
                {
                    'ModuleID': 2,
                    'Description': 'Module 2 Description',
                    'QuestionID': [4, 5, 6]  # List of question IDs for Module 2
                },
                # Add more modules as needed
            ]
  """


def GetSelectedQuestionDetails(questionID, userID, moduleid):
    if (not questionID):
        GetQuestionIDFromSelectedModule = f"select questionid from questions where moduleid={moduleid} limit 1"
        cursor.execute(GetQuestionIDFromSelectedModule)
        questionID = cursor.fetchone()[0]

    getQuestionInfo = f"select A.Description,B.CompletedQuestions,B.TotalQuestions,B.ProgressPercentage,C.QuestionID,C.QuestionText,C.CorrectAnswer from modules A, usermoduleprogress B, questions C where A.ModuleID = B.ModuleID and A.ModuleID = C.ModuleID and B.UserID = {userID} and C.QuestionId = {questionID}"

    cursor.execute(getQuestionInfo)
    result = cursor.fetchall()

    # Convert list of tuples to single dictionary
    columns = [col[0] for col in cursor.description]  # Get column names
    questionInfoDict = dict(zip(columns, result[0])) if result else {}

    return questionInfoDict


def CheckCorrectnessOfUserQuery(userquery, user_id, question_id):
    myquery = f"SELECT ModuleID, CorrectAnswer FROM Questions WHERE QuestionID = {question_id}"
    cursor.execute(myquery)
    result = cursor.fetchone()
    module_id, answerquery = result

    try:
        # Execute the user query
        cursor.execute(userquery)
        result1 = cursor.fetchall()
    except m.Error as e:
        print(f"Error executing user queries: {e}")
        result1 = []

    # Execute the answer query
    cursor.execute(answerquery)
    result2 = cursor.fetchall()
    # Check if the result sets are the same
    if result1 == result2:
        print("Results are the same")
        is_correct = True
    else:
        print("Results are different")
        is_correct = False

    # Insert a new entry into QuestionAttemptLogs
    insert_query = "INSERT INTO QuestionAttemptLogs (UserID, QuestionID,ModuleID,IsCorrect) VALUES (%s,%s, %s, %s)"
    cursor.execute(insert_query, (user_id, question_id, module_id, is_correct))
    connection.commit()  # Commit the transaction
    print("New entry inserted into QuestionAttemptLogs successfully")

    if (is_correct):
        return True
    else:
        return False


def get_data_fromQuery(user_Query):
    Data_dit = {"TableColumnHeadings": [], "TableRowData": []}
    data = []
    cursor.execute(user_Query)
    column_headings = [col[0] for col in cursor.description]
    for i in cursor:
        data.append(list(i))
    Data_dit["TableColumnHeadings"] = column_headings
    Data_dit["TableRowData"] = data
    return Data_dit
