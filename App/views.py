from django.shortcuts import render
from App.utils import datafunctions as obje
# Create your views here.
def index(request):
    return render(request,'index.html')
def homepage(request):
    return render(request,'home.html')
def helppage(request):
    return render(request,'help.html')
def aboutpage(request):
    return render(request,'about_us.html')

def solvepage(request):
    userid=request.session['Current_UserID']
    UserTotalModuleProgressInfo=obje.GetUserTotalModuleProgressDetails(userid)
    UserEachModuleProgressInfo=obje.GetUserEachModuleProgressDetails(userid)
    return render(request,'solve.html', {'OverallProgressData':UserTotalModuleProgressInfo,'EachModuleProgressData':UserEachModuleProgressInfo})

def questionspage(request):
    AllQuestionsDetails=obje.GetAllQuestionsDetails()
    selected_moduleID = request.GET.get('module_id')

    selected_questionID = request.GET.get('question_id')
    userid=request.session['Current_UserID']
    Selected_QuestionDetails=obje.GetSelectedQuestionDetails(selected_questionID,userid,selected_moduleID)
    request.session['Current_SelectedQuestion']=Selected_QuestionDetails['QuestionID']

    return render(request,'questions.html',{'question_id':selected_questionID,'SideBarData': AllQuestionsDetails, 'questionInfo': Selected_QuestionDetails})

def userquerysubmit_virtual(request):
    AllQuestionsDetails=obje.GetAllQuestionsDetails()
    selected_moduleID = request.GET.get('module_id')

    selected_questionID = request.session.get('Current_SelectedQuestion')
     
    userid=request.session['Current_UserID']
    Selected_QuestionDetails=obje.GetSelectedQuestionDetails(selected_questionID,userid,selected_moduleID)

    if request.method == 'POST':
        UserQuery=request.POST.get('userSQL_query')
        Answer_Bool=obje.CheckCorrectnessOfUserQuery(UserQuery,userid,selected_questionID)
        QueryTableDictionary=obje.get_data_fromQuery(UserQuery)
        Display_Table_headings=QueryTableDictionary["TableColumnHeadings"]
        Display_Table_Data=QueryTableDictionary["TableRowData"]
        #add ,code to get the output of user query
        print(Answer_Bool)
        return render(request,'questions.html',{'Userquery_Field':UserQuery,'isQueryCorrect':Answer_Bool,'Display_table_data':Display_Table_Data,'Display_Table_head':Display_Table_headings,'question_id':selected_questionID,'SideBarData': AllQuestionsDetails, 'questionInfo': Selected_QuestionDetails})
             
    return render(request,'questions.html',{'question_id':selected_questionID,'SideBarData': AllQuestionsDetails, 'questionInfo': Selected_QuestionDetails})

def loginpage(request):
    UserAuthenticationConfirmation=''
    if request.method == 'POST':
        username = request.POST.get('Username_Input_Box')
        password = request.POST.get('Password_Input_Box')
        userid=obje.OnSignIN_CheckForValidUserPassword(username,password)
        if(userid):
            UserAuthenticationConfirmation=1
            request.session['Current_UserName']=username
            request.session['Current_UserID'] = userid
            obje.On_LoginLogout_AddDataToLogsTable(userid,'Login')
            return render(request,'log_in.html',{'UserAuthenticationConfirmation':UserAuthenticationConfirmation})
        else:
            UserAuthenticationConfirmation=0
            return render(request,'log_in.html',{'UserAuthenticationConfirmation':UserAuthenticationConfirmation})
        
    return render(request,'log_in.html',{'UserAuthenticationConfirmation':UserAuthenticationConfirmation})
    
def logoutpage_virtual(request):
    userid=request.session['Current_UserID']
    obje.On_LoginLogout_AddDataToLogsTable(userid,'Logout')
    request.session['Current_UserID'] = 0
    request.session['Current_UserName']=""
    return render(request,'home.html')

def signuppage(request):
    UserDataAddedConfirmation=''
    if request.method == 'POST':
        username = request.POST.get('UserName_InputBox')
        email = request.POST.get('UserEmail_InputBox')
        password = request.POST.get('UserPassword_InputBox')
        if(obje.OnSignUP_AddDataToUsersTable(username,email,password)):
            print("user data successfully added")
            UserDataAddedConfirmation=1
            return render(request,'sing_up.html',{'UserDataAddedConfirmation':UserDataAddedConfirmation})
        else:
            print("User already exists")
            UserDataAddedConfirmation=0
            return render(request,'sing_up.html',{'UserDataAddedConfirmation':UserDataAddedConfirmation})
            
    return render(request,'sing_up.html',{'UserDataAddedConfirmation':UserDataAddedConfirmation})
