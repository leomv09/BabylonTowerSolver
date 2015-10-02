

def parse_file(doc_name):
    with open(doc_name, "r") as f:
        array = []
        content = f.read().splitlines()
        for element in content:
            array.append(element.split())
        return array
