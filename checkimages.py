import os
import sys
from os import listdir
from PIL import Image
import mysql.connector as database

#Environment variables / default values
DB_HOST = os.getenv('DB_HOST','localhost')
DB_USER = os.getenv('DB_USER','root')
DB_PASSWORT = os.getenv('DB_PASSWORT','secret')
FILE_PATH = os.getenv('FILE_PATH','files')
patharray = [FILE_PATH+"/folder1",FILE_PATH+"/folder2",FILE_PATH+"/folder3",FILE_PATH+"/folder4"]

# Connect to MariaDB Platform
try:
    connection = database.connect(
        user=DB_USER,
        password=DB_PASSWORT,
        host=DB_HOST,
        database="testdatabase"
    )
except database.Error as e:
    print("Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


def Is_id_checked(id):
  print("Check flag for Upload " + id)
  statement = "SELECT uploadid, filechecked FROM uploads WHERE uploadid=" + id
  cursor = connection.cursor()
  cursor.execute(statement)
  for (uploadid) in cursor:
    return uploadid[1]


def Set_id_checked(id):
  print("Upload " + id + " is checked. Update flag")
  statement = "UPDATE uploads SET filechecked = 1 WHERE uploadid = " + id
  cursor = connection.cursor()
  cursor.execute(statement)
  connection.commit();

def check_all():
  for path in patharray:
    for filename in listdir(path):
      if(filename=="corrupt"):
        break
      if(Is_id_checked(filename[:-4]) == 0):
        imagepath = path + '/' + filename
        if filename.endswith('.gif') or filename.endswith('.png') or filename.endswith('.jpg'):
          try:
            img = Image.open(imagepath) 
            img.verify()
            Set_id_checked(filename[:-4])
          except (IOError, SyntaxError) as e:
            print('Bad file:', imagepath)
            #os.remove(imagepath)
            os.replace(path + '/' + filename, path + '/' + "corrupt/" + filename)
        if filename.endswith('.mp4'):
          result = os.system("ffmpeg -v error -i " + imagepath + ' -f null ' + './' + filename + ' >/dev/null 2>&1')
          if result != 0:
            print('Bad file:', imagepath)
            ##os.remove(imagepath)
            os.replace(path + '/' + filename, path + '/' + "corrupt/" + filename)
          else:
            Set_id_checked(filename[:-4])
            
check_all()

