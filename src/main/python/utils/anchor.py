# utility functions to deal with an HTML anchor tag

def getText(tag: str):
    start = tag.find(">") + 1
    finish = tag.find("</a")
    if finish >= start:
        return tag[start:finish]
    return ""


def getHref(tag: str):
    start = tag.find("href") + 5
    finish = tag.find(">")
    if finish >= start:
        href = tag[start:finish]
        href = href.replace("'", "")
        href = href.replace("\"", "")
        return href
    return ""
