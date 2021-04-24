def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
 
    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        if len(str(text.description)) <= 1: continue
        # print("Searching for: " + str(text.description))
        if try_rh_search(str(text.description)):
            # print(str(text.description).lower().strip())
            return str(text.description).lower().strip() # will check the robinhood ticker search api and if it finds a match, then returns
        else:
            continue

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def text_detect(content):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    # with io.open(path, 'rb') as image_file:
    #     content = image_file.read()

    image = vision.Image(content=content)
 
    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        if len(str(text.description)) <= 1: continue
        # print("Searching for: " + str(text.description))
        if try_rh_search(str(text.description)):
            # print(str(text.description).lower().strip())
            return str(text.description).lower().strip() # will check the robinhood ticker search api and if it finds a match, then returns
        else:
            continue

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def try_rh_search(text):
    import robin_stocks.robinhood as rh
    # import robin_stocks.gemini as gem
    # import robin_stocks.tda as tda
    # import pprint
    login = rh.login("roshan.poduval@gmail.com", "testpassword579")
    stock = None
    stock = rh.stocks.find_instrument_data(text)
    if stock[0] is None:
        return False
    else:
        # stock = stock[0]['symbol']
        # stockPrice = ' '.join(rh.stocks.get_latest_price(stock))
        # print("Current price of " + stock + ": $" + stockPrice)
        # print("The general information about the " + stock + " stock:")
        # # pprint.pprint(rh.stocks.get_fundamentals(stock))
        return True


def main():
    # detect_text("sample.jpg")
    # assert detect_text("burberry.jpg") == 'burberry' # seems like skewed text also has a problem ## output = burberr
    
    assert detect_text("subway.jpg") == None # since subway is not a publically traded company
    assert detect_text("mcdonalds.jpg") == "mcdonald's"
    # assert detect_text("starbucks.png") == "starbucks" # seems like curved text causes problems ## output = coffee
    assert detect_text("amazon.jpg") == "amazon"
    assert detect_text("microsoft.jpg") == "microsoft"


if __name__ == "__main__":
    # execute only if run as a script
    main()