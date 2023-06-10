import pygame as pg

def printfile(surfaceLoc, textLinesLoc, textFontLoc, textColLoc, xMaxLoc, yMaxLoc):
    textRectLoc = pg.Rect(0.1 * xMaxLoc, 0.1 * yMaxLoc, 0.8 * xMaxLoc, 25)  # create Rect for the story
    for line in textLinesLoc:  # get the story text and render it
        storyTextLine = textFontLoc.render(line, True, textColLoc)
        surfaceLoc.blit(storyTextLine, textRectLoc)
        textRectLoc.move_ip(0, 25)


def gettext(fileLoc):
    with open(fileLoc + ".txt", encoding='utf-8', errors='ignore') as f:
        textLinesLoc = []
        for line in f:
            textLinesLoc.append(line.strip())
    return textLinesLoc

def gameend(surfaceLoc, textFontLoc, textColLoc, xMaxLoc, yMaxLoc):
    gameRun = True
    contRect = pg.Rect(0.5 * xMaxLoc - 200, 0.9 * yMaxLoc, 300, 25)  # draw space to continue
    surfaceLoc.blit(textFontLoc.render("Press SPACE to go back to the menu", True, textColLoc), contRect)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameRun = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                gameRun = False
            elif event.key == pg.K_ESCAPE:
                gameRun = False
    return gameRun