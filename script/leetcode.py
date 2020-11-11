import os
import sys
import LeetcodeCrawler

class Leetcode:
    def __init__(self):
        self.scriptPath = sys.path[0]
        self.workplace = os.path.join(self.scriptPath, "..")
        self.leetcodePath = os.path.join(self.workplace, "leetcode")
        self.leetcodeCrawler = LeetcodeCrawler.LeetcodeCrawler()
    
    def new(self, titleSlug):
        # get information
        info = self.leetcodeCrawler.getProblemDetail(titleSlug)
        dirPath = os.path.join(self.leetcodePath, info["id"] + "-" + titleSlug)
        # create index.md
        if(not os.path.exists(dirPath)):
            os.makedirs(dirPath)
        with open(os.path.join(dirPath, "index.md"), "w", encoding="utf-8") as fw:
            fw.write("# " + info["title"] + "\n")
            with open(os.path.join(self.scriptPath, "template/leetcode.md"), "r", encoding="utf-8") as fr:
                fw.write(fr.read())
        # images and desc.md
        for img in info["images"]:
            info["content"] = info["content"].replace(img["src"], img["filename"])
            with open(os.path.join(dirPath, img["filename"]), "wb") as f:
                f.write(img["data"])
        
        with open(os.path.join(dirPath, "desc.md"), "w", encoding="utf-8") as f:
            f.write(info["content"])
            
        # write tag
        with open(os.path.join(self.workplace, "tag/leetcode.md"), "a", encoding="utf-8") as f:
            free = None
            if info["free"] == True:
                free = ":o:" # "`:heavy_check_mark:`"
            else:
                free = ":x:" # ":heavy_multiplication_x:"
            f.write("|%s|%s|%s|%s|%s|\n" %(info["id"], info["title"], info["difficulty"], ", ".join(["`" + tag + "`" for tag in info["tags"]]), free))