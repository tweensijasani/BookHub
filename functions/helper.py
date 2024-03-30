
def get_json_response(description, results):
    res_headers = [x[0] for x in description]
    json_response = []
    json_body = {}
    json_body["Message"] = "Success"
    for result in results:
        json_response.append(dict(zip(res_headers,result)))
    json_body["Results"] = json_response
    return json_body


def get_book_authors(results):
    # Parse results and form dict for multiple authors
    book_authors = {}
    for result in results:
        if result[0] in book_authors:
            book_authors[result[0]].append(result[-1])
        else:
            book_authors[result[0]] = []
            book_authors[result[0]].append(result[-1])
    # print(book_authors)
    return book_authors


def get_book_with_authors(author_dict, description, results):
    res_headers = [x[0] for x in description]
    res_headers.append("Author")
    json_response = []
    json_body = {}
    json_body["Message"] = "Success"
    for result in results:
        reslist = list(result)
        reslist.append(author_dict[result[0]])
        result = tuple(reslist)
        json_response.append(dict(zip(res_headers,result)))
    # print(len(json_response))
    json_body["Results"] = json_response
    return json_body