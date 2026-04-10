#this is just where
from website import create_app
print("running main.py")
app = create_app()

if __name__ == '__main__':
     app.run(debug=True) #default port. owuld be on localhost:5000

