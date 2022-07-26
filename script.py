import os
import pandas as pd
import openpyxl
import numpy as np

def get_files(path):
    drive_path = 'C:\\Users\\Andrew\\Documents\\Arizona'
    path_list = []
    print(path)
    #Walk through dir and get the paths of all the csv files. Append to list
    for root, dirs, files in os.walk(path):
            # print(os.listdir(dirs)[0])
            count = 0 
            for name in files:
                if name.startswith("00") and (name.endswith('.XLSX') | name.endswith('.XLS')):
                    #The first file in directory contains the information we want
                    count+=1
                    #Only save path if count = 1
                    if count == 1:
                        path_list.append(os.path.join(root, name))
                    else:
                        continue
            
    return path_list

#Main function that will call all other functions. Takes path from app.py (GUI)
def controller(path):
    print(path)
    files = get_files(path)
    # df = clean_oofr(files)
    cheat_sheet(files)



def clean_oofr(files):

    #To hold list of dicts
    matrix = []
    for file in files:
        table = {}
        #Make sure file can be opened.
        try:
            temp = pd.read_excel(file)
        except Exception as e:
            print(e)
            continue
        if 'F/A' in temp.columns:
            table['FA count'] = temp['F/A'].count()
        elif 'FA' in temp.columns:
            table['FA count'] = temp['FA'].count

        if 'Builder' in temp.columns:
            table['Builder'] = temp['Builder'].values[0]
        elif 'BUILDER' in temp.columns:
            table['Builder'] = temp['BUILDER'].values[0]
        
        if 'Subdivision' in temp.columns:
            table['Subdivision'] = temp['Subdivision'].values[0]
        elif 'SUBDIVISION' in temp.columns:
            table['Subdivision'] = temp['SUBDIVISION'].values[0]

        matrix.append(table)

    df = pd.DataFrame(matrix)

    df['FA count'].fillna(0, inplace=True)
    df.fillna("No Information Available", inplace=True)

    df.to_csv('oofr_stats.csv', index=False)

def cheat_sheet(files):
    matrix = []
    for file in files:
        table = {}
        #Make sure file can be opened.
        try:
            temp = pd.read_excel(file,sheet_name=1)
            
        except Exception as e:
            print(e)
        # print(temp)
        temp = temp.astype(str)
        
        col = temp.loc[temp.isin(['Builder:']).any(axis=1)].index.tolist()

        #Data is disorganized, have to find the tables within the sheet and append
        #based on key-word (builder, Homes, clients)
        for ind,column in enumerate(temp.columns):
            for r,row in enumerate(temp[column]):
                if 'Builder' in str(row):
                    table['Builder'] = temp.iloc[r, ind+1]
                if 'of Homes' in str(row):
                    print(row)
                    table['Number of Homes'] = temp.iloc[r, ind+1]
                if 'Clients' in str(row):
                    table['Total Clients'] = temp.iloc[r, ind+1]
        #Append temp dict to master list
        matrix.append(table)            
        print(matrix)           
            

 


