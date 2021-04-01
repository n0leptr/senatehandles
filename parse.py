# Parse page and create list of twitter handles for processing later
import requests
import lxml.html as lh
import pandas as pd


def main():
    thandles = 'https://www.socialseer.com/resources/us-senator-twitter-accounts/'
    page_handles = requests.get(thandles)

    doc_a = lh.fromstring(page_handles.content)
    # site stores info in a table
    # Senator Name - Twitter Handle
    th_elements = doc_a.xpath('//tr')

    # store the column names
    col = []
    i = 0
    # Store Column Headers and Assign an Empty List for each col
    for t in th_elements[0]:
        i += 1
        name = t.text_content()
        col.append((name, []))

    # Append data to col lists
    for j in range(1, len(th_elements)):
        T = th_elements[j]
        # There are only 5 Cols of Data, we don't want anything else.
        if len(T) != 5:
            break
        # Col Index
        i = 0
        for t in T.iterchildren():
            data = t.text_content()
            if i > 0:
                try:
                    data = int(data)
                except:
                    pass
            col[i][1].append(data)
            i += 1

    # Creating a Pandas DataFrame to use later.
    dict_handles = {title: column for (title, column) in col}
    df_handles = pd.DataFrame(dict_handles)

    # Debugging Prints to see if I got data correctly
    print('Total Senators Listed: ' + str(len(df_handles.index)))
    for index, row in df_handles.iterrows():
        print('Senator:' + parse_name(row['Senator']) +
              '\nTwitter Handle: @' + row['Official Twitter'] + '\n')

    # I Just want the twitter handles, eventually we'll build sentiment analysis for each one.
    handles = []
    for x in df_handles['Official Twitter']:
        handles.append(x)

# Stuff to convert 'Lname, Fname' in df to 'Fname Lname' format
# This is so I can get party Affiliation from Wikipedia.


def parse_name(n):
    l = n.split(',')
    l.reverse()
    return list_to_string(l)


def list_to_string(l):
    s = ''
    for n in l:
        s += n + ' '
    return s


if __name__ == '__main__':
    main()
