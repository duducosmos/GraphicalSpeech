#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
GraphicalSpeech: Create a graphical using data via speech recognition

copyright : Eduardo dos Santos Pereira. 2012.

    GraphicalSpeech is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.
    PyGraWC is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = 'Eduardo dos Santos Pereira'
__email__ = 'pereira.somoza@gmail.com'
__data__ = '28/02/2012'
__license__ = 'General Public License - http://www.gnu.org/licenses/'

import android

from pygooglechart import XYLineChart
from pygooglechart import Axis

import os
import time

try:
    os.chdir("/mnt/sdcard/graphicospeech/")
except:
    os.mkdir("/mnt/sdcard/graphicospeech/")
    
droid = android.Android()




myLayout = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/linearLayout1"
    android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    android:orientation="vertical" >

    <LinearLayout
        android:id="@+id/linearLayout2"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="1.09"
        android:background="#ff000000" >
        
        <TextView
            android:id="@+id/textView3"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="GraphicalSpeech    "
            android:textAppearance="?android:attr/textAppearanceSmall"/>
            
        <Button
            android:id="@+id/button2"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Sobre" />

        <Button
            android:id="@+id/button4"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="GoogleDocs" />

    </LinearLayout>

        <RelativeLayout
            android:id="@+id/relativeLayout1"
            android:layout_width="wrap_content"
            android:layout_height="match_parent"
            android:layout_weight="1.09" >
            
            <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
                android:id="@+id/background"
                android:orientation="vertical"
                android:layout_width="match_parent"
                android:layout_height="match_parent"
                android:background="#ff000000">
            <TextView
                android:id="@+id/textview0"
                android:layout_width="fill_parent"
                android:layout_height="wrap_content"
                android:text="Nome do arquivo"
                android:gravity="center" />
            <EditText
                android:id="@+id/textedit0"
                android:layout_width="fill_parent"
                android:layout_height="wrap_content"
                android:textSize="18sp"
                android:gravity="center"/>
            <TextView
                android:id="@+id/textview1"
                android:layout_width="fill_parent"
                android:layout_height="wrap_content"
                android:text="Total de pontos"
                android:gravity="center" />
            <EditText
                android:id="@+id/textedit1"
                android:layout_width="fill_parent"
                android:layout_height="wrap_content"
                android:textSize="18sp"
                android:gravity="center"
                android:inputType="numberDecimal" />
            <Button
                android:id="@+id/button1"
                android:layout_width="fill_parent"
                android:layout_height="wrap_content"
                android:text="Ditar X e Y" />
            <Button
                android:id="@+id/button3"
                android:layout_width="fill_parent"
                android:layout_height="wrap_content"
                android:text="Sair"
                android:gravity="center" />
            <TextView
                android:id="@+id/textview2"
                android:layout_width="fill_parent"
                android:layout_height="wrap_content"
                android:text="Plot"
                android:gravity="center" />
            <ImageView
                android:id="@+id/image1"
                android:layout_width="fill_parent"
                android:layout_height="wrap_content" />

        </LinearLayout>
    </RelativeLayout>

</LinearLayout>
"""

def spreadsheetSaver(tableName, dados):

    import gdata.spreadsheet.text_db as gst

    email = droid.dialogGetInput("Entre com o seu email",\
                                 "Qual o email para conectar ao google Docs? "\
                                 )
    email = email.result

    password = droid.dialogGetPassword("Digite a senha",\
                                       "Senha para conectar ao google Docs")
    password = password.result

    
    droid.dialogCreateAlert("Google Docs","Salvando dados no Google Docs, aguarde")
    droid.dialogShow()
    client = gst.DatabaseClient(username=email,password=password)
    database = client.CreateDatabase(tableName)
    table = database.CreateTable('pontos', ['x','y'])

     

    for linhas in dados:
        record = table.AddRecord(linhas)
    droid.dialogDismiss()
        

def dicDadosGenerate(dadosx,dadosy):
    listDicDados = []
    for i in range(len(dadosx)):
        dic = {}
        dic['x'] = str(dadosx[i])
        dic['y'] = str(dadosy[i])
        listDicDados.append(dic)
    return listDicDados
    

def sobre():
    mensagem = """
    GraphicalSpeech: Ditar dados x e y.
    Clique no botao GoogleDocs para salvar os 
    dados em uma tabela na sua conta do google docs
    Desenvolvido por : Eduardo dos Santos Pereira.
    email: pereira.somoza@gmail.com
    """
    droid.dialogCreateAlert("Sobre", mensagem)
    droid.dialogSetPositiveButtonText("Sair")
    droid.dialogShow()
    
def catDado():
    cont = 0
    while True:
        point = droid.recognizeSpeech().result
        
        try:
            
            
            point = float(point)
            droid.dialogCreateAlert("Verificar Valor de Entrada",\
                                    "O Valor ditado foi: %s" %point)
            droid.dialogSetPositiveButtonText("OK")
            droid.dialogSetNegativeButtonText("Reditar")
            droid.dialogShow()
            resposta = droid.dialogGetResponse().result
            if resposta['which'] == 'positive':
                return point
            else:
                droid.ttsSpeak("Diga um numero")
        except:
            cont += 1
            droid.ttsSpeak("Diga um numero")
            if(cont == 3):
                droid.dialogCreateAlert("Falha",
                """Falha no reconhecimento dos dados.
                Tentar novamente: OK
                Ou clique em Sair""")
                droid.dialogSetPositiveButtonText("OK")
                droid.dialogSetNegativeButtonText("Sair")
                droid.dialogShow()
                resposta = droid.dialogGetResponse().result
                if resposta['which'] == 'positive':
                    cont = 0
                else:
                    return None
            
def MaxMindado(dado):
    x0 = dado[0]
    x1 = dado[0]
    for ntmp in dado:
        if(ntmp > x0):
            x0 = ntmp
        if(ntmp < x1):
            x1 = ntmp
    return x0,x1
        

def dadosSpeech(npoints):
    data = []
    for i in range(npoints):
        point = catDado()
        if( point != None):
            data.append(point)
        else:
            return None
    return data
        
        

def grafico(fileName,datax,datay):
    """Graphical generate"""
    
    droid.dialogCreateAlert("Gerando Grafico","Aguarde a geracao do gráfico")
    droid.dialogShow()
    
    
    
    if(len(datax) != 0):
        xmax, xmin = MaxMindado(datax)
        ymax, ymin = MaxMindado(datay)
        
        if(xmax != xmin):
            deltax = (xmax -xmin)/10.0
        else:
            droid.makeToast("Erro: falta definir eixo x")
            return
        if(ymax != ymin):
            deltay = (ymax - ymin)/10.0
        else:
            droid.makeToast("Erro: Falta definir dados de y")
            return
            
        left_axis = [datax[0] + deltax*i for i in range(11)]
        bottom_axis = [datay[0] + deltay*i for i in range(11)]
    chart = XYLineChart(500, 400,
                       x_range=(xmin,xmax),
                       y_range=(ymin,ymax))
    chart.add_data(datax)
    chart.add_data(datay)
        
    chart.set_axis_labels(Axis.LEFT,[ymin,ymax])
    chart.set_axis_labels(Axis.BOTTOM,[xmin,xmax])
    chart.download('/mnt/sdcard/graphicospeech/'+fileName)  
    droid.fullSetProperty("image1","src",\
                           "file:///mnt/sdcard/graphicospeech/"+fileName)
    
    droid.dialogDismiss()
     
    
    
def eventLoop():
    lisDicDados = None
    while True:
        event = droid.eventWait().result
        key = event["data"]
        if key.has_key("key"):
            if key["key"] == "4":
                return

        if event["name"] == "click":
            id = event["data"]["id"]
            resultado = ""
            r1 = False
            datay = None
            datax = None


            if id == "button1":                
                nPontos = droid.fullQueryDetail("textedit1").result
                nPontos = int(nPontos["text"])
                fileName = droid.fullQueryDetail("textedit0").result
                fileName = fileName["text"]
                
                if(nPontos != ""):
                    droid.dialogCreateAlert("Dados y","Entrar dados de y")
                    droid.dialogSetPositiveButtonText("O.K.")
                    droid.dialogShow()
                    resp1 = droid.dialogGetResponse().result
                    if resp1['which'] == 'positive':
                        datay = dadosSpeech(nPontos)

                    if( datay != None):
                        droid.dialogCreateAlert("Dados x","Entrar dados de x")
                        droid.dialogSetPositiveButtonText("O.K.")
                        droid.dialogShow()
                        resp2 = droid.dialogGetResponse().result
                    
                        if resp2['which'] == 'positive':
                            datax = dadosSpeech(nPontos)
                        if(datax != None):
                            lisDicDados = dicDadosGenerate(datay,datax)
                            r1 = True
                else:
                    resultado = "Entre com o numero de pontos"
                    droid.makeToast(resultado)
                    droid.ttsSpeak(resultado)
                if(r1 == True ):
                    if(fileName != ""):
                        grafico(fileName,datax,datay)    

                droid.fullSetProperty("textview2","text",resultado)

            elif id == "button2":
                sobre()

            elif id == "button4":
                if(lisDicDados):
                    spreadsheetSaver("GraphicalSpeech", lisDicDados)
                else:
                    droid.dialogCreateAlert("Dados", "Falta entrar Dados")
                    droid.dialogSetPositiveButtonText("O.K")
                    droid.dialogShow()

            elif id == "button3":
                return

        elif event["name"] == "screen":
            if envent["data"] == "destroy":
                return


droid.fullShow(myLayout)
eventLoop()
droid.fullDismiss()
