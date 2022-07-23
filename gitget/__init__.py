import dotenv

if dotenv.find_dotenv():
    print("Loading dotenv")
    dotenv.load_dotenv(override=True)
