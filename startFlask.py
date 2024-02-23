from src.bot import main
from src.app import app
if __name__ == "__main__":
    app.run(debug=True,host='localhost',port=80)
    # main()