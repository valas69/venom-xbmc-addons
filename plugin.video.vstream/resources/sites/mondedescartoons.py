#-*- coding: utf-8 -*-
#
# Valas
#
#
from resources.lib.gui.hoster import cHosterGui #systeme de recherche pour l'hote
from resources.lib.handler.hosterHandler import cHosterHandler #systeme de recherche pour l'hote
from resources.lib.gui.gui import cGui #systeme d'affichage pour xbmc
from resources.lib.gui.guiElement import cGuiElement #systeme d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entree des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortie des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.config import cConfig #config
from resources.lib.parser import cParser #recherche de code
#from resources.lib.util import cUtil #outils pouvant etre utiles
 
import xbmc
 
#Si vous créez une source et la deposez dans le dossier "sites" elle sera directement visible sous xbmc
 
SITE_IDENTIFIER = 'mondedescartoons' #identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = 'Monde des cartoons' #nom que xbmc affiche
SITE_DESC = 'Dessin animé en VO(STFR)/VF' #description courte de votre source
 
URL_MAIN = 'http://www.mondedescartoons.fr/' #url de votre source
 
#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
#LA RECHERCHE GLOBAL N'UTILE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
 
 
ANIM_ANIMS = ('http://', 'load') #animés (load source)
ANIM_NEWS = (URL_MAIN, 'showSerie') #animés (derniers ajouts = trie par date)
 
def load(): #fonction chargee automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage
    oGui.addText(SITE_IDENTIFIER, "Il se peut que certain déssin animés ne soit pas disponible en VF ou VOSTFR tout en étant repértorié.")
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oOutputParameterHandler.addParameter('lang', "vf")
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Liste des dessins animés [VF]', 'films_news.png', oOutputParameterHandler)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oOutputParameterHandler.addParameter('lang', "vo")
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Liste des dessins animés [VO(STFR?)]', 'films_news.png', oOutputParameterHandler)
    #ici la function showMovies a besoin d'une url ici le racourci MOVIE_NEWS
 
    oGui.setEndOfDirectory() #ferme l'affichage
 
#Pour les series, il y a generalement une etape en plus pour la selection des episodes ou saisons.
def showSerie():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    lang = oInputParameterHandler.getValue("lang")
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('http://www.mondedescartoons.fr/live/', '').replace("http://www.mondedescartoons.fr/contact/","").replace("http://www.mondedescartoons.fr/faq/","").replace("http://www.mondedescartoons.fr/credits/","").replace("http://www.mondedescartoons.fr/partenaires/","")
   
    sPattern = 'class="menu-item menu-item-type-custom menu-item-object-custom menu-item-.+?"><a href="http://www.mondedescartoons.fr/(.+?)-(.+?)>(.+?)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        dialog = cConfig().createDialog(SITE_NAME)
        total = len(aResult[1])
        for url,ep,aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = str(aEntry) #Titre du dessin animé ex: Adventure Time
            sTitleRef = str(url) #Reference du dessin animé ex: advf
            if "vf" not in sTitleRef and "vo" not in sTitleRef:
                sTitleRef +="vo"
            sUrl2 = URL_MAIN+str(url).replace('vf',lang)+'-'+ep
 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieRef', sTitleRef.replace("vf",lang))
            oOutputParameterHandler.addParameter('sMovie', sTitle)
            oOutputParameterHandler.addParameter('page', sHtmlContent)
            #oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addTV(SITE_IDENTIFIER, 'showSaison', sTitle, '', '', '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
 
    oGui.setEndOfDirectory()
 
def showEpisode(): #cherche les episodes de series
 
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    Saison = oInputParameterHandler.getValue("Saison")
    lang = oInputParameterHandler.getValue("lang")
    sRef = str(oInputParameterHandler.getValue('sMovieRef'))
    sHtmlContent = oInputParameterHandler.getValue("page")
    sPattern = '<br><a href="http://www.mondedescartoons.fr/'+sRef+'-s'+Saison+'-(.+?)/">(.+?)</a>'
 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) #Exemple de ce que aResult retourne: True, (s01-e01, Episode 1)
 
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for ep,aEntry in aResult[1]: #ep -> s1-e01 et aEntry Episode 1
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            URL_EPISODE = str(URL_MAIN+sRef+"-s"+Saison+"-"+str(ep)) #Exemple de ce que URL_EPISODE retourne: http://www.mondedescartoons.fr/advf-s1-e01/
 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_EPISODE)
            oOutputParameterHandler.addParameter('episode', aEntry)
            oGui.addTV(SITE_IDENTIFIER, 'findEpisodeHoster', Saison + aEntry , '', '', '', oOutputParameterHandler)
        cConfig().finishDialog(dialog)
 
 
    oGui.setEndOfDirectory()
 
def showSaison():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
   
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sRef = oInputParameterHandler.getValue('sMovieRef')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sHtmlContent = sHtmlContent.replace('http://www.mondedescartoons.fr/live/', '').replace("http://www.mondedescartoons.fr/contact/","").replace("http://www.mondedescartoons.fr/faq/","").replace("http://www.mondedescartoons.fr/credits/","").replace("http://www.mondedescartoons.fr/partenaires/","")
    sPattern = '<div class="su-spoiler-title"><span class="su-spoiler-icon"></span>Saison (.+?)</div><div class="su-spoiler-content su-clearfix" style=.+?"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for sais in aResult[1]:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('Saison', sais)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieRef', sRef)
            oOutputParameterHandler.addParameter('page', sHtmlContent)
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisode', "Saison "+sais, '', "", "", oOutputParameterHandler)
 
 
 
    oGui.setEndOfDirectory()
def findEpisodeHoster():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    url = oInputParameterHandler.getValue("siteUrl")
    episode = oInputParameterHandler.getValue("episode")
    oRequestHandler = cRequestHandler(str(url))
    sHtmlContent = oRequestHandler.request()
    sPattern = '<iframe .+?src="(.+?)".+?</iframe>'
    oParser = cParser()
    videolink = str(oParser.parse(sHtmlContent, sPattern)[1]).replace('[','').replace(']','').replace("'",'')
    if len(videolink) < 4:
        sPattern = '<script src="([^"]+)"></script><br />'
        videolink = str(oParser.parse(sHtmlContent, sPattern)[1]).replace('[','').replace(']','').replace("'",'')
    if "//" in videolink and "http" not in videolink: #(type de lien: //www.le_lien.fr -> https://www.le_lien.fr)
        videolink = videolink.replace("//", "https://")
 
    oHoster = cHosterGui().checkHoster(videolink)
    if (oHoster != False):
        oHoster.setDisplayName(episode)
        oHoster.setFileName(episode)
        cHosterGui().showHoster(oGui, oHoster, videolink, '')
     
    oGui.setEndOfDirectory()
