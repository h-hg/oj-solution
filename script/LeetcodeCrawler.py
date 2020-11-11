import requests
import json
from bs4 import BeautifulSoup

class LeetcodeCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.userAgent = "Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"

    """
    @desc Return the problem list
    """
    def getProblemList(self):
        url = "https://leetcode.com/api/problems/all/"
        headers = {
            "User-Agent": self.userAgent,
            "Connection": "keep-alive",
            "Content-Type": "application/json"
        }
        resp = self.session.get(url=url, headers=headers)
        dataJson = resp.json()
        problemList = [None] * (dataJson["stat_status_pairs"])

        for x in dataJson["stat_status_pairs"]:
            problemId = int(x["stat"]["frontend_question_id"]) - 1 # begin at 0
            problemList[problemId] = {
                "slugTitle": x["stat"]["question__title_slug"],
                "free": not x["paid_only"]
            }
        return problemList

    def getProblemDetail(self, titleSlug):
        headers = {
            "User-Agent": self.userAgent,
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com/problems/" + titleSlug
        }
        url = "https://leetcode.com/graphql"
        params = {
        "operationName": "questionData",
            "variables": {
                "titleSlug": titleSlug
            },
            "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      paidOnly\n      hasVideoSolution\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    enableDebugger\n    envInfo\n    libraryUrl\n    adminUrl\n    __typename\n  }\n}\n"
        }        
        resp = self.session.post(url=url, data=json.dumps(params).encode("utf8"), headers=headers)
        dataJson = resp.json()
        
        return {
            "id": dataJson["data"]["question"]["questionFrontendId"],
            "title": dataJson["data"]["question"]["title"],
            "titleSlug": titleSlug,
            "difficulty": dataJson["data"]["question"]["difficulty"],
            "tags": [topicTag["name"] for topicTag in dataJson["data"]["question"]["topicTags"]],
            "free": not dataJson["data"]["question"]["isPaidOnly"],
            "content": dataJson["data"]["question"]["content"],
            "hints": dataJson["data"]["question"]["hints"],
            "images": self.getImgs(dataJson["data"]["question"]["content"])
        }
    
    def getImgs(self, htmlCode):
        soup = BeautifulSoup(htmlCode, 'html.parser')
        imgs = []
        for img in soup.find_all("img"):
            url = img.get("src")
            imgs.append({
                "src": url,
                "filename": url[url.rfind("/") + 1 : len(url)],
                "data": requests.get(url).content
            })
        return imgs