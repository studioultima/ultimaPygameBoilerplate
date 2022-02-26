import pygame
import json
import operator

#Functions
#-------------------------------
def getCurrentSeconds(startSceneTicks):
    seconds = (pygame.time.get_ticks()-startSceneTicks)/1000
    roundedSeconds = int(round(seconds))
    return roundedSeconds

def getSettingsJSON():
    jsonSettings = open('settings.json','r')
    jsonString = jsonSettings.read()
    jsonConverted = json.loads(jsonString)
    return jsonConverted

#get the width trought the get_size function
def getWidth(object):
    width = object.get_size()[0]
    return width

#get the width trought the get_size function
def getHeight(object):
    height = object.get_size()[1]
    return height

def addToRenderStack(element,x,y,priority):
    renderElement = {'element':element,'x':x,'y':y,'priority':priority}
    return renderElement

def resetScreens():
    mainScreen.fill(blackColor)
    renderScreen.fill(blackColor)
    overlayScreen.fill(transparentColor)

def updateFramerateMultiplier():
    framerateMultiplier = clockFramerate.tick(framerateLimit)
    return framerateMultiplier

def runRender(renderScreenStack,overlayScreenStack):
    
    #renderScrenStack
    #reordering stack example
    if renderScreenStack:
        renderScreenStack = sorted(renderScreenStack, key = operator.itemgetter('y', 'x'),reverse=True)
        renderScreenStack = sorted(renderScreenStack, key = operator.itemgetter('priority',))

        for renderElement in renderScreenStack:
            renderScreen.blit(renderElement['element'],(renderElement['x'],renderElement['y']))
    
    #reordering stack example
    if overlayScreenStack:
        overlayScreenStack = sorted(overlayScreenStack, key = operator.itemgetter('y', 'x'),reverse=True)
        overlayScreenStack = sorted(overlayScreenStack, key = operator.itemgetter('priority',))


        for renderElement in overlayScreenStack:
            overlayScreen.blit(renderElement['element'],(renderElement['x'],renderElement['y']))
        
    upscaledRenderScreen = pygame.transform.scale(renderScreen, (mainScreenWidth,mainScreenHeight))
    mainScreen.blit(upscaledRenderScreen, (0,0))
    mainScreen.blit(overlayScreen, (0,0))        
    pygame.display.update()
#-------------------------------
pygame.init() 

#customEvents
startSceneTicks = pygame.time.get_ticks()
AddBootEvent = pygame.USEREVENT + 0 #32850
bootEvent = pygame.event.Event(AddBootEvent)
pygame.event.post(bootEvent)

#getSettingsFromJSON
mainScreenWidth     = getSettingsJSON()['mainScreenWidth']
mainScreenHeight    = getSettingsJSON()['mainScreenHeight']
windowCaption       = getSettingsJSON()['windowCaption']
downscaleMultiplier = getSettingsJSON()['downscaleMultiplier']

#mainScreen
icon = pygame.image.load('images/logo.png')
pygame.display.set_icon(icon)
pygame.display.set_caption(windowCaption)
mainScreen = pygame.display.set_mode((mainScreenWidth,mainScreenHeight),pygame.RESIZABLE)

#renderScreen
renderScreenWidth  = mainScreenWidth  / downscaleMultiplier
renderScreenHeight = mainScreenHeight / downscaleMultiplier
renderScreen = pygame.Surface((renderScreenWidth,renderScreenHeight),pygame.SRCALPHA)

#overlayScreen
overlayScreen = pygame.Surface((mainScreenWidth,mainScreenHeight),pygame.SRCALPHA)

#framerate
framerateLimit = getSettingsJSON()['framerateLimit']
clockFramerate = pygame.time.Clock()
framerateMultiplier = 1
    
#colors
whiteColor = 255, 255, 255 
blackColor = 0, 0, 0
transparentColor = 0, 0, 0, 0

#fonts
pygame.font.init()
m5x7_16 = pygame.font.Font('fonts/m5x7.ttf',16)
m5x7_32 = pygame.font.Font('fonts/m5x7.ttf',32)
m5x7_64 = pygame.font.Font('fonts/m5x7.ttf',64)

#static game elements
logoImg = pygame.image.load('images/logo.png').convert()
logoText = m5x7_32.render('Pygame Boilerplate', True, whiteColor)
logoTextWebsite = m5x7_16.render('studioultima.com', True, whiteColor)
fadeInScreen = pygame.Surface((renderScreenWidth,renderScreenHeight),pygame.SRCALPHA)

#game Flags & Variables
currentScene = 'splashscreen'
finishedFadeInFlag = bool(0)
transparencyFadeInScreen = 255
transparencyTransitionSpeed = 0.1


#gameLoop
while True:
    #update Framerate Multiplier
    framerateMultiplier = updateFramerateMultiplier()

    resetScreens()

    if currentScene == 'splashscreen':

        #-------------------------------
        sceneName = 'Splash Screen'
        nextScene = 'splashscreen'

        for event in pygame.event.get():
            #debug events
            #print (event)
            #Quitting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_RETURN:
                    nextScene = 'helloworld'  
                    startSceneTicks = pygame.time.get_ticks()
            if event.type == pygame.USEREVENT + 0:
                print ('BootEvent') 

        
        renderScreenStack =  []
        overlayScreenStack = []

        sceneTimeWidget = m5x7_32.render('Scene Time: ' + str(getCurrentSeconds(startSceneTicks)), True, whiteColor)
        fpsCounter = m5x7_32.render('FPS: ' + str(round(clockFramerate.get_fps())), True, whiteColor)
        sceneNameWidget = m5x7_32.render('Scene: ' + str(sceneName), True, whiteColor)

        overlayScreenStack.append(addToRenderStack(sceneNameWidget,0,0,0))
        overlayScreenStack.append(addToRenderStack(sceneTimeWidget,0,0 + getHeight(sceneNameWidget),0))
        overlayScreenStack.append(addToRenderStack(fpsCounter,mainScreenWidth - getWidth(fpsCounter),0,0))

        if getCurrentSeconds(startSceneTicks) > 1 :
            if finishedFadeInFlag == bool(0):
                if transparencyFadeInScreen > 0:
                    failsafePrediction = transparencyFadeInScreen - (transparencyTransitionSpeed * framerateMultiplier)
                    if failsafePrediction <= 0:
                        transparencyFadeInScreen = 0
                    else:
                        transparencyFadeInScreen -= transparencyTransitionSpeed * framerateMultiplier
                #activate finishedFadeInFlag
                if transparencyFadeInScreen == 0:
                    finishedFadeInFlag = bool(1)

        
        if getCurrentSeconds(startSceneTicks) > 8 :
            if transparencyFadeInScreen < 255:
                failsafePrediction = transparencyFadeInScreen + (transparencyTransitionSpeed * framerateMultiplier)
                if failsafePrediction >= 255:
                    transparencyFadeInScreen = 255
                else:
                    transparencyFadeInScreen += transparencyTransitionSpeed * framerateMultiplier
            
            
        fadeInScreen.fill((0,0,0,transparencyFadeInScreen))

        
        if getCurrentSeconds(startSceneTicks) > 11 :
            nextScene = 'helloworld'  
            startSceneTicks = pygame.time.get_ticks()

        
        renderScreenStack.append(addToRenderStack(fadeInScreen,0,0,1))
        renderScreenStack.append(addToRenderStack(logoImg,renderScreenWidth/2 - getWidth(logoImg)/2 ,renderScreenHeight/2 - getHeight(logoImg)/2,0))
        renderScreenStack.append(addToRenderStack(logoText,renderScreenWidth/2 - getWidth(logoText)/2 ,renderScreenHeight/2 + getHeight(logoImg)/2 ,0))
        renderScreenStack.append(addToRenderStack(logoTextWebsite,renderScreenWidth/2 - getWidth(logoTextWebsite)/2 ,renderScreenHeight/2 + getHeight(logoImg)/2 + getHeight(logoText) ,0))

        #-------------------------------

    elif currentScene == 'helloworld':

        #-------------------------------
        sceneName = 'Hello World'
        nextScene = 'helloworld'

        for event in pygame.event.get():
            #debug events
            #print (event)
            #Quitting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            if event.type == pygame.USEREVENT + 0:
                print ('BootEvent') 

        
        renderScreenStack =  []
        overlayScreenStack = []

        fpsCounter = m5x7_32.render('FPS: ' + str(round(clockFramerate.get_fps())), True, whiteColor)
        sceneNameWidget = m5x7_32.render('Scene: ' + str(sceneName), True, whiteColor)

        overlayScreenStack.append(addToRenderStack(sceneNameWidget,0,0,0))
        overlayScreenStack.append(addToRenderStack(fpsCounter,mainScreenWidth - getWidth(fpsCounter),0,0))

      
        helloWorld = m5x7_64.render('Hello World', True, whiteColor)

        renderScreenStack.append(addToRenderStack(helloWorld,renderScreenWidth/2 - getWidth(helloWorld)/2 ,renderScreenHeight/2 - getHeight(helloWorld)/2,0))

    
        #-------------------------------

    currentScene = nextScene

    runRender(renderScreenStack,overlayScreenStack)

