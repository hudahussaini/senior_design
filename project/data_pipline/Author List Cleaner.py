list_path = "/Users/abolt/Documents/GitHub/senior_design/Author List"


def clean_author_list(path):
    authors = open(path).readlines()
    for author in authors:
        author_index = authors.index(author)
        temp_author = author
        if temp_author.count("\n") == 1:
            temp_author = temp_author.replace("\n", "")
        if temp_author.count(" '") == 1 & temp_author.count("' ") == 1:
            start = temp_author.index(" '")
            end = temp_author.index("' ") + 1
            temp_author = temp_author[:start] + temp_author[end:]
        if temp_author.count(" ") == 2:
            split_name = temp_author.split(" ")
            split_name[1] = split_name[1][0]
            temp_author = " ".join(split_name)
        authors[author_index] = temp_author
    return authors

print(clean_author_list(list_path))