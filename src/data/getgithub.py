from __future__ import division
import requests, json, os
import dateutil.parser as dp

'''
this script is to get github public projects with their info.
'''
ignore = ['GoodCause', 'TTP-Techninal-Questions','Code2040', 'josuerojasrojas.github.io', 'josuerojasrojas.github.io-old', 'Bulletin-Board', 'hackathonstuff2017', 'Portfolio'] #repos to ignore
user = 'josuerojasrojas'
basicInfo = requests.get('https://api.github.com/users/'+user,auth=('josuerojasrojas',os.environ['gittoken'])).json()
repos = requests.get('https://api.github.com/users/'+user+'/repos',auth=('josuerojasrojas',os.environ['gittoken'])).json()
allLanguages = set([])


def languagePercent(langs):
    total = 0
    for language in langs.keys():
        total+= langs[language]
        allLanguages.add(language) #this should be more locally scope but this works fine for now
    for language in langs.keys():
        langs[language] = (langs[language]/total) * 100
    return langs

# i am sure there is a better way to filter the data
# ill do that later
def getInfo():
    repoNames = []
    htmlURL = []
    repoDesc = []
    createAt = []
    languages = []
    projectLink = []
    languagesList= []
    for repo in repos:
        if repo['name'] in ignore:
            continue
        languagesInfo = languagePercent(requests.get(repo['languages_url'],auth=('josuerojasrojas',os.environ['gittoken'])).json()) if repo['languages_url'] else []
        repoNames.append(repo['name'] if repo['name'] else '')
        htmlURL.append(repo['html_url'] if repo['html_url'] else '')
        repoDesc.append(repo['description'] if repo['description'] else '')
        createAt.append(repo['created_at'] if repo['created_at'] else '')
        languages.append(languagesInfo)
        languagesList.append(languagesInfo.keys())
        projectLink.append(repo['homepage'] if repo['homepage'] else '#')
    datevalue = [dp.parse(dateC).strftime('%s') for dateC in createAt] # value of time for sorting
    return repoNames, htmlURL, repoDesc, createAt, languages,languagesList, projectLink, datevalue

# this returns a json object (how i wanted)
# getInfo() should be run first to get allLanguages
def organizeData(repoNames, htmlURL, repoDesc, createAt, languages,languagesList, projectLink, datevalue, allLanguages=allLanguages):
    # make each repo json
    repoJson = []
    for i in range(len(repoNames)):
        repoJson.append({
        'repo_name': repoNames[i],
        'url': htmlURL[i],
        'description': repoDesc[i],
        'languages': languages[i],
        'languagesList': languagesList[i],
        'created': createAt[i],
        'projectLink': projectLink[i],
        'datevalue': datevalue[i]
        })
    dataJson = {
        'fullname': basicInfo['name'],
        'username': user,
        'avatar_url': basicInfo['avatar_url'],
        'languages':list(allLanguages),
        'repos': repoJson
    }
    return dataJson

def main():
    repoNames, htmlURL, repoDesc, createAt, languages, languagesList, projectLink, datevalue = getInfo()
    with open('data.json','w') as jsonfile:
        json.dump(organizeData(repoNames, htmlURL, repoDesc, createAt, languages,languagesList, projectLink, datevalue), jsonfile)
    os.chdir(os.getcwd())
    # os.system('cd '+ os.getcwd()+ '; json2yaml data.json > data.yml') #it's easier to use so i've heard, plus it looks pretty

main()
