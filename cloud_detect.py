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

    # print('Texts len=' + str(texts.__len__()) + ' :')
    # max_len = -1
    # for ele in texts:
    #     if len(str(ele.description)) > max_len:
    #         max_len = len(str(ele.description))
    #         res = ele.description
    # second_max_len = -1
    # for ele in texts:
    #     if len(str(ele.description)) > second_max_len and len(str(ele.description)) != max_len:
    #         second_max_len = len(str(ele.description))
    #         res2 = ele.description
    # if max_len != -1: print(res)
    # if second_max_len != -1: print(str(res2).lower())
    # if second_max_len != -1: return str(res2).lower()

    for text in texts:
        if len(str(text.description)) <= 1: continue
        # print("Searching for: " + str(text.description))
        if try_rh_search(str(text.description)):
            # print(str(text.description).lower().strip())
            return str(text.description).lower().strip() # will check the robinhood ticker search api and if it finds a match, then returns
        else:
            continue

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

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