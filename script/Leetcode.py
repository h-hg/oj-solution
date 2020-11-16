import os
import sys
import config
import LeetcodeCrawler

class Leetcode:
    def __init__(self):
        self.scriptPath = config.scriptPath
        self.workplace = config.workplace
        self.leetcodePath = config.leetcodePath
        self.leetcodeCrawler = LeetcodeCrawler.LeetcodeCrawler()

    def createIndexMd(self, info, dirPath):
        if(not os.path.exists(dirPath)):
            os.makedirs(dirPath)
        with open(os.path.join(dirPath, "index.md"), "w", encoding="utf-8") as fw:
            fw.write("# " + info["title"] + "\n")
            with open(os.path.join(self.scriptPath, "template/leetcode.md"), "r", encoding="utf-8") as fr:
                fw.write(fr.read())

    def createDescMD(self, info, dirPath):
        # images and desc.md
        for img in info["images"]:
            # There are something wrong with docsify embed files with images of html
            # info["content"] = info["content"].replace(img["src"], img["filename"])
            with open(os.path.join(dirPath, img["filename"]), "wb") as f:
                f.write(img["data"])

        with open(os.path.join(dirPath, "desc.md"), "w", encoding="utf-8") as f:
            f.write(info["content"])

    def updateTag(self, info):
        filePath = os.path.join(self.workplace, "tag/leetcode.md")
        # read the tags
        tags = None, None
        with open(filePath, "r", encoding="utf-8") as f:
            # read the tags
            f.readline()
            f.readline()
            lines = f.readlines()
            tags = {int(line[1 : line.find("|", 1)]): line for line in lines}
        # insert current tag
        free = None
        if info["free"] == True:
            free = ":o:" # "`:heavy_check_mark:`"
        else:
            free = ":x:" # ":heavy_multiplication_x:"
        tags[int(info["id"])] = "|{}|{}|{}|{}|{}|\n".format(info["id"], info["title"], info["difficulty"], ", ".join(["`" + tag + "`" for tag in info["tags"]]), free)
        # sort the tag
        tags = [tags[key] for key in sorted(tags.keys())]
        # write tag
        with open(filePath, "w", encoding="utf-8") as f:
            header = "|ID|Problem|Difficulty|Tag|Free|\n|:-:|:-:|:-:|:-:|:-:|\n"
            f.write(header)
            f.writelines(tags)

    def updateSidebar(self, info):
        lines, beginIdx, endIdx, items = None, None, None, None
        # read
        with open(os.path.join(self.workplace, "SUMMARY.md"), "r", encoding="utf-8") as f:
            lines = f.readlines()
            beginIdx = lines.index("- Leetcode\n") + 1
            for i in range(beginIdx, len(lines)):
                if not lines[i].startswith(" " * 4):
                    endIdx = i
                    break
            items = {int(line[line.find("[") + 1 : line.find(".")]) : line for line in lines[beginIdx : endIdx]}
        # insert current item
        items[int(info["id"])] = "    - [{}. {}](leetcode/{}-{}/index.md)\n".format(info["id"], info["title"], info["id"], info["titleSlug"])
        # sort and update
        items = [items[key] for key in sorted(items.keys())]
        lines[beginIdx : endIdx] = items
        # write
        with open(os.path.join(self.workplace, "SUMMARY.md"), "w", encoding="utf-8") as f:
            f.writelines(lines)
    
    def new(self, titleSlug):
        # get information
        info = self.leetcodeCrawler.getProblemDetail(titleSlug)
        dirPath = os.path.join(self.leetcodePath, info["id"] + "-" + titleSlug)
        # create index.md
        self.createIndexMd(info, dirPath)
        # desc.md and image
        self.createDescMD(info, dirPath)
        # update tag
        self.updateTag(info)
        # update sidebar
        self.updateSidebar(info)