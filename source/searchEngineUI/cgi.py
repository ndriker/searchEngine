#!/usr/bin/python
import cgi

print("Content-type: text/html\n\n")

def test():
    form = cgi.FieldStorage()
    query = form.getvalue("query")
    print(query)

if __name__ == "__main__":
    print("main")
    test()


