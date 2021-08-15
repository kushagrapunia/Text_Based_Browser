import os
import sys
import requests
from bs4 import BeautifulSoup
import colorama
from colorama import init, Fore


nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow
and change shape, and that could be a boon to medicine
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's
 Bad Moon Rising. The world is a very different place than
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''


# write your code here
def get_request(url: str):
    if not url.__contains__("https://"):
        url = 'https://' + url
    return requests.get(url)

def readable_text(text):
    text_list = []
    tags = ['title', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']
    s = BeautifulSoup(text, 'html.parser')
    for tag in s.find_all(tags):
        text = tag.get_text()
        if tag.name == 'a':
            text = Fore.BLUE + text
        text_list.append(text)
    return '\n'.join(text_list)


if __name__ == '__main__':
    args = sys.argv
    directory = args[1]
    stack = []

    if not os.access(directory, os.F_OK):
        os.mkdir(directory)
    if os.access(directory, os.F_OK):
        while True:
            line = input().strip()
            colorama.init(autoreset=True)
            if line == 'exit':
                break
            elif line == 'back':
                if len(stack) != 0:
                    file_name = stack.pop()
                    file_name = stack.pop()
                    file_path = os.path.join(directory, file_name)
                    with open(file_path, 'r') as f:
                        print(f.read())
                continue
            if line.count('.') > 0:
                # key = line.replace('.', '_')
                try:
                    req = get_request(line)
                except requests.exceptions.ConnectionError:
                    print('Incorrect URL')
                else:
                    x = readable_text(req.content)
                    print(x)
                    file_name = line
                    file_path = os.path.join(directory, file_name)
                    with open(file_path, 'w') as f:
                        f.write(x)


                # if key in ['nytimes_com', 'bloomberg_com']:
                #     if key == 'nytimes_com':
                #         print(nytimes_com)
                #         values = nytimes_com
                #     else:
                #         print(bloomberg_com)
                #         values = bloomberg_com
                #     file_name = key.split('_')[0]
                #     stack.append(file_name)
                #     file_path = os.path.join(directory, file_name)
                #     with open(file_path, 'w') as f:
                #         f.write(values)
                # else:
                #     print('Error: Incorrect URL')
            else:
                key = line.split()
                if len(key) == 1:
                    if key[0] in os.listdir(directory):
                        file_name = key[0]
                        stack.append(file_name)
                        file_path = os.path.join(directory, file_name)
                        with open(file_path, 'r') as f:
                            print(f.read())
                    else:
                        print('Error: Incorrect URL')
                else:
                    print('Error: Incorrect URL')
    else:
        print('Error: Incorrect URL')
