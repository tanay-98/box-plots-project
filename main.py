from website import create_app


app = create_app()

if __name__=="__main__":
    #TODO - turn debug mode off
    app.run(debug=True)