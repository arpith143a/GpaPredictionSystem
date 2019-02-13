# coding: utf-8

# In[1]:


# SELECT * FROM `students4` WHERE SEM3GPA=0.0 and SEM3CREDITS=0.0 and SEM4GPA=0.0 and SEM4CREDITS=0.0

# ,ID,SEM1CREDITS,SEM1GPA,SEM2CREDITS,SEM2GPA,SEM3CREDITS,SEM3GPA,SEM4CREDITS,SEM4GPA,CCREDITS

# SELECT MAX(CCREDITS), MIN(CCREDITS) from students6 where CCREDITS!=SEM1CREDITS and CCREDITS!=SEM1CREDITS+SEM2CREDITS and CCREDITS!=SEM1CREDITS+SEM2CREDITS+SEM3CREDITS and  CCREDITS=SEM1CREDITS+SEM2CREDITS+SEM3CREDITS+SEM4CREDITS

import keras
import csv
from sklearn import preprocessing
import numpy as np
import pandas as pd
import math
import numpy as np

import string
import csv
from sklearn import preprocessing

def array_string_to_float(a,*params):
    size=len(params)
    gcount=0
    bcount=0
    good=[]
    bad=[]
    for x in range(0,size):
        if (is_number(params[x][a])):
            params[x][a]=float(params[x][a])
            good.append(params[x][a])
            gcount=gcount+1
        else:
            bad.append(params[x][a])
            bcount=bcount+1
    good = np.asarray(good)
    bad = np.asarray(bad)
    typ2=type(bad)
    if bcount != 0:
        print('fishy')
        print(good.shape)
        print(bad.shape)
        print(type(good))
        print(type(bad))
        print(len(params))
        print(bad)
    return good

file=open("students7.csv", "r")
# file=open("students4.5.csv", "r")
reader = csv.reader(file)


### storing csv data in array##################################

processed_rows = []
for line in reader:
    processed_rows.append(line)

size=len(processed_rows)+1  #### SIZE OF LIST####################

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#######################label encoder function#######################

def labencoder(x=[],*args):
    le = preprocessing.LabelEncoder()
    le.fit(x)
    y=le.transform(x)
    return y

#######################one hot encoding##########################
def encoder(x=[],*args):
    labelBinarizer = preprocessing.LabelBinarizer()
    labelBinarizer.fit(x)

    binarized = labelBinarizer.transform(x)
    return binarized

####transform gender of input variable##################
def gender_en(array):
    gender=[]
    zero=0
    one=1
    if array[0]=='M':
        gender.append(one)
    else:
        gender.append(zero)
    return gender

####transform marital of input variable##################
def marital_en(array):
    marital=[]
    zero=0
    one=1
    if array[0]=='S':
        marital.append(one)
    else:
        marital.append(zero)
    return marital

# ###### preprocessing AGE ################################################## FEW AGES NOT THERE (DELETED)
def ip_age(arr):
    if(is_number(arr)):
        arr=float(arr)

    if  arr < 25:  ######## U25 ###########################
        arr='U25'
    elif arr>= 25 and arr < 30:  ######## U30 ###########################
        arr='U30'
    elif arr>= 30 and arr < 37:  ######## U37 ###########################
        arr='u37'
    elif arr>= 37 and arr < 45:  ######## U44 ###########################
        arr='U44'
    elif arr>= 45:  ######## G45 ###########################
        arr='G45'
    else:
        arr = 'U25'
    return arr

for x in range(0,size-1):
    if(is_number(processed_rows[x][0])):
        processed_rows[x][0] =  ip_age(processed_rows[x][0])
age=[]
for x in range(0,size-1):
    age.append(processed_rows[x][0])
AGE=labencoder(age)
AGEen=encoder(AGE)
def age_en(age_ip):

    #######input age step 1##################################3
    ge=[age_ip]
    ge=np.array(ge)
    gen=ip_age(ge)

    #print(gen)

    ####### static defined for getting ages###################################
    AGE1=AGEen[:,0]
    AGE2=AGEen[:,1]
    AGE3=AGEen[:,2]
    AGE4=AGEen[:,3]
    AGE5=AGEen[:,4]
    agedf1 = pd.DataFrame(
            {
                'age' : age,
                'AGE1': AGE1,
                'AGE2': AGE2,
                'AGE3': AGE3,
                'AGE4': AGE4,
                'AGE5': AGE5
            }
        )
    agedf1.age.unique()
    agedf2=agedf1.drop_duplicates('age')
    #print(agedf2)


    ########## input age step 2#################
    agedf3=agedf2.loc[agedf2.age == gen]   ###########################33
    agedf4=agedf3.drop(['age'], axis=1)
    ageres = agedf4.as_matrix()
    agrs=ageres.ravel()
    return agrs

############ PREPROCESSING ENGLISH SCORE ######################################### CORRRECT
def ip_englishscore(arr):
    if(is_number(arr)):
        arr=float(arr)

    elif arr == '':
        arr = 0
    if  arr < 4.6 :  ######## U25 ###########################
        arr='N'
    elif arr>= 4.5 and arr < 5.1:  ######## U30 ###########################
        arr='E1'
    elif arr>= 5.0 and arr < 5.6:  ######## U37 ###########################
        arr='E2'
    elif arr>= 5.5 and arr < 6.1:  ######## U44 ###########################
        arr='E3'
    elif arr>= 6.0 and arr < 6.6:  ######## G45 ###########################
        arr='E4'
    elif arr>= 6.5 and arr < 7.6:  ######## G45 ###########################
        arr='E5'
    elif arr> 7.5:
        arr='E6'
    return arr

for x in range(0,size-1):
    processed_rows[x][4] = ip_englishscore(processed_rows[x][4])

englishscore=[]
for x in range(0,size-1):
    englishscore.append(processed_rows[x][4])
ENGLISHSCORE=labencoder(englishscore)

ENGen=encoder(ENGLISHSCORE)
def english_score_en(eng_ip):


    ##### input function for englishscore########

    #######input eng step 1##################################3
    eng=[eng_ip]

    eng=np.array(eng)
    eng=ip_englishscore(eng)

    ####### static defined for getting eng###################################
    ENGLISHSCORE1=ENGen[:,0]
    ENGLISHSCORE2=ENGen[:,1]
    ENGLISHSCORE3=ENGen[:,2]
    ENGLISHSCORE4=ENGen[:,3]
    ENGLISHSCORE5=ENGen[:,4]
    ENGLISHSCORE6=ENGen[:,5]
    ENGLISHSCORE7=ENGen[:,6]


    engdf1 = pd.DataFrame(
            {
                'englishscore' : englishscore,
                'ENGLISHSCORE1': ENGLISHSCORE1,
                'ENGLISHSCORE2': ENGLISHSCORE2,
                'ENGLISHSCORE3': ENGLISHSCORE3,
                'ENGLISHSCORE4': ENGLISHSCORE4,
                'ENGLISHSCORE5': ENGLISHSCORE5,
                'ENGLISHSCORE6': ENGLISHSCORE6,
                'ENGLISHSCORE7': ENGLISHSCORE7
            }
        )
    engdf1.englishscore.unique()
    engdf2=engdf1.drop_duplicates('englishscore')
    #print(engdf2)


    # ########## input eng step 2#################
    engdf3=engdf2.loc[engdf2.englishscore == eng]   ###########################33
    engdf4=engdf3.drop(['englishscore'], axis=1)
    engres = engdf4.as_matrix()
    return engres[0]


# #######################PREPROCESSING FIELD OF STUDY########################################### CORRECT
##### function to transform input fos into category#######
def ip_fos(arr):
    if arr=='Construction, Engineering and Infrastructure Management' or arr=='Geotechnical and Earth Resources Engineering' or arr=='Geosystem Exploration and Petroleum GeoEngineering' or arr=='Structural Engineering' or arr=='Transportation Engineering' or arr=='Water Engineering and Management' or arr=='Geotechnical and Geoenvironmental Engineering':  ######## CIVIL ###########################
        arr='CIVIL'
    elif arr=='Mechatronics' or arr=='Microelectronics' or arr=='Microelectronics and Embedded Systems' or arr=='Industrial and Manufacturing Engineering' or arr=='Nanotechnology' or arr=='Data Science and AI' or arr=='Industrial Engineering & Management' or arr=='Design and Manufacturing Engineering':  ######## ISE ###########################
        arr='ISE'
    elif arr=='Computer Science' or arr== 'Information Management' or arr=='Remote Sensing and Geographic Information Systems' or arr=='Telecommunications' or arr=='Data Science and AI' or arr=='Management of Technology' or arr=='Software Engineering': ######## ICT ###########################
        arr='ICT'
    elif arr=='Information & Communications Technologies' or arr== 'Disaster Preparedness, Mitigation and Management':  ######## INTERDISCIPLINARY########################
        arr='INTERDISCIPLINARY'
    elif arr== 'Agri-Business Management' or arr=='Energy Business Management' or arr=='Urban Water Engineering and Management' or arr=='Energy and Environment' or arr=='Pulp and Paper Technology' or arr=='Agricultural Systems & Engineering' or arr== 'Agricultural Systems And Engineering' or arr=='Aquaculture and Aquatic Resources Management' or arr=='Climate Change and Sustainable Development' or arr=='Energy' or arr=='Environmental Engineering and Management' or arr=='Food Engineering and Bioprocess Technology' or arr=='Food, Agriculture and Bio Systems' or arr=='Gender and Development Studies' or arr=='Gender, Transportation and Development' or arr=='Regional and Rural Development Planning' or arr=='Urban Environmental Management' or arr=='Natural Resources Management' :  ######## ALL SERD ###########################
        arr='SERD'
    elif arr=='International Business' or arr=='AgriBusiness Management' or arr=='International Business - Management of Technology (VN)' or arr=='International Business - Management of Technology (BKK)' or arr== 'Service Marketing and Technology' or arr=='International Public Management' or arr=='Offshore Technology and Management' or arr=='Human Resources Management' or arr=='International Business - Management of Technology' or arr=='Business Administration - MBA' or arr=='Banking and Finance' or arr=='Finance' or arr=='Banking and Information Management':  ######## ALL SOM ###########################
        arr='SOM'
    return arr

for x in range(0,size-1):
    processed_rows[x][9] = ip_fos(processed_rows[x][9])

fieldofstudy=[]
for x in range(0,size-1):
    fieldofstudy.append(processed_rows[x][9])
FIELDOFSTUDY=labencoder(fieldofstudy)
fieldofstudyen=encoder(fieldofstudy)
def field_of_study_en(fos_input):


    fos=[fos_input]
    #print("input fos transformed to array")

    fos=np.array(fos)
    fos=ip_fos(fos)
    #print("fos transformed in category")

    FIELDOFSTUDY1=fieldofstudyen[:,0]
    FIELDOFSTUDY2=fieldofstudyen[:,1]
    FIELDOFSTUDY3=fieldofstudyen[:,2]
    FIELDOFSTUDY4=fieldofstudyen[:,3]
    FIELDOFSTUDY5=fieldofstudyen[:,4]
    FIELDOFSTUDY6=fieldofstudyen[:,5]

    fosdf1 = pd.DataFrame({'fieldofstudy': fieldofstudy,'FIELDOFSTUDY1': FIELDOFSTUDY1,'FIELDOFSTUDY2': FIELDOFSTUDY2,'FIELDOFSTUDY3': FIELDOFSTUDY3,'FIELDOFSTUDY4': FIELDOFSTUDY4,'FIELDOFSTUDY5': FIELDOFSTUDY5,'FIELDOFSTUDY6' : FIELDOFSTUDY6})
    fosdf1.fieldofstudy.unique()
    fosdf2=fosdf1.drop_duplicates('fieldofstudy')
    #print(fosdf2)

    # ########## input eng step 2#################
    fosdf3=fosdf2.loc[fosdf2.fieldofstudy == fos]   ###########################33
    fosdf4=fosdf3.drop(['fieldofstudy'], axis=1)
    fosres = fosdf4.as_matrix()
    fosres=fosres.ravel()
    #print("encoded input fos")
    return fosres

#  ################# PREPROCESSING PREVIOUS MAJOR###########################

# # here new  column category created for previous major#######################
# # NOTE: a function has to be created where the input previous major must map with its respective CATEGORY


######forming array of encoded arrays######
previousmajor=[]
for x in range(0,size-1):
    previousmajor.append(processed_rows[x][8])
PREVIOUSMAJOR=labencoder(previousmajor)

orgprevmaj=[]
for x in range(0,size-1):
    orgprevmaj.append(processed_rows[x][7])

PREVIOUSMAJORen=encoder(PREVIOUSMAJOR)
def previous_major_en(ippm):

    PM1=PREVIOUSMAJORen[:,0]
    PM2=PREVIOUSMAJORen[:,1]
    PM3=PREVIOUSMAJORen[:,2]
    PM4=PREVIOUSMAJORen[:,3]
    PM5=PREVIOUSMAJORen[:,4]
    PM6=PREVIOUSMAJORen[:,5]
    PM7=PREVIOUSMAJORen[:,6]
    PM8=PREVIOUSMAJORen[:,7]
    PM9=PREVIOUSMAJORen[:,8]
    PM10=PREVIOUSMAJORen[:,9]
    PM11=PREVIOUSMAJORen[:,10]
    PM12=PREVIOUSMAJORen[:,11]
    PM13=PREVIOUSMAJORen[:,12]

    ####### panda for matching prev maj with cat################
    ppmdf1=pd.DataFrame({'orgprevmaj': orgprevmaj,'previousmajor': previousmajor })
    ppmdf2=ppmdf1.drop_duplicates('orgprevmaj')
    # #print(ppmdf2)

    #########step 2##########
    ppmdf3=ppmdf2.loc[ppmdf2.orgprevmaj == ippm]
    ppmdf4=ppmdf3.drop(['orgprevmaj'], axis=1)
    ppmdf5 = ppmdf4.as_matrix()
    ppmdf6=ppmdf5.ravel()
    ppmm=''.join(ppmdf6)
    #print(ppmm)

    ########### pandas to match cat with encodes###########

    pmdf1 = pd.DataFrame({'previousmajor': previousmajor,'aa': PM1,'ab': PM2,'ac': PM3,'ad': PM4,'ae': PM5,'af': PM6,'ag': PM7,'ah': PM8,'ai': PM9,'aj': PM10,'ak': PM11,'al': PM12,'am': PM13})

    pmdf2=pmdf1.drop_duplicates('previousmajor')
    #print(pmdf2)


    # ########## step3 #################
    pmdf3=pmdf2.loc[pmdf2.previousmajor == ppmm]   ###########################33
    pmdf4=pmdf3.drop(['previousmajor'], axis=1)
    pmres = pmdf4.as_matrix()
    pmrs=pmres.ravel()
    return pmrs

file=open("worldbank.csv", "r")
reader = csv.reader(file)


### storing worldbank.csv data in array##################################

oecd_rows = []
for line in reader:
    oecd_rows.append(line)
size2=len(oecd_rows)
#########################INSERTING INCOME VALUE FROM OECD to students data##################### CORRECT
count = 0;
count1=0;
COUNTRY = 3;
for oecd_row in oecd_rows:
    for processed_row in processed_rows:
        if(processed_row[COUNTRY]== oecd_row[1]):
            processed_row[10]=oecd_row[0]
            count += 1

##############################transforming country names not same in world bank #####################
for x in range(0,size-1):
    if processed_rows[x][3]=='PR China' or processed_rows[x][3]=='Iran'or processed_rows[x][3]=='Taiwan':
        processed_rows[x][10]='Upper middle income'
    elif processed_rows[x][3]=='Korea' or processed_rows[x][3]=='United States of America' or processed_rows[x][3]=='Hong Kong':
        processed_rows[x][10]='High income'
    elif processed_rows[x][3]=='Kyrgyzstan' or processed_rows[x][3]=='Tibetan Living in India' or processed_rows[x][3]=='Republic of Yemen' or processed_rows[x][3]=='Cook Islands':
        processed_rows[x][10]='Lower middle income'

income=[]
for x in range(0,size-1):
    income.append(processed_rows[x][10])
INCOME=labencoder(income)

# #print(processed_rows[0])

# for x in range(0,size-1):
#     #print(processed_rows[x][14])


# In[13]:


#print(processed_rows[0][3],income[0],INCOME[0])
INCen=encoder(INCOME)

nationality=[]
for x in range(size-1):
    nationality.append(processed_rows[x][3])
#print(nationality[0],income[0],INCOME[0],INCen[0])

###### input function for nationality  step1 #########
def nationality_en(ipnat):
    # ipnat='PR China'
    for x in range(len(oecd_rows)):
        if(oecd_rows[x][1]==ipnat):
            ipinc=oecd_rows[x][0]

        elif ipnat=='PR China' or ipnat=='Iran'or ipnat=='Taiwan':
            ipinc='Upper middle income'
        elif ipnat=='Korea' or ipnat=='United States of America' or ipnat=='Hong Kong':
            ipinc='High income'
        elif ipnat=='Kyrgyzstan' or ipnat=='Tibetan Living in India' or ipnat=='Republic of Yemen' or ipnat=='Cook Islands':
            ipinc='Lower middle income'

    #print(ipinc)
    # ####### static defined for getting income encooder###################################
    IN1=INCen[:,0]
    IN2=INCen[:,1]
    IN3=INCen[:,2]
    IN4=INCen[:,3]
    indf1 = pd.DataFrame({'income': income,'aa': IN1,'ab': IN2,'ac': IN3,'ad': IN4})

    indf2=indf1.drop_duplicates('income')
    #print(indf2)

    # # ########## input eng step 2#################
    indf3=indf2.loc[indf2.income == ipinc]   ###########################33
    indf4=indf3.drop(['income'], axis=1)
    inres = indf4.as_matrix()
    inres=inres.ravel()
    #print( "encoded input income")
    return inres

# In[15]:


lw1=[]
for x in range(0,size-1):
    lw1.append(processed_rows[x][14])
LEFTWITH1=labencoder(lw1)

#print(lw1[0],LEFTWITH1[0])


# In[16]:


lw2=[]
for x in range(0,size-1):
    lw2.append(processed_rows[x][17])
LEFTWITH2=labencoder(lw2)


#print(lw2[0],LEFTWITH2[0])


# In[17]:


lw3=[]
for x in range(0,size-1):
    lw3.append(processed_rows[x][20])
LEFTWITH3=labencoder(lw3)

#print(lw3[0],LEFTWITH3[0])


# In[18]:


####### function to transform leftwith input attributes#######
def ip_lw(string_ip):
    if string_ip == 'T/R + C':
        return 1
    else:
        return 0

############PREPROCESS PREVIOUSINSTITUTE CGPA##############################################

size=len(processed_rows)+1
for x in range(1,size-1):
    ############## for thailand #############################################################
    if processed_rows[x][3]=='Thailand' :
        grade = str(processed_rows[x][6]).replace('%',"");
        if(is_number(grade)):
            thai_grade=float(grade)
            if(thai_grade >= 75.0):
                processed_rows[x][6]= 4.0
            elif(thai_grade >= 65.0 and  thai_grade <= 74.0 ):
                processed_rows[x][6]= 3.0
            elif(thai_grade >= 55.0 and  thai_grade <= 64.0 ):
                processed_rows[x][6]= 2.0
        else:
            if (processed_rows[x][6]=='A'):
                processed_rows[x][6]= 4.0
            elif (processed_rows[x][6]=='B+' or processed_rows[x][6]=='A-'):
                processed_rows[x][6]= 3.5
            elif (processed_rows[x][6]=='C+' or processed_rows[x][6]=='B'):
                processed_rows[x][6]= 2.75
            elif (processed_rows[x][6]=='C'):
                processed_rows[x][6]= 2.5
    ################ for vietnam ##################################################################
    elif processed_rows[x][3]=='Vietnam':
        if(is_number(processed_rows[x][6])):
            viet_grade=float(processed_rows[x][6])

            if(9.00 <=   viet_grade  <= 10.00):
                processed_rows[x][6]= 4.0
            elif(8.00 <= viet_grade  <= 9.0 ):
                processed_rows[x][6]= 3.5
            elif(7.00 <= viet_grade  <= 8.0  ):
                processed_rows[x][6]= 3.0
            elif(6.00 <= viet_grade  <= 7.0) or (60.00 <= viet_grade  <= 70.0)   :
                processed_rows[x][6]= 2.5
            elif(5.00 <= viet_grade <= 6.0):
                processed_rows[x][6]= 2.0
            elif(4.00 <= viet_grade <= 5.0):
                processed_rows[x][6]= 1.0

        else:
            if (processed_rows[x][6]=='Excellent' or 'V.G'):
                processed_rows[x][6]= 3.5
            elif (processed_rows[x][6]=='Good'):
                processed_rows[x][6]= 3.0
            elif (processed_rows[x][6]=='Fair'):
                processed_rows[x][6]= 2.75
            elif (processed_rows[x][6]=='Average'):
                processed_rows[x][6]= 1.5

    elif processed_rows[x][5]=='Genetic Computer School, Singapore':
        if(is_number(processed_rows[x][6])):
            viet_grade=float(processed_rows[x][6])

            if(50.00 <=   viet_grade  <= 60.00):
                processed_rows[x][6]= 2.4

    elif processed_rows[x][3]=='India' or processed_rows[x][3]=='Tibetan Living in India':
        grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(grade)):
            grade_float = float(grade);
            if(grade_float >= 60.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 50.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 40.0):
                processed_rows[x][6]= 3
            elif 6.0 <= grade_float <= 10.0:
                processed_rows[x][6] = 4.0
            elif(5.00 <= grade_float <= 5.9):
                processed_rows[x][6]= 3.5
            elif(4.0 <= grade_float <= 4.9):
                processed_rows[x][6]= 3.0

#
        elif (processed_rows[x][6]=='B+' or processed_rows[x][6]== 'b+'):
                processed_rows[x][6]=3.5

        elif processed_rows[x][6]=='A+' or processed_rows[x][6]== 'a+':
                processed_rows[x][6]=4.0
        else:
            if(grade_float >= 9.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 8.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 7.0):
                processed_rows[x][6]= 3
            elif(grade_float >= 5.0):
                processed_rows[x][6]= 2.75

    elif processed_rows[x][3]=='Myanmar':
        myanmar_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(myanmar_grade)):
            grade_float = float(myanmar_grade);
            if(grade_float >= 65.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 50.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 40.0):
                processed_rows[x][6]= 3
            elif(grade_float >= 30.0):
                processed_rows[x][6]= 2


            elif 6.0 <= grade_float <= 10.0:
                processed_rows[x][6] = 4.0
            elif(5.00 <= grade_float <= 6.0):
                processed_rows[x][6]= 3.5
            elif(4.3 <= grade_float <= 5.0):
                processed_rows[x][6]= 3.0
            elif( 3.5 <= grade_float <= 4.3):
                processed_rows[x][6]= 2.0
            elif 0 <= grade_float < 3.6:
                processed_rows[x][6]= 1.0
        else:
            if processed_rows[x][6]=='A+' :  ##### 4.3
                processed_rows[x][6]= 4.0

            elif processed_rows[x][6]=='A' or processed_rows[x][6]=='A-':  ######### 3.5
                processed_rows[x][6]=3.5

            elif processed_rows[x][6]=='B' or processed_rows[x][6]=='B+' :  ######### 3
                processed_rows[x][6]=3.0
            elif processed_rows[x][6]=='B-' :  ######### 3
                processed_rows[x][6]=2.75
            elif processed_rows[x][6]=='C+'  or processed_rows[x][6]=='Pass':  ######### 3
                processed_rows[x][6]=2.5

    elif processed_rows[x][3]=='Bhutan' or processed_rows[x][3]=='Zimbabwe':
        Bhutan_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Bhutan_grade)):
            grade_float = float(Bhutan_grade);
            if(grade_float >= 80.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 70.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 60.0):
                processed_rows[x][6]= 3
            elif(grade_float >= 50.0):
                processed_rows[x][6]= 2.75
            elif(grade_float >= 40.0):
                processed_rows[x][6]= 2.5

            elif 8.0 <= grade_float <= 10.0:
                processed_rows[x][6] = 4.0
            elif(7.00 <= grade_float <= 6.0):
                processed_rows[x][6]= 3.5
            elif(6.0 <= grade_float <= 5.0):
                processed_rows[x][6]= 3.0
            elif( 5.0 <= grade_float <= 4.0):
                processed_rows[x][6]= 2.0

        else:
            if processed_rows[x][6]=='A+' :  ##### 4.3
                processed_rows[x][6]= 4.0

            elif processed_rows[x][6]=='A' or processed_rows[x][6]=='A-':  ######### 3.5
                processed_rows[x][6]=3.5

            elif processed_rows[x][6]=='B' or processed_rows[x][6]=='B+' :  ######### 3
                processed_rows[x][6]=3.0
            elif processed_rows[x][6]=='B-' :  ######### 3
                processed_rows[x][6]=2.75
            elif processed_rows[x][6]=='C+'  or processed_rows[x][6]=='Pass':  ######### 3
                processed_rows[x][6]=2.5

    elif processed_rows[x][3]=='Japan':
        if processed_rows[x][6]=='N' :
            processed_rows[x][6]=2.75


    elif processed_rows[x][3]=='Lao PDR':
        Lao_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Lao_grade)):
            grade_float = float(Lao_grade);
            if(grade_float >= 80.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 70.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 60.0):
                processed_rows[x][6]= 3
            elif(grade_float >= 50.0):
                processed_rows[x][6]= 2.75


            elif 8.0 <= grade_float <= 10.0:
                processed_rows[x][6] = 4.0
            elif(7.00 <= grade_float <= 8.0):
                processed_rows[x][6]= 3.5
            elif(6.0 <= grade_float <= 7.0):
                processed_rows[x][6]= 3.0
            elif( 5.0 <= grade_float <= 6.0):
                processed_rows[x][6]= 2.0

        else:
            if processed_rows[x][6]=='A' :  ##### 4.3
                processed_rows[x][6]= 4.0

            elif processed_rows[x][6]=='B+' :  ######### 3
                processed_rows[x][6]=3.5
            elif processed_rows[x][6]=='B' :  ######### 3
                processed_rows[x][6]=3.0
            elif processed_rows[x][6]=='C+' :  ######### 3
                processed_rows[x][6]=2.75
            elif processed_rows[x][6]=='C' :  ######### 3
                processed_rows[x][6]=2.5

    elif processed_rows[x][3]=='Philippines':
        Phi_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Phi_grade)):
            grade_float = float(Phi_grade);
            if(grade_float >= 94.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 90.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 83.0):
                processed_rows[x][6]= 3
            elif(grade_float >= 77.0):
                processed_rows[x][6]= 2.75


            elif 9.4 <= grade_float <= 10.0:
                processed_rows[x][6] = 4.0
            elif 9.0 <= grade_float <= 9.4:
                processed_rows[x][6] = 3.5
            elif(8.3 <= grade_float <= 9.1):
                processed_rows[x][6]= 3.0
            elif(7.7 <= grade_float <= 8.4):
                processed_rows[x][6]= 2.75


            elif 1.0 <= grade_float <= 1.24:
                processed_rows[x][6] = 4.0
            elif(1.25 <= grade_float <= 1.74):
                processed_rows[x][6]= 3.5
            elif(1.75 <= grade_float <= 2.5):
                processed_rows[x][6]= 3.0
            elif( 2.6 <= grade_float <= 4.0):
                processed_rows[x][6]= 2.75
            elif( 4.0 <= grade_float <= 5.0):
                processed_rows[x][6]= 2.5
#         else:
#             if (processed_rows[x][6]=='N'):
#                 processed_rows[x][6]=2.5


    elif processed_rows[x][3]=='Sri Lanka':
        Phi_grade = str(processed_rows[x][6]).replace('%',"");
        Sri_grade = str(processed_rows[x][6]).replace("'","")
        if(is_number(Phi_grade)):
            grade_float = float(Phi_grade)

            if(grade_float >= 75.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 65.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 55.0) or (grade_float >= 5.0)  :
                processed_rows[x][6]= 3
            elif(grade_float >= 40.0):
                processed_rows[x][6]= 2.75

            elif (0.0<=grade_float<=5.0):
                grade_float= grade_float * 4.0
                grade_float=grade_float/5.0
                processed_rows[x][6]= round(grade_float,2)

        elif(is_number(Sri_grade)):

            grade_float = float(Sri_grade)

            if(grade_float >= 75.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 65.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 55.0):
                processed_rows[x][6]= 3
            elif(grade_float >= 40.0):
                processed_rows[x][6]= 2.75

            elif (0.0<=grade_float<=5.0):
                grade_float= grade_float * 4.0
                grade_float=grade_float/5.0
                processed_rows[x][6]= round(grade_float,2)
        else:
            if  processed_rows[x][6]=='Pass':  ##### 4.3
                processed_rows[x][6]= 2.75
#                 processed_rows[x][6]=='N' or


    elif processed_rows[x][3]=='Indonesia':
        bang_grade = str(processed_rows[x][6]).replace('..',".");

        if processed_rows[x][6]=='N':
            processed_rows[x][6]=2.75


    elif processed_rows[x][3]=='Bangladesh':
        bang_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(bang_grade)):
            grade_float = float(bang_grade);
            if(grade_float >= 60.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 55.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 50.0):
                processed_rows[x][6]= 3.0
            elif(grade_float >= 43.0):
                processed_rows[x][6]= 2.75
            elif(grade_float >= 35.0):
                processed_rows[x][6]= 2.5

            elif (0.0<=grade_float<=5.0):
                grade_float= grade_float * 4.0
                grade_float=grade_float/5.0
                processed_rows[x][6]= round(grade_float,2)

    elif processed_rows[x][3]=='Cambodia':
        cam_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(cam_grade)):
            grade_float = float(cam_grade);
            if(grade_float >= 85.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 80.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 70.0):
                processed_rows[x][6]= 3.0
            elif(grade_float >= 65.0):
                processed_rows[x][6]= 2.75
            elif(grade_float >= 50.0):
                processed_rows[x][6]= 2.5

            elif (5.0<=grade_float<=10.0):
                grade_float= grade_float * 4.0
                grade_float=grade_float/10.0
                processed_rows[x][6]= round(grade_float,2)
            elif(10.0<=grade_float<=20.0):
                processed_rows[x][6]=2.75

        else:
            if processed_rows[x][6]=='A' :  ##### 4.3
                processed_rows[x][6]= 4.0

            elif processed_rows[x][6]=='B+':  ######### 3.5
                processed_rows[x][6]=3.5

            elif processed_rows[x][6]=='B'  :  ######### 3
                processed_rows[x][6]=3.0
            elif processed_rows[x][6]=='C+' :  ######### 3
                processed_rows[x][6]=2.5
            elif processed_rows[x][6]=='C':  ######### 3
                processed_rows[x][6]=2.0
#             or processed_rows[x][6]=='N'


    elif processed_rows[x][3]=='Nepal':
        Nepal_grade = str(processed_rows[x][6]).replace('%',"");
        Nepali_grade = str(processed_rows[x][6]).replace('/',"");

        if(is_number(Nepal_grade)):
            grade_float = float(Nepal_grade);
            if(grade_float >= 80.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 60.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 40.0):
                processed_rows[x][6]= 3.0
            elif(grade_float >= 32.0):
                processed_rows[x][6]= 2.75
            elif (5.0<=grade_float<=10.0):
                grade_float= grade_float * 4.0
                grade_float=grade_float/10.0
                processed_rows[x][6]= round(grade_float,2)

        elif(is_number(Nepali_grade)):
            grade_float = float(Nepali_grade);
            if(grade_float >= 80.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 60.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 40.0):
                processed_rows[x][6]= 3.0
            elif(grade_float >= 32.0):
                processed_rows[x][6]= 2.75
            elif (5.0<=grade_float<=10.0):
                grade_float= grade_float * 4.0
                grade_float=grade_float/10.0
                processed_rows[x][6]= round(grade_float,2)

#         else:
#             if processed_rows[x][6]=='N':
#                 processed_rows[x][6]=2.75


    elif processed_rows[x][3]=='Pakistan' or processed_rows[x][3]=='Kenya' or processed_rows[x][3]=='Singapore':
        Pak_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Pak_grade)):
            grade_float = float(Pak_grade);
            if(grade_float >= 70.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 60.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 50.0):
                processed_rows[x][6]= 3.0
            elif(grade_float >= 40.0):
                processed_rows[x][6]= 2.75
            elif(grade_float >= 33.0):
                processed_rows[x][6]= 2.5
        else:
            if processed_rows[x][6]=='A1' or processed_rows[x][6]=='A+' or processed_rows[x][6]=='A' :  ##### 4.3
                processed_rows[x][6]= 4.0

            elif processed_rows[x][6]=='B':  ######### 3.5
                processed_rows[x][6]=3.5

            elif processed_rows[x][6]=='C' :  ######### 3
                processed_rows[x][6]=3.0
            elif processed_rows[x][6]=='D' :  ######### 3
                processed_rows[x][6]=2.5
            elif processed_rows[x][6]=='E':  ######### 3
                processed_rows[x][6]=2.0

    elif processed_rows[x][3]=='PR China' or processed_rows[x][3]=='Taiwan' or processed_rows[x][3]=='Mongolia':
        China_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(China_grade)):
            grade_float = float(China_grade);
            if(grade_float >= 90.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 80.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 70.0):
                processed_rows[x][6]= 3.0
            elif(grade_float >= 60.0):
                processed_rows[x][6]= 2.75
            elif (5.0<=grade_float<=10.0):
                grade_float= grade_float * 4.0
                grade_float=grade_float/10.0
                processed_rows[x][6]= round(grade_float,2)

        else:
            if processed_rows[x][6]=='A+' :  ##### 4.3
                processed_rows[x][6]= 4.0

            elif processed_rows[x][6]=='A' or processed_rows[x][6]=='A-':  ######### 3.5
                processed_rows[x][6]=3.5

            elif processed_rows[x][6]=='B' or processed_rows[x][6]=='B+' :  ######### 3
                processed_rows[x][6]=3.0
            elif processed_rows[x][6]=='B-' or processed_rows[x][6]=='C+' :  ######### 3
                processed_rows[x][6]=2.75
            elif processed_rows[x][6]=='C-'  or processed_rows[x][6]=='Pass':  ######### 3
                processed_rows[x][6]=2.5
#             or processed_rows[x][6]=='N'


    elif processed_rows[x][3]=='Kyrgyzstan' or  processed_rows[x][3]=='Colombia' or processed_rows[x][3]=='Korea' or processed_rows[x][3]=='Tanzania' or processed_rows[x][3] =='Turkmenistan':
        Kyr_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Kyr_grade)):
            grade_float = float(Kyr_grade);
            if (0.0<= grade_float <= 5.0):
                grade_float= grade_float * 4.0
                grade_float=grade_float/5.0
                processed_rows[x][6]= round(grade_float,2)

    elif processed_rows[x][3]=='Iran' or processed_rows[x][3]=='France' or processed_rows[x][3]=='Denmark':
        Ir_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Ir_grade)):
            grade_float = float(Ir_grade);


            if( grade_float>= 80.0):
                processed_rows[x][6]=4.0
            elif( grade_float>= 70.0):
                processed_rows[x][6]=3.5
            elif( grade_float>= 60.0):
                processed_rows[x][6]=3.0

            elif 18.0 <= grade_float <= 20.0:
                processed_rows[x][6] = 4.0
            elif(16.0 <= grade_float <= 18.00):
                processed_rows[x][6]= 3.5
            elif(14.0 <= grade_float <= 16.00):
                processed_rows[x][6]= 3.0
            elif( 12.0 <= grade_float <= 14.0):
                processed_rows[x][6]= 2.75
            elif( 10.0 <= grade_float <= 12.0):
                processed_rows[x][6]= 2.5

        else:
            if processed_rows[x][6]=='A' :  ##### 4.3
                processed_rows[x][6]= 4.0

            elif processed_rows[x][6]=='B+':  ######### 3.5
                processed_rows[x][6]=3.5

            elif processed_rows[x][6]=='B'  :  ######### 3
                processed_rows[x][6]=3.0
            elif processed_rows[x][6]=='C+' :  ######### 3
                processed_rows[x][6]=2.5
            elif processed_rows[x][6]=='C':  ######### 3
                processed_rows[x][6]=2.0


    elif processed_rows[x][3]=='Canada':
        if processed_rows[x][6]=='A+' :  ##### 4.3
            processed_rows[x][6]= 4.0

        elif processed_rows[x][6]=='A' or processed_rows[x][6]=='A-':  ######### 3.5
            processed_rows[x][6]=3.5

        elif processed_rows[x][6]=='B' or processed_rows[x][6]=='B+' :  ######### 3
            processed_rows[x][6]=3.0
        elif processed_rows[x][6]=='B-' or processed_rows[x][6]=='C+' :  ######### 3
            processed_rows[x][6]=2.75
        elif processed_rows[x][6]=='C-'  or processed_rows[x][6]=='Pass':  ######### 3
            processed_rows[x][6]=2.5


    elif processed_rows[x][3]=='Germany':
        Ger_grade = str(processed_rows[x][6]).replace('%',"");
        if(is_number(Ger_grade)):
            grade_float = float(Ger_grade);
            if grade_float>= 80.0:
                processed_rows[x][6]=4.0

            if 1.0 <= grade_float <= 1.6:
                processed_rows[x][6] = 4.0
            elif(1.51 <= grade_float <= 2.6):
                processed_rows[x][6]= 3.5
            elif(2.5 <= grade_float <= 3.6):
                processed_rows[x][6]= 3.0
            elif( 3.5 <= grade_float <= 4.1):
                processed_rows[x][6]= 2.75
            elif( 4.01 <= grade_float <= 6.0):
                processed_rows[x][6]= 2.5
        else:
            if processed_rows[x][6]=='A' :  ##### 4.3
                processed_rows[x][6]= 4.0

            elif processed_rows[x][6]=='B+':  ######### 3.5
                processed_rows[x][6]=3.5

            elif processed_rows[x][6]=='B' or processed_rows[x][6]=='Satry' :  ######### 3
                processed_rows[x][6]=3.0
            elif processed_rows[x][6]=='C+' :  ######### 3
                processed_rows[x][6]=2.5
            elif processed_rows[x][6]=='C':  ######### 3
                processed_rows[x][6]=2.0


    elif processed_rows[x][3]=='Rwanda' :
        Rw_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Rw_grade)):
            grade_float = float(Rw_grade);

            if( grade_float>= 80.0):
                processed_rows[x][6]=4.0
            elif( grade_float>= 75.0):
                processed_rows[x][6]=3.5
            elif( grade_float>= 60.0):
                processed_rows[x][6]=3.0
            elif( grade_float>= 40.0):
                processed_rows[x][6]=2.75

    elif processed_rows[x][3]=='Sweden' :
        sw_grade = str(processed_rows[x][6]).replace('%',"");
        if(is_number(sw_grade)):
            grade_float = float(sw_grade)
            if( grade_float>= 90.0):
                processed_rows[x][6]=4.0
            elif( grade_float>= 60.0):
                processed_rows[x][6]=3.0
            elif( grade_float<= 60.0):
                processed_rows[x][6]=2.0

    elif processed_rows[x][3]=='Maldives':
        mald_grade = str(processed_rows[x][6]).replace('%',"");
        if(is_number(mald_grade)):
            grade_float = float(mald_grade)
            if( grade_float>= 85.0):
                processed_rows[x][6]=4.0
            elif( grade_float>= 75.0):
                processed_rows[x][6]=3.0
            elif( grade_float>= 65.0):
                processed_rows[x][6]=2.0
            elif( grade_float>= 50.0):
                processed_rows[x][6]=1.0
            elif (0.0<= grade_float <= 5.0):
                grade_float= grade_float * 4.0
                grade_float=grade_float/5.0
                processed_rows[x][6]= round(grade_float,2)


    elif processed_rows[x][3]=='Hong Kong' :
        HK_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(HK_grade)):
            grade_float = float(HK_grade);
            if(grade_float >= 80.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 70.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 55.0):
                processed_rows[x][6]= 3.0
            elif(grade_float >= 40.0):
                processed_rows[x][6]= 2.75

            elif (5.0<=grade_float<=10.0):
                grade_float= grade_float * 4.0
                grade_float=grade_float/10.0
                processed_rows[x][6]= round(grade_float,2)

        else:
            if processed_rows[x][6]=='A+' :  ##### 4.3
                processed_rows[x][6]= 4.0

            elif processed_rows[x][6]=='A' or processed_rows[x][6]=='A-':  ######### 3.5
                processed_rows[x][6]=3.5

            elif processed_rows[x][6]=='B' or processed_rows[x][6]=='B+' :  ######### 3
                processed_rows[x][6]=3.0
            elif processed_rows[x][6]=='B-' or processed_rows[x][6]=='C+' :  ######### 3
                processed_rows[x][6]=2.75
            elif processed_rows[x][6]=='C-'  or processed_rows[x][6]=='Pass':  ######### 3
                processed_rows[x][6]=2.5
#                 or processed_rows[x][6]=='N'


    elif processed_rows[x][3]=='Uzbekistan' :
        Uz_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Uz_grade)):
            grade_float = float(Uz_grade);
            if(grade_float >= 85.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 75.0):
                processed_rows[x][6]= 3.0
            elif(grade_float >= 55.0):
                processed_rows[x][6]=2.75

    elif processed_rows[x][3]=='Afghanistan' or processed_rows[x][3]=='Kazakhstan' :
        Af_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Af_grade)):
            grade_float = float(Af_grade);
            if(grade_float >= 90.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 80.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 55.0):
                processed_rows[x][6]=3.0
            elif(grade_float >= 50.0):
                processed_rows[x][6]=2.75

    elif processed_rows[x][3]=='United Kingdom':
        UK_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(UK_grade)):
            grade_float = float(UK_grade);
            if(grade_float >= 70.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 65.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 60.0):
                processed_rows[x][6]=3.0
            elif(grade_float >= 50.0):
                processed_rows[x][6]=2.75
#     elif processed_rows[x][3]=='U':
#         UK_grade = str(processed_rows[x][6]).replace('%',"");

#         if(is_number(UK_grade)):
#             grade_float = float(UK_grade);
#             if(grade_float >= 70.0):
#                 processed_rows[x][6]= 4.0
#             elif(grade_float >= 65.0):
#                 processed_rows[x][6]= 3.5
#             elif(grade_float >= 60.0):
#                 processed_rows[x][6]=3.0
#             elif(grade_float >= 50.0):
#                 processed_rows[x][6]=2.75


    elif processed_rows[x][3]=='Timor-Leste':
        if processed_rows[x][6]=='N':
            processed_rows[x][6]=2.75


    elif processed_rows[x][3]=='Nigeria':
        Nig_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Nig_grade)):
            grade_float = float(Nig_grade);
            if(grade_float >= 70.0):
                processed_rows[x][6]= 4.0
            elif(grade_float >= 60.0):
                processed_rows[x][6]= 3.5
            elif(grade_float >= 50.0):
                processed_rows[x][6]=3.0
            elif(grade_float >= 45.0):
                processed_rows[x][6]=2.75
            elif(grade_float >= 40.0):
                processed_rows[x][6]=2.5
            elif 0.0<= grade_float <= 5.0:
                grade_float= grade_float * 4.0
                grade_float=grade_float/5.0
                processed_rows[x][6]= round(grade_float,2)


    elif processed_rows[x][3]=='Spain' :
        Sp_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Sp_grade)):
            grade_float = float(Sp_grade);

            if( grade_float>= 90.0):
                processed_rows[x][6]=4.0
            elif( grade_float>= 70.0):
                processed_rows[x][6]=3.5
            elif( grade_float>= 55.0):
                processed_rows[x][6]=3.0
            elif( grade_float>= 50.0):
                processed_rows[x][6]=2.75

            elif 9.0 <= grade_float <= 10.0:
                processed_rows[x][6] = 4.0
            elif(7.0 <= grade_float <= 9.00):
                processed_rows[x][6]= 3.5
            elif(5.5 <= grade_float <= 7.0):
                processed_rows[x][6]= 3.0
            elif( 5.0 <= grade_float <= 5.5):
                processed_rows[x][6]= 2.75

    elif processed_rows[x][3]=='Uganda' :
        Ug_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Ug_grade)):
            grade_float = float(Ug_grade);

            if( grade_float>= 80.0):
                processed_rows[x][6]=4.0
            elif( grade_float>= 75.0):
                processed_rows[x][6]=3.5
            elif( grade_float>= 65.0):
                processed_rows[x][6]=3.0
            elif( grade_float>= 60.0):
                processed_rows[x][6]=2.75

    elif processed_rows[x][3]=='Republic of Yemen' :
        ye_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(ye_grade)):
            grade_float = float(ye_grade);

            if( grade_float>= 88.0):
                processed_rows[x][6]=4.0
            elif( grade_float>= 78.0):
                processed_rows[x][6]=3.5
            elif( grade_float>= 63.0):
                processed_rows[x][6]=3.0
            elif( grade_float>= 48.0):
                processed_rows[x][6]=2.75

    elif processed_rows[x][3]=='South Africa':
        if(processed_rows[x][6]=='n'):
            processed_rows[x][6]=2.75

    elif processed_rows[x][3]=='Mexico':
        Me_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(Me_grade)):
            grade_float = float(Me_grade);

            if( grade_float>= 90.0):
                processed_rows[x][6]=4.0
            elif( grade_float>= 80.0):
                processed_rows[x][6]=3.5
            elif( grade_float>= 60.0):
                processed_rows[x][6]=3.0

    elif processed_rows[x][3]=='El Salvador':
        el_grade = str(processed_rows[x][6]).replace('%',"");
        if(is_number(el_grade)):
            grade_float = float(el_grade);
            if 9.0 <= grade_float <= 10.0:
                processed_rows[x][6] = 4.0
            elif(7.0 <= grade_float <= 9.00):
                processed_rows[x][6]= 3.5
            elif(5.0 <= grade_float <= 7.0):
                processed_rows[x][6]= 3.0
            elif( 3.0 <= grade_float <= 5.0):
                processed_rows[x][6]= 2.75

    elif processed_rows[x][3]=='Turkey':
        tu_grade = str(processed_rows[x][6]).replace('%',"");
        if(is_number(tu_grade)):
            grade_float = float(tu_grade);
            if( grade_float>= 85.0):
                processed_rows[x][6]=4.0
            elif( grade_float>= 75.0):
                processed_rows[x][6]=3.5
            elif( grade_float>= 60.0):
                processed_rows[x][6]=3.0
            elif( grade_float>= 50.0):
                processed_rows[x][6]=2.75

    elif processed_rows[x][3]=='Ghana':
        gh_grade = str(processed_rows[x][6]).replace('%',"");
        if(is_number(gh_grade)):
            grade_float = float(gh_grade);
            if( grade_float>= 75.0):
                processed_rows[x][6]=4.0
            elif( grade_float>= 65.0):
                processed_rows[x][6]=3.5
            elif( grade_float>= 60.0):
                processed_rows[x][6]=3.0
            elif( grade_float>= 50.0):
                processed_rows[x][6]=2.75

    elif processed_rows[x][3]=='Namibia':
        if processed_rows[x][6]=='N':
            processed_rows[x][6]=2.75


    elif processed_rows[x][3]=='Australia' :
        aus_grade = str(processed_rows[x][6]).replace('%',"");

        if(is_number(aus_grade)):
            grade_float = float(aus_grade);

            if( grade_float>= 83.0):
                processed_rows[x][6]=4.0
            elif( grade_float>= 73.0):
                processed_rows[x][6]=3.5
            elif( grade_float>= 63.0):
                processed_rows[x][6]=3.0
            elif( grade_float>= 50.0):
                processed_rows[x][6]=2.75

            elif 7.0 <= grade_float <= 10.0:
                processed_rows[x][6] = 4.0
            elif(6.0 <= grade_float <= 7.00):
                processed_rows[x][6]= 3.5
            elif(5.0 <= grade_float <= 6.0):
                processed_rows[x][6]= 3.0
            elif( 4.0 <= grade_float <= 5.0):
                processed_rows[x][6]= 2.75


prevgpa=[]
count=0
for x in range(0,size-1):
    prevgpa.append(processed_rows[x][6])

# In[19]:

### Previous Institute #########################################################

file=open("real.csv", "r")
reader1 = csv.reader(file)
rows = []
for line in reader1:
    rows.append(line)
size3=len(rows)
name=[]
r1=[]
r2=[]
for row in rows:
    name.append(row[2])
size4=len(name)

name=np.array(name)
name=name.transpose()
#print(name.shape)
#print("previous gpa float transformation:")
r1=array_string_to_float(0,*rows).transpose()
#print("cgpa float transformation:")
r2=array_string_to_float(1,*rows).transpose()
#print(r1)
df = pd.DataFrame({'a': name,'b': r1,'c': r2,'Average': "",'Rank': "" })

#print(len(df))

df['b'] = pd.to_numeric(df['b'], errors='coerce')
df['c'] = pd.to_numeric(df['c'], errors='coerce')

df['sub']= (df['c'] - df['b'])
df['sub'] = pd.to_numeric(df['sub'], errors='coerce')

df['Average'] = df.groupby('a')['sub'].transform('mean')
df['Average'] = pd.to_numeric(df['Average'], errors='coerce')

df['Rank'] = df['Average'].rank(method='dense',ascending=True)
df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')

#print("Minimum rank ")
print (df['Rank'].min())
#print("Max rank ")
print (df['Rank'].max())
#print("total unique ranks")
#print(df['Average'].nunique()) #### total ranks 617
#print("total  institutes")
#print(df['Average'].count()) #####total institutes#####

#print(df)
#print("Average CGPA:")
avgcgpa=df["c"].mean()
#print(avgcgpa)


##########################storing back into arrays for modelling#################################
preinstset=df.as_matrix()

#print("1st row of array")
#print(preinstset[0])
prename=[]

for p in preinstset:
    prename.append(p[2])
score=array_string_to_float(5,*preinstset)
rank=array_string_to_float(1,*preinstset)


#print(len(prename))


rankset=[]
for x in range(0,size-1):
    rankset.append(preinstset[x][1])
rankset=labencoder(rankset)

iset=[]
for x in range(0,size-1):
    if(is_number(preinstset[x][1])):
        preinstset[x][1]=float(preinstset[x][1])
    oset=math.ceil(preinstset[x][1]/6.47)
    iset.append(oset)
iset=np.array(iset)
#print(iset)
s=df['a']
def prev_institution_en(ipprename, prevgpa):
    #################### input previous institute #########################################

    # ipprename='VRS' ### input value() take into string
    pd.options.mode.chained_assignment = None


    if is_number(prevgpa):
        prevgpa = float(prevgpa)

    if (ipprename in set(s)):
        #print(ipprename)
        dfdf=df.drop_duplicates('a')
        dfdf1=dfdf.loc[dfdf.a == ipprename]
        dfdf2=dfdf1.drop(df.columns[[0,2,3,4,5]], axis=1)
        iprankold=dfdf2.as_matrix()
        iprankold=iprankold.ravel()
        #print(iprankold)
        iprank=iprankold/(df['Average'].nunique()/100)
        ipfinrank=math.ceil(iprank)

        #print("final rank of old institute ",ipprename,"is:", ipfinrank)

    else:
        #print("For New institute")
        #print(avgcgpa)
        ippgpa=[prevgpa] ####### get this value aftertransforming orginal pregpa

        ipscore=avgcgpa- ippgpa[0]
        hey=round(ipscore,2)
        #print('The rounded of score is',hey)

        dfx=df.drop_duplicates('a')
        dfx.Average=dfx.Average.round(2)

        dfx['dif'] = (dfx['Average'] - hey).abs()
        newprank=dfx.Rank[dfx['dif'].idxmin()]
        ipfinrank=math.ceil(newprank/6.47)

        #print("final rank of new institute ",ipprename,"is:", ipfinrank)
    return ipfinrank

#############################FEATURE SELECTION PROCESS ####################################################

##################final arrays for training##############################################

FIELDOFSTUDY = fieldofstudyen
AGE = AGEen
ENGLISHSCORE = ENGen
INCOME = INCen
PREVIOUSMAJOR = PREVIOUSMAJORen

SEM1 = []

cgpa=array_string_to_float(40,*processed_rows)
prevgpa=array_string_to_float(6,*processed_rows)
sem1cre=array_string_to_float(13,*processed_rows)
sem1gpa=array_string_to_float(12,*processed_rows)

sem2cre=array_string_to_float(16,*processed_rows)
sem2gpa=array_string_to_float(15,*processed_rows)

sem3cre=array_string_to_float(19,*processed_rows)
sem3gpa=array_string_to_float(18,*processed_rows)

sem4cre=array_string_to_float(22,*processed_rows)
sem4gpa=array_string_to_float(21,*processed_rows)

for i in range(0, len(processed_rows)):
    curRow = []
#     curRow.extend(MARITAL[i])
#     curRow.extend(GENDER[i])
    curRow.extend(INCOME[i].flatten())
    curRow.extend(FIELDOFSTUDY[i].flatten())
    curRow.extend(ENGLISHSCORE[i].flatten())
    curRow.extend(PREVIOUSMAJOR[i].flatten())
    curRow.extend(AGE[i].flatten())
    curRow.append(iset[i])
    curRow.append(prevgpa[i])
    curRow.append(sem1cre[i])
    SEM1.append(curRow)
model1=np.array(SEM1)

SEM2=[]

for i in range(0, len(processed_rows)):
    curRow = []
#     curRow.extend(MARITAL[i])
    curRow.extend(INCOME[i].flatten())
    curRow.extend(FIELDOFSTUDY[i].flatten())
    curRow.extend(ENGLISHSCORE[i].flatten())
    curRow.extend(PREVIOUSMAJOR[i].flatten())
    curRow.extend(AGE[i].flatten())
    curRow.append(LEFTWITH1[i])
    curRow.append(iset[i])
    curRow.append(prevgpa[i])
    curRow.append(sem1cre[i])
    curRow.append(sem1gpa[i])
    curRow.append(sem2cre[i])
    SEM2.append(curRow)
model2=np.array(SEM2)


SEM3=[]


for i in range(0, len(processed_rows)):
    curRow = []
    curRow.extend(AGE[i].flatten())
    curRow.extend(INCOME[i].flatten())
    curRow.extend(FIELDOFSTUDY[i].flatten())
    curRow.extend(ENGLISHSCORE[i].flatten())
    curRow.extend(PREVIOUSMAJOR[i].flatten())
    curRow.append(LEFTWITH1[i])
    curRow.append(LEFTWITH2[i])
    curRow.append(iset[i])
    curRow.append(prevgpa[i])
    curRow.append(sem1cre[i])
    curRow.append(sem1gpa[i])
    curRow.append(sem2cre[i])
    curRow.append(sem2gpa[i])
    curRow.append(sem3cre[i])

    SEM3.append(curRow)
model3=np.array(SEM3)

SEM4=[]

for i in range(0, len(processed_rows)):
    curRow = []
#     curRow.extend(MARITAL[i])
#     curRow.extend(INCOME[i].flatten())
    curRow.extend(AGE[i].flatten())

    curRow.extend(FIELDOFSTUDY[i].flatten())
    curRow.extend(ENGLISHSCORE[i].flatten())
    curRow.extend(PREVIOUSMAJOR[i].flatten())
    curRow.append(LEFTWITH2[i])
    curRow.append(LEFTWITH3[i])
    curRow.append(iset[i])
    curRow.append(prevgpa[i])
    curRow.append(sem1cre[i])
    curRow.append(sem1gpa[i])
    curRow.append(sem2cre[i])
    curRow.append(sem2gpa[i])
    curRow.append(sem3cre[i])
    curRow.append(sem3gpa[i])
    curRow.append(sem4cre[i])
#     curRow.append(LEFTWITH1[i])
    SEM4.append(curRow)
model4=np.array(SEM4)


scalerx1 = preprocessing.MinMaxScaler(feature_range = (0,1))
# scalery1 = preprocessing.MinMaxScaler(feature_range = (0,1))

scalerx2 = preprocessing.MinMaxScaler(feature_range = (0,1))
# scalery2 = preprocessing.MinMaxScaler(feature_range = (0,1))

scalerx3 = preprocessing.MinMaxScaler(feature_range = (0,1))
# scalery3 = preprocessing.MinMaxScaler(feature_range = (0,1))

scalerx4 = preprocessing.MinMaxScaler(feature_range = (0,1))
# scalery4 = preprocessing.MinMaxScaler(feature_range = (0,1))


sem1cre=array_string_to_float(13,*processed_rows)
sem1gpa=array_string_to_float(12,*processed_rows)

sem2cre=array_string_to_float(16,*processed_rows)
sem2gpa=array_string_to_float(15,*processed_rows)

sem3cre=array_string_to_float(19,*processed_rows)
sem3gpa=array_string_to_float(18,*processed_rows)

sem4cre=array_string_to_float(22,*processed_rows)
sem4gpa=array_string_to_float(21,*processed_rows)

prevgpa=array_string_to_float(6,*processed_rows)



# # ######take numeric rows from sem1##############
# income, fos, english score, previous major, age+minmax = iset, prevgpa, sem1cre
model1row1=model1[:,[35,36,37]]

# # ##### take numeric rows from sem2##############
# income, fos, english score, previous major, age, leftwith1 + minmax = iset, prevgpa, sem1cre, sem1gps, sem2cre
model2row1=model2[:,[36,37,38,39,40]]


# # ###########take numeric rows from sem3########
# age, income , field of study, english score,PREVIOUSMAJOR,leftwith1,leftwith2  + minmax = iset , prevgpa,   sem1cre,sem1gpa, sem2cre,sem2gpa,sem3cre
model3row1=model3[:,[37,38,39,40,41,42,43]]

# # ######################take numeric rows from sem4########
# age,field of study, english score,PREVIOUSMAJOR,leftwith2,leftwith3  + minmax = iset , prevgpa,   sem1cre,sem1gpa, sem2cre,sem2gpa,sem3cre ,sem3gpa,sem4cre
model4row1=model4[:,[33,34,35,36,37,38,39,40,41]]

m1=scalerx1.fit(model1row1)
m2=scalerx2.fit(model2row1)
# y2=scalery1.fit_transform(y2.reshape(-1, 1))
m3=scalerx3.fit(model3row1)
m4=scalerx4.fit(model4row1)

## original transform
M1=m1.transform(model1row1)
M2=m2.transform(model2row1)
M3=m3.transform(model3row1)
M4=m4.transform(model4row1)
#print("LALALA:", model1row1)

def minmax_sem1(iset, prevgpa, sem1cre):
    #print("AAGAM")
    #print(iset)
    return m1.transform([[iset, prevgpa, sem1cre]])

def minmax_sem2(iset, prevgpa, sem1cre, sem1gpa, sem2cre):
    #print("AAGAM")
    #print(iset, prevgpa, sem1cre, sem1gpa, sem2cre)
    return m2.transform([[iset, prevgpa, sem1cre, sem1gpa, sem2cre]])

def minmax_sem3(iset , prevgpa,sem1cre,sem1gpa, sem2cre,sem2gpa,sem3cre):
    return m3.transform([[iset , prevgpa,sem1cre,sem1gpa, sem2cre,sem2gpa,sem3cre]])

def minmax_sem4(iset , prevgpa,sem1cre,sem1gpa, sem2cre,sem2gpa,sem3cre ,sem3gpa,sem4cre):
    return m4.transform([[iset , prevgpa,sem1cre,sem1gpa, sem2cre,sem2gpa,sem3cre ,sem3gpa,sem4cre]])

import tensorflow as tf

semester1_predictor = keras.models.load_model("./sem1.h5")
semester1_predictor._make_predict_function()
semester1_graph = tf.get_default_graph()

semester2_predictor = keras.models.load_model("./sem2.h5")
semester2_predictor._make_predict_function()
semester2_graph = tf.get_default_graph()

semester3_predictor = keras.models.load_model("./sem3.h5")
semester3_predictor._make_predict_function()
semester3_graph = tf.get_default_graph()

semester4_predictor = keras.models.load_model("./sem4.h5")
semester4_predictor._make_predict_function()
semester4_graph = tf.get_default_graph()


def predict_sem1(income, fos, english_score, previous_major, age, iset, prevgpa, sem1cre):
    print(income, fos, english_score, previous_major, age, iset, prevgpa, sem1cre)
    income = nationality_en(income)
    fos = field_of_study_en(fos)
    english_score = english_score_en(english_score)
    previous_major =  previous_major_en(previous_major)
    age = age_en(age)
    iset = prev_institution_en(iset, prevgpa)

    input = []
    input.extend(income)
    input.extend(fos)
    input.extend(english_score)
    input.extend(previous_major)
    input.extend(age)
    # iset = 0.5 # TODO: REMOVE
    iset = iset / 100
    input.extend(minmax_sem1(iset, prevgpa, sem1cre).ravel())
    input = np.array([ input ])
    #print("shape:", input.shape)
    #print(input)
    print(input)

    with semester1_graph.as_default():
        prediction = semester1_predictor.predict(input)
    return prediction

def predict_sem2(income, fos, english_score, previous_major, age, leftwith1, iset, prevgpa, sem1cre, sem1gpa, sem2cre):
    income = nationality_en(income)
    fos = field_of_study_en(fos)
    english_score = english_score_en(english_score)
    previous_major =  previous_major_en(previous_major)
    age = age_en(age)
    iset = prev_institution_en(iset, prevgpa)
    leftwith1 = ip_lw(leftwith1)

    input = []
    input.extend(income)
    input.extend(fos)
    input.extend(english_score)
    input.extend(previous_major)
    input.extend(age)
    input.extend([ leftwith1 ])
    # iset = 0.5 # TODO: REMOVE
    iset = iset / 100
    input.extend(minmax_sem2(iset, prevgpa, sem1cre, sem1gpa, sem2cre).ravel())
    input = np.array([ input ])
    #print("shape:", input.shape)
    #print(input)
    with semester2_graph.as_default():
        prediction = semester2_predictor.predict(input)
    return prediction

def predict_sem3(age, income , fos, english_score, previous_major, leftwith1, leftwith2, iset, prevgpa, sem1cre, sem1gpa, sem2cre,sem2gpa,sem3cre):
    income = nationality_en(income)
    fos = field_of_study_en(fos)
    english_score = english_score_en(english_score)
    previous_major =  previous_major_en(previous_major)
    age = age_en(age)
    iset = prev_institution_en(iset, prevgpa)
    leftwith1 = ip_lw(leftwith1)
    leftwith2 = ip_lw(leftwith2)

    input = []
    input.extend(age)
    input.extend(income)
    input.extend(fos)
    input.extend(english_score)
    input.extend(previous_major)
    input.extend([ leftwith1 ])
    input.extend([ leftwith2 ])
    # iset = 0.5 # TODO: REMOVE
    iset = iset / 100
    input.extend(minmax_sem3(iset, prevgpa, sem1cre, sem1gpa, sem2cre, sem2gpa, sem3cre).ravel())
    input = np.array([ input ])
    #print("shape:", input.shape)
    #print(input)

    with semester3_graph.as_default():
        prediction = semester3_predictor.predict(input)
    return prediction

def predict_sem4(age, fos, english_score, previous_major, leftwith2, leftwith3, iset , prevgpa, sem1cre, sem1gpa, sem2cre, sem2gpa, sem3cre ,sem3gpa, sem4cre):
    fos = field_of_study_en(fos)
    english_score = english_score_en(english_score)
    previous_major =  previous_major_en(previous_major)
    age = age_en(age)
    iset = prev_institution_en(iset, prevgpa)
    leftwith2 = ip_lw(leftwith2)
    leftwith3 = ip_lw(leftwith3)

    input = []
    input.extend(age)
    input.extend(fos)
    input.extend(english_score)
    input.extend(previous_major)
    input.extend([ leftwith2 ])
    input.extend([ leftwith3 ])
    # iset = 0.5 # TODO: REMOVE
    iset = iset / 100
    input.extend(minmax_sem4(iset, prevgpa, sem1cre, sem1gpa, sem2cre, sem2gpa, sem3cre, sem3gpa, sem4cre).ravel())
    input = np.array([ input ])
    #print("shape:", input.shape)
    #print(input)

    with semester4_graph.as_default():
        prediction = semester4_predictor.predict(input)
    return prediction

# print("sem1prediction", predict_sem1('India','Information Management','6.0','Computer Science','23','VRS','3.3','12'))
# print("sem2prediction", predict_sem2('India','Information Management','6.0','Computer Science','23','T/R + C','VRS','3.3','12','3.13','15'))
# print("sem3prediction", predict_sem3('23','India','Information Management','6.0','Computer Science','T/R + C','T/R + C','VRS','3.3','12','3.13','15','3.5','10'))
# print("sem4prediction", predict_sem4('23','Information Management','6.0','Computer Science','T/R + C','T/R + C','VRS','3.3','12','3.13','15','3.5','10','3.25','3.0'))

