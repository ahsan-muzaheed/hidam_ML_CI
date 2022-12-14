# -*- coding: utf-8 -*-
"""PP-RNN+GRU+LSTM- model5

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16efGiDOV0hnMyOjzojya9mX6fH5XpjHC
"""
#python C:\0.ml\p.py
import json
import pandas as pd
import numpy as np
from numpy import array
from numpy import hstack
#from keras.models import Sequential
#from keras.layers import LSTM
#from keras.layers import Dense
#import scipy.stats as st
import tensorflow as tf
from sklearn.metrics import mean_squared_error
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from sklearn.model_selection import train_test_split

from datetime import datetime
from sklearn import preprocessing
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, confusion_matrix, adjusted_rand_score

import torch
import torch.nn as nn
#import matplotlib.pyplot as plt
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = 'cpu'
print(device)

import json
import sys
# Covert JSON to Dictionsary
def jsonToDict(jsonString):

    dictionary = json.loads(jsonString)
    # print(aDict)
    # print(aDict["splitMethod"])
    # print(aDict["range"])

    return dictionary



# Create txt file to store results
#txtCreater()
# txtAppender("Output from downstrem ML")
# txtAppender("------------------------")
# Convert JSON input to Dictionary

if len(sys.argv) > 1:
    print("sys.argv[1]: ",sys.argv[1])
    jsonDict = jsonToDict(sys.argv[1])
    
    
    
    print("jsonDict[labelFile]: ",jsonDict["labelFile"])
    print("jsonDict[inputsFile]: ",jsonDict["inputsFile"])
    
   







#from google.colab import drive
#drive.mount('/content/MyDrive/')
#4/1AX4XfWj4gZil2kGwsKoDw0jn6UuUv1lyfMwtQPErYTPJe9_uq8OKay-tj0I

#!wget https://www.dropbox.com/s/uy58al2rwf6yn9u/labels_1540_4classes_icmla_21.pck
#!wget https://www.dropbox.com/s/4bt5ugb9rimbrgx/mvts_1540_icmla_21.pck

#from google.colab import files
#uploaded = files.upload()

labelFile="labels_1540_4classes_icmla_21.pck"
inputsFile="mvts_1540_icmla_21.pck"


labelFile=jsonDict["labelFile"]#"Sampled_labels.pck"
inputsFile=jsonDict["inputsFile"]#"Sampled_inputs.pck"
#inputsFile="C:\\Users\\XXXX\\Desktop\\Sampled_inputs.pck"
#labelFile="C:\\Users\\XXXX\\Desktop\\Sampled_labels.pck"

import pickle

def load(file_name):
    with open(file_name, 'rb') as fp:
        obj = pickle.load(fp)
    return obj

Sampled_inputs=load(inputsFile)
Sampled_labels=load(labelFile)
print(Sampled_inputs.shape)
print(type(Sampled_inputs[0]))
#print(Sampled_inputs)

temp=Sampled_inputs[0].T
df = pd.DataFrame(temp)
  #print(temp.shape)

df

temp=Sampled_inputs[0]
#print(temp)
df = pd.DataFrame(temp)
trainData=Sampled_inputs
trainLebel=Sampled_labels
print("trainData.shape: ",trainData.shape)
print("trainLebel.shape: ",trainLebel.shape)

"""# New Section"""

#four-class problem {X, M, B/C, Q}
print("np.unique(trainLebel): ",np.unique(trainLebel))

df

temptrainData=np.empty([1540,60, 33])
n=len(trainData)
for l in range(0, n):
  temp=trainData[l]
  #print(temp)
  #temp=np.transpose(temp)
  temp=temp.T
  #print(temp.shape)
  #print(temp)
  temptrainData[l,:,:]=temp
  n=n+1
  #np.append(temptrainData, temp)
  #print(temptrainData)

#print(temptrainData.shape)
#print(trainData.shape) 
trainData=temptrainData
print("trainData.shape: ",trainData.shape)
#print(trainData[0])

temp=trainData[0]
#print(temp)
df = pd.DataFrame(temp)
#df=pd.DataFrame.from_dict(trainData)
trainData222=trainData

df

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
print(trainData.shape)

print(type(trainData))
npArrays=[]
for l in range(0, len(trainData)):
  trainData_std = sc.fit_transform(trainData[l])
  #trainData_std = trainData_std.astype(np.float64)
  #print(type(trainData_std[0][0]))
  npArrays.append(trainData_std)


print(type(npArrays))
arr = np.asarray(npArrays)
print(type(arr))
trainData=arr
df = pd.DataFrame(trainData[0])

#print(npArrays.shape)

df

INPUT_DIM = 1320
HIDDEN_DIM = 64
NUM_TS = 60
NUM_CLASSES = 4
#NUM_CLASSES = 1
num_layers = 1 #number of stacked lstm layers
hidden_size=HIDDEN_DIM

INPUT_DIM = 33
HIDDEN_DIM = 33
NUM_TS = 60
NUM_CLASSES = 4


class LSTM_MVTS_LRN(nn.Module):
  def __init__(self, input_dim, hidden_dim, num_steps): #input_dim = 33, hidden_dim = 33
    super(LSTM_MVTS_LRN, self).__init__()
    self.input_dim = 33#input_dim
    self.hidden_dim = 33#hidden_dim
    self.output_dim = 33#input_dim


    self.lstm1 = nn.LSTM(33, 33) #encoder
    self.lstm2 = nn.LSTM(33, 33) #decoder


    #self.lstm1 = nn.RNN(33, 33) #encoder
    #self.lstm2 = nn.RNN(33, 33) #decoder

    #self.lstm1 = nn.GRU(33, 33) #encoder
    #self.lstm2 = nn.GRU(33, 33) #decoder


    self.num_steps = num_steps 
    #self.hidden2class = nn.Linear(hidden_dim, num_classes)
  def forward(self, mvts):
    #print("model():","mvts.shape: ",mvts.shape)#[40, 33]
    #input single mvts (60, 33); output class probability vector (1,4)
    
    input1=mvts.view(len(mvts), 1, -1)
    #print("model():","input1.shape: ",input1.shape) #[40, 1, 33]
   
    lstm_out, _ = self.lstm1(input1) #mvts.shape: (40, 33); len(mvts)=40; new shape: (40, 1, 33); lstm_out1 --> (40, 128)
    #print("model():","lstm_out.shape: ",lstm_out.shape) #[40, 1, 33]

    lstm_out2 = lstm_out[:, -1, :] 
    #print("model():","lstm_out2.shape: ",lstm_out2.shape) #[40, 33]

    lstm_out_of_lastRow = lstm_out[len(lstm_out2)-1] #vector of 40th timestep : [1,128]
    #print("model():","lstm_out_of_lastRow.shape: ",lstm_out_of_lastRow.shape)#(([1, 33]

 
    num=20
    predicted_timestamp_vectors = torch.zeros((num,33)) #
    #print("predicted_timestamp_vectors ",predicted_timestamp_vectors.shape)#(([20, 33]
    for i in range(num):
      #last_lstm2_out =  self.lstm2(lstm_out_of_lastRow) #vecotr of 41st timestamp: [1,33]
      
      input2=lstm_out_of_lastRow.view(len(lstm_out_of_lastRow), 1, -1)
      #print("model():","input2.shape: ",input2.shape) #[1, 1, 33]

      last_lstm2_out, _ = self.lstm2(input2)
      #print("last_lstm2_out-",i, last_lstm2_out.shape)#([1, 1, 33]
      last_lstm2_out2 = last_lstm2_out[:, -1, :] 
      #print("model():",i,"last_lstm2_out2.shape: ",last_lstm2_out2.shape) #[1, 33]
      
      predicted_timestamp_vectors[i, :] = last_lstm2_out2
      lstm_out_of_lastRow=last_lstm2_out2

      #h, o = self.lstm2(input2)
      #reshape
      #input2 = h
      #save o



    #lstm_out2, _ = self.lstm2(lstm_out1.view(len(lstm_out1), 1, -1)) #lstm_out1.shape: (40, 128); len(mvts)=40; new shape: (40, 1, 128); lstm_out2 --> (40, 128) -> can use later 
    #lstm_out2_clipped = lstm_out[0:20,:] -> can use later
    #return lstm_out2_clipped 
    #return lstm_out
    #print("model() predicted_timestamp_vectors.shape: ",predicted_timestamp_vectors.shape) #[1, 33]
    return predicted_timestamp_vectors

def showBarChart(test_no,losses,label,xlabel,ylabel):
              import matplotlib.pyplot as plt
              #print("showCurve() test_no:",test_no)
              #print(losses)
              #plt.plot(test_no, losses, label = 'Test error')
              plt.bar(test_no, losses, label = label)
              plt.xlabel(xlabel)
              plt.ylabel(ylabel)
              plt.show()

def showBarChart2(test_no2,losses2,label2):
              import matplotlib.pyplot as plt2
              #print("showCurve() test_no:",test_no)
              print(losses2)
              #plt.plot(test_no, losses, label = 'Test error')
              plt2.bar(test_no2, losses2, label = label2)
              plt2.xlabel("epoch")
              plt2.ylabel("losses")
              plt2.show()

def showCurve(test_no,losses,label):
              import matplotlib.pyplot as plt
              #print("showCurve() test_no:",test_no)
              #print(losses)
              plt.plot(test_no, losses, label = label)
              plt.xlabel("epoch")
              plt.ylabel("losses")
              plt.show()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def doClassSpecificCalulcation(Accuracy,trainLebel,classification_report_dict):
  print('\np.mean(Accuracy) :',np.mean(Accuracy))
  print('\np.std(Accuracy) :',np.std(Accuracy))
  print('\n33333333 p.mean np.std(Accuracy) :     ',np.round(np.mean(Accuracy),2),"+-",np.round(np.std(Accuracy),2) )
  for j in range( len(np.unique(trainLebel)) ):
    print('\n\n\n\nclass :',j) 
    precision=[]
    recall=[]
    f1_score=[]
    for i in range(len(classification_report_dict)):
      report=classification_report_dict[i]
      #print('classification_report : \n',report) 
      temp=report[str(j)]['precision'] 
      precision.append(temp)

      temp=report[str(j)]['recall'] 
      recall.append(temp)

      temp=report[str(j)]['f1-score'] 
      f1_score.append(temp)

    print('\np.mean(precision) \t p.mean(recall) \t p.mean(f1_score) :') 


    print(np.mean(precision)) 
    print(np.mean(recall)) 
    print(np.mean(f1_score))

    print('\np.mean p.std(precision) \tp.mean  p.std(recall) \tp.mean  p.std(f1_score) :')

    print(np.round(np.mean(precision),2),"+-",np.round(np.std(precision),2) )
    print(np.round(np.mean(recall),2),"+-",np.round(np.std(recall),2) )
    print(np.round(np.mean(f1_score),2),"+-",np.round(np.std(f1_score),2) )

def RMSELoss(yhat,y): #https://discuss.pytorch.org/t/rmse-loss-function/16540
    return torch.sqrt(torch.mean((yhat-y)**2))

def doTrainingForThisMVTS(mvts,model,loss_function):
            loss_MAE = nn.L1Loss()
            loss_MSE = nn.MSELoss()
            
            #print("mvts no:",i ,"input mvts.shape: ",mvts.shape)
            #df = pd.DataFrame(mvts)
            #print(df)
            mvts = torch.from_numpy(mvts).float()
            mvts_input = mvts[0:40,:]
            df_mvts_input = pd.DataFrame(mvts_input)
            #print(df_mvts_input)

            #mvts = mvts.to(device)#print(mvts.is_cuda)
            #mvts = mvts.view(mvts.size(0), -1)
            #print("mvts no:",i ,"df_mvts_input.shape: ",df_mvts_input.shape)
            #print("mvts no:",i ,"mvts_input.shape: ",mvts_input.shape)
            Predicted_20_rows = model(mvts_input) #Predicted_20_rows -> [20, 33]
            #print("mvts no:",i ,"Predicted_20_rows.shape: ",Predicted_20_rows.shape)


            target = mvts[40:60,:]
            #df_target = pd.DataFrame(target)

            #print("mvts no:",i ,"target.shape: ",target.shape)
            target = torch.from_numpy(np.array(target)).float()
            #print("mvts no:",i ,"target.shape: ",target.shape)
            loss_MSE_total=0
            loss_RMSE_total=0
            loss_MAE_total=0
           
            for k in range(20):
               tttt = loss_MSE(Predicted_20_rows[k], target[k]) #distance calculate
               tttt2 = loss_MAE(Predicted_20_rows[k], target[k]) #distance calculate
               tttt3 =torch.sqrt(tttt)
              
               
               #print("row no:",k ," loss: ",tttt)
               loss_MSE_total=loss_MSE_total+tttt
               loss_RMSE_total=loss_RMSE_total+tttt3
               loss_MAE_total=loss_MAE_total+tttt2
            return loss_MSE_total ,loss_RMSE_total,loss_MAE_total

import random
import matplotlib.pyplot as plt
#losses = []

losses_test = []
test_no_test = []
df_mvts_input=[]
df_target=[]

test_totalLoss_epoch=[]
train_totalLoss_epoch=[]

train_mse_epoch=[]
test_mse_epoch=[]

train_rmse_epoch=[]
test_rmse_epoch=[]

train_mae_epoch=[]
test_mae_epoch=[]


loss_MAE = nn.L1Loss()
loss_MSE = nn.MSELoss()

epochs=[]
def doLstmBasedCalculations():
    HIDDEN_DIM=20*33
    num_masterIteration=1

    print("trainData.shape: ",trainData.shape)
    X_train, X_test, y_train, y_test = train_test_split(trainData, trainLebel, test_size=0.3, random_state=0,shuffle = False)
    print("X_train.shape X_test.shape y_train.shape y_test.shape ",X_train.shape, X_test.shape ,y_train.shape, y_test.shape)
 
    classification_report_dict=[]
    Accuracy=[]
    for masterIteration in range(num_masterIteration):
        #print("\nmasterIteration HIDDEN_DIM : ",masterIteration, HIDDEN_DIM)
        #print(bcolors.WARNING + "\nmasterIteration :" + bcolors.WARNING,masterIteration)
        #random_state=random.randint(42, 100)
        #print("random_state: ",random_state)


        model = LSTM_MVTS_LRN(INPUT_DIM, 
                              #hds,
                              660, 
                              NUM_CLASSES)
        #loss_function = nn.NLLLoss()
        #optimizer = optim.SGD(model.parameters(), lr=0.01)

        loss_function = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01) 

        num_mvts_to_process =trainData.shape[0]# X_train.shape[0] #numTrain#200 #
        #num_mvts_to_process=20
        numEpochs =500
        numEpochs =2 
        model.zero_grad()
        #train
       
        for epoch in range(numEpochs):
          print("\n masterIteration: ",masterIteration, "     epoch: ",epoch)
          totalLoss_epoch=0
          total_rmseLoss_epoch=0
          total_maeLoss_epoch=0


          #loss_values = []
          #running_loss = 0.0

          
         
          endMvts=X_train.shape[0]
          losses=[]
        
          train_no = []
          k=0
          for i in range(0,endMvts):
          #for i in range(0,2):
            model.zero_grad()
            model.to(device)
            mvts = trainData[i,:,:]
            
            loss_total ,loss_RMSE_total,loss_MAE_total=doTrainingForThisMVTS(mvts,model,loss_function)

          #for mean
            totalLoss_epoch=totalLoss_epoch+loss_total
            total_rmseLoss_epoch=total_rmseLoss_epoch+loss_RMSE_total
            total_maeLoss_epoch=total_maeLoss_epoch+loss_MAE_total


          #for graph
            loss_total2=loss_total.detach().numpy()
            #print("train mvts no:",i,"loss_total2",loss_total2)
            losses.append(loss_total2)    
            k=k+1
            train_no.append(k)

            


            #print("------- >")
            #print("------- >")
            #loss.backward()

            

            loss_total.backward(retain_graph=True)
            optimizer.step()
          #showCurve(test_no,losses,"tarining")   
          #showBarChart(train_no,losses,"tarining","epoch train- "+str(epoch),"losses train- "+str(epoch))
          #print("\n masterIteration: ",masterIteration, "     epoch: ",epoch," tarining totalLoss_epoch:",totalLoss_epoch)
          #print(" tarining totalLoss_epoch:",totalLoss_epoch)
          train_totalLoss_epoch.append(totalLoss_epoch.detach().numpy())        
          #print("\n test")


          mse=totalLoss_epoch.detach().numpy()/endMvts
          print("train mse:",mse)
          train_mse_epoch.append(mse)
          
          rmse=total_rmseLoss_epoch.detach().numpy()/endMvts
          print("train rmse:",rmse)
          train_rmse_epoch.append(rmse)

          mae=total_maeLoss_epoch.detach().numpy()/endMvts
          print("train mae:",mae)
          train_mae_epoch.append(mae)
         

          with torch.no_grad():
            losses_test=[]
            test_no2=[]
            loss_total_test=0

            totalLoss_epoch_test=0
            total_rmseLoss_epoch_test=0
            total_maeLoss_epoch_test=0

            j=0
            endMvts=X_test.shape[0]
            for i in range(0,endMvts):
            #for i in range(0,2):
              #model.zero_grad()
              #model.to(device)

              mvts = trainData[i,:,:]
              #print("mvts no:",i ,"input mvts.shape: ",mvts.shape)
              #df = pd.DataFrame(mvts)
              #print(df)
              mvts = torch.from_numpy(mvts).float()
              mvts_input = mvts[0:40,:]
              df_mvts_input = pd.DataFrame(mvts_input)
              #print(df_mvts_input)

              #mvts = mvts.to(device)#print(mvts.is_cuda)
              #mvts = mvts.view(mvts.size(0), -1)
              #print("mvts no:",i ,"df_mvts_input.shape: ",df_mvts_input.shape)
              #print("mvts no:",i ,"mvts_input.shape: ",mvts_input.shape)
              Predicted_20_rows = model(mvts_input) #Predicted_20_rows -> [20, 33]
              #print("test mvts no:",i ,"Predicted_20_rows.shape: ",Predicted_20_rows.shape)


              target = mvts[40:60,:]
              #df_target = pd.DataFrame(target)

              #print("mvts no:",i ,"target.shape: ",target.shape)
              target = torch.from_numpy(np.array(target)).float()
              #print("mvts no:",i ,"target.shape: ",target.shape)
              loss_MSE_total=0
              loss_RMSE_total=0
              loss_MAE_total=0
              for k in range(20):
                tttt = loss_MSE(Predicted_20_rows[k], target[k]) #distance calculate
                tttt3 =torch.sqrt(tttt)
                tttt2 = loss_MAE(Predicted_20_rows[k], target[k]) #distance calculate
               
                #tttt = tttt.item()
                #print("row no:",k ," loss: ",tttt)
                loss_MSE_total=loss_MSE_total+tttt 
                loss_RMSE_total=loss_RMSE_total+tttt3
                loss_MAE_total=loss_MAE_total+tttt2

              loss_total2=loss_MSE_total.detach().numpy()
              #print("test mvts no:",i,"loss_total",loss_total2)
             
              #print("mvts test no:",i,"loss_total",loss_total)
              losses_test.append(loss_total2)
              j=j+1
              test_no2.append(j)
              totalLoss_epoch_test=totalLoss_epoch_test+loss_total
              total_rmseLoss_epoch_test=total_rmseLoss_epoch_test+loss_RMSE_total
              total_maeLoss_epoch_test=total_maeLoss_epoch_test+loss_MAE_total



              


            #print(losses_test)
            #showBarChart(test_no2,losses_test,"testing","epoch test- "+str(epoch),"losses test- "+str(epoch))
            #print("\n masterIteration: ",masterIteration, "     epoch: ",epoch," tarining totalLoss_epoch_test:",totalLoss_epoch_test)
            #print("test totalLoss_epoch_test:",totalLoss_epoch_test)
            test_totalLoss_epoch.append(totalLoss_epoch_test.detach().numpy())


            epochs.append(epoch)
            mse=totalLoss_epoch_test/endMvts
            print("test mse:",mse)
            test_mse_epoch.append(mse)

            rmse=total_rmseLoss_epoch_test/endMvts
            print("test rmse:",rmse)
            test_rmse_epoch.append(rmse)


            mae=total_maeLoss_epoch_test/endMvts
            print("test mae:",mae)
            test_mae_epoch.append(mae)

            #print("test_totalLoss_epoch:",test_totalLoss_epoch)
            #print("train_totalLoss_epoch:",train_totalLoss_epoch)
            #print("epochs:",epochs)



        #showBarChart(epochs,train_totalLoss_epoch,"tarining","epoch(train) ","losses(train)" )           
        #showBarChart(epochs,test_totalLoss_epoch,"testing","epoch(test)" ,"losses(test)")

        #showBarChart(epochs,train_mse_epoch,"tarining","epoch(train) ","mse(train)" )           
        #showBarChart(epochs,test_mse_epoch,"testing","epoch(test)" ,"mse(test)")


        print("train_totalLoss_epoch.mean: ",np.mean(np.where(np.isnan(train_totalLoss_epoch), 0, train_totalLoss_epoch)))
        print("test_totalLoss_epoch.mean: ",np.mean(np.where(np.isnan(test_totalLoss_epoch), 0, test_totalLoss_epoch)))
        
        print("train_mse_epoch.mean: ",np.mean(np.where(np.isnan(train_mse_epoch), 0, train_mse_epoch)))
        print("test_mse_epoch.mean: ",np.mean(np.where(np.isnan(test_mse_epoch), 0, test_mse_epoch)))

        print("train_rmse_epoch.mean: ",np.mean(np.where(np.isnan(train_rmse_epoch), 0, train_rmse_epoch)))
        print("test_rmse_epoch.mean: ",np.mean(np.where(np.isnan(test_rmse_epoch), 0, test_rmse_epoch)))

        print("train_mae_epoch.mean: ",np.mean(np.where(np.isnan(train_mae_epoch), 0, train_mae_epoch)))
        print("test_mae_epoch.mean: ",np.mean(np.where(np.isnan(test_mae_epoch), 0, test_mae_epoch)))

              #print("------- >")
              #print("------- >")
              #loss.backward()

              #print("mvts no:",i ," loss: ",loss.detach().numpy())

              #loss_total.backward(retain_graph=True)
              #optimizer.step()

#startCalulations()
doLstmBasedCalculations()