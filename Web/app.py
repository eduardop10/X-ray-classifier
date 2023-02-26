#Actor: Eduardo Pereira
from flask import Flask, render_template, request
import Model.model as model
import os, shutil
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
import os

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates',)

@app.route('/')
def upload_file():
   return render_template('upload.html')
@app.route('/result')
def show_result():
   return render_template('result.html')

@app.route('/uploader', methods = ['POST'])
def upload_file1():
   if request.method == 'POST':
      arrResults= []
      files = request.files.getlist("file")
      for file in files:
          file.save(os.path.join("web/static/uploads/", secure_filename(file.filename)))
          result= model.MakePredictionWithImage(os.path.join("web/static/uploads/", secure_filename(file.filename)))
          result["Name"]=secure_filename(file.filename).split("/")[-1]
          #encode image to base64
          #image = open(file, 'rb')
          #image_read = file.read()
          #result["base64Image"]= base64.encodebytes(file["file"]).decode("ascii")#base64.encodebytes(image_read).decode("ascii")
          #print(str(secure_filename(file.filename))+":"+str(result))
          arrResults.append(result)

          """
          listResults += '<article class="card-result"><img src="./images/Viral Pneumonia-1345_GRAY.png" alt="Iamgem Analisada" aria-label="Imagem Analisada"><div class="card-result-info"><h1>Nome do Arquivo: <span>{}</span></h1><ul area-label="Resultado da Análise"><li>Resultado: <span> {}</span></li><li>Porcentagem de Classificação: <span>{}</span></li></ul></div></article>'.format(file.filename, result["Result"], result['NormalProbPercent'] if result["Result"] == "Normal" else result['CovidProbPercent'])
          """
          print(result)
      return render_template('result.html',arrResults= arrResults)

if __name__ == '__main__':
   app.run(debug = True)

