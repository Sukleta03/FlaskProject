from app import create_app

app = create_app('main')

if __name__ == '__main__':
    app.run(debug=True)