import requests
import sys
import re
import pandas as pd

headers = {

    "Authorization": "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"
}

query1 = "create a page only with table of contents,overview,scope, problem statement for "
query2 = "Create a page only with table of contents,Prerequisites, Implementation, Conclusion for "
tableofcontents = "Table of Contents"+'\n'
scope = "Scope"+'\n'
problemstatement = "Problem Statement\n"
overview = "Overview\n"
prerequisites = "Prerequisites\n"
implementation = "Implementation\n"
conclusion = "Conclusion\n"

api_key_chatgpt = "<Chat_GPT-Key>"

api_key = "Confluence_Key"

model = "gpt-3.5-turbo"

dataframe1 = pd.read_excel('story.xlsx')
topic_list = dataframe1['Topics'].tolist()
print(topic_list)


def chat_with_chatgpt(query):

    res = requests.post(f"https://api.openai.com/v1/chat/completions",

                        headers={

                            "Content-Type": "application/json",

                            "Authorization": f"Bearer {api_key_chatgpt}"

                        },

                        json={

                            "model": model,
                            "messages": [
                                {
                                    "role": "user",
                                    "content": f'{query}'
                                }

                            ],
                            "max_tokens": 4000,

                        }).json()

    return res['choices'][0]['message']['content']


def confluence_page(topic):

    res = requests.post(f"https://ukgjira.atlassian.net/wiki/rest/api/content/",

                        headers={

                            "Content-Type": "application/json",

                            "Authorization": f"Basic {api_key}"

                        },

                        json={

                            "title": f'{topic}',
                            "type": "page",

                            "space": {

                                "key": "~71202053e2e572103e4fa9a2365f9088ba6196"
                            },
                            "body": {
                                "storage": {
                                    "value":
                                        '<p><h1><b>' +
                                        tableofcontents+'</b></h1>' +
                                        '<ul><li>'+overview+'</li>' +
                                        '<li>'+scope+'</li>' +
                                        '<li>'+problemstatement+'</li>' +
                                        '<li>'+prerequisites+'</li>' +
                                        '<li>'+implementation+'</li>' +
                                        '<li>'+conclusion+'</li></ul>' +
                                    '<h2><b>'+overview+'</b></h2>'+'<p style="margin-left: 30.0px;">'+over_desc+'</p>'+'<h2><b>'+scope+'</b></h2>'+'<p style="margin-left: 30.0px;">'+scope_desc+'</p>'+'<h2><b>'+problemstatement+'</b></h2>'+'<p style="margin-left: 30.0px;">'+problemstatement_desc+'</p>'+'<h2><b>' +
                                        prerequisites+'</b></h2>'+'<p style="margin-left: 30.0px;">'+prerequisites_desc+'</p>'+'<h2><b>'+implementation+'</b></h2>'+'<p style="margin-left: 30.0px;">' +
                                    implementation_desc+'</p>'+'<h2><b>'+conclusion+'</b></h2>' +
                                        '<p style="margin-left: 30.0px;">'+conclusion_desc+'</p>'+'</p>',
                                    "representation": "storage"
                                }
                            }
                        }).json()

    return res


for topic in topic_list:
    print(topic_list)
    prompt_query1 = "".join([query1, topic])
    response_query1 = chat_with_chatgpt(prompt_query1)
    with open("story.txt", "w") as f:
        f.write(f"{response_query1}\n")
    file = open("story.txt", "r+")
    summary = file.read()
    summary = re.sub("[^A-Z\n\t' ']", "", summary, 0, re.IGNORECASE)
    print("Normal String", summary)
    over_desc = summary.split("Overview")[2].split("Scope")[0]
    print("over_desc", over_desc)
    scope_desc = summary.split("Scope")[2].split("Problem Statement")[0]
    print("scope_desc", scope_desc)
    problemstatement_desc = summary.split("Problem Statement")[2]
    print("problemstatement_desc", problemstatement_desc)

    prompt_query2 = "".join([query2, topic])
    response_query2 = chat_with_chatgpt(prompt_query2)
    with open("myfile.txt", "w") as f:
        f.write(f"{response_query2}\n")
    file2 = open("myfile.txt", "r+")
    summary1 = file2.read()
    print("sumary1", summary1)
    summary1 = re.sub("[^A-Z\n\t' ']", "", summary1, 0, re.IGNORECASE)
    print("Normal String summary1", summary1)
    prerequisites_desc = summary1.split("Prerequisites")[
        2].split("Implementation")[0]
    print("prerequisites_desc", prerequisites_desc)
    implementation_desc = summary1.split("Implementation")[
        2].split("Conclusion")[0]
    implementation_desc = implementation_desc.replace(
        '\n', "<p style='margin-left: 30.0px;'></p>")
    print("implementation_desc_original", implementation_desc)
    conclusion_desc = summary1.split("Conclusion")[2]
    print("conclusion_desc", conclusion_desc)
    response1 = confluence_page(topic)
    print(response1)
