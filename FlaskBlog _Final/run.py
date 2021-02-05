#python run.py

from flaskblog import create_app

#creat application:
app = create_app() #could pass in configuration, default is current settings

if __name__ == '__main__':
    app.run(debug=True)
