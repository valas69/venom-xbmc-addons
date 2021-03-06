#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, VSlog
import re, base64

#copie du site http://www.kaydo.ws/
#copie du site https://www.hds.to/

SITE_IDENTIFIER = 'kaydo_ws'
SITE_NAME = 'Kaydo (hds.to)'
SITE_DESC = 'Site de streaming en HD'

URL_MAIN = 'https://www.hds.to/'

MOVIE_NEWS = (URL_MAIN + 'affiche.php', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films.php', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'populaires.php', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'films.php?s=go&sort=rating', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'top-films.php', 'showMovies')
MOVIE_HD = (URL_MAIN + 'films.php', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_RANDOM = (URL_MAIN + 'random.php', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'series-latest.php', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series.php', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')

URL_SEARCH = (URL_MAIN + 'search.php?q=', 'sHowResultSearch')
URL_SEARCH_MOVIES = (URL_MAIN + 'search.php?q=', 'sHowResultSearch')
URL_SEARCH_SERIES = (URL_MAIN + 'search.php?q=', 'sHowResultSearch')
FUNCTION_SEARCH = 'sHowResultSearch'

def Decode(chain):
    try:
        chain = 'aHR' + chain
        chain = 'M'.join(chain.split('7A4c1Y9T8c'))
        chain = 'V'.join(chain.split('8A5d1YX84A428s'))
        chain = ''.join(chain.split('$'))

        return base64.b64decode(chain)
    except:
        return chain

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP[1], 'Top Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_RANDOM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_RANDOM[1], 'Films Aleatoires', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = cUtil().urlEncode(sSearchText)
        sUrl = URL_SEARCH[0] + sSearchText
        if '' in sSearchText:
            sSearchText.replace('','+')
        sHowResultSearch(sUrl)
        oGui.setEndOfDirectory()
        return

def sHowResultSearch(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    sUrl = sSearch

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="login-box">(.+?)<footer class='
    aResult = re.search(sPattern, sHtmlContent, re.DOTALL)
    if (aResult):
        sHtmlContent = aResult.group(1)

    sPattern = '<img src="(thumb[^"]+)".+?<a href="(.+?)" class="name">(.+?)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN+aEntry[1]
            sThumb = URL_MAIN+aEntry[0]
            #sDesc = aEntry[3]
            sTitle2 = str(aEntry[2])
            sTitle2 = sTitle2.replace('<font color="orange">[SÉRIE]</font>', '')
            sTitle = sTitle2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            if 'details-serie.php' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            elif 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'films.php?s=go&sort=add&g=Action'] )
    liste.append( ['Animation', URL_MAIN + 'films.php?s=go&sort=add&g=Animation'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'films.php?s=go&sort=add&g=Arts Martiaux'] )
    liste.append( ['Aventure', URL_MAIN + 'films.php?s=go&sort=add&g=Aventure'] )
    liste.append( ['Biopic', URL_MAIN + 'films.php?s=go&sort=add&g=Biopic'] )
    liste.append( ['Comédie', URL_MAIN + 'films.php?s=go&sort=add&g=Comédie'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'films.php?s=go&sort=add&g=Comédie dramatique'] )
    liste.append( ['Documentaire', URL_MAIN + 'films.php?s=go&sort=add&g=Documentaire'] )
    liste.append( ['Drame', URL_MAIN + 'films.php?s=go&sort=add&g=Drame'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'films.php?s=go&sort=add&g=Epouvante-horreur'] )
    liste.append( ['Espionnage', URL_MAIN + 'films.php?s=go&sort=add&g=Espionnage'] )
    liste.append( ['Fantastique', URL_MAIN + 'films.php?s=go&sort=add&g=Fantastique'] )
    liste.append( ['Famille', URL_MAIN + 'films.php?s=go&sort=add&g=Famille'] )
    liste.append( ['Guerre', URL_MAIN + 'films.php?s=go&sort=add&g=Guerre'] )
    liste.append( ['Historique', URL_MAIN + 'films.php?s=go&sort=add&g=Historique'] )
    liste.append( ['Musical', URL_MAIN + 'films.php?s=go&sort=add&g=Musical'] )
    liste.append( ['Policier', URL_MAIN + 'films.php?s=go&sort=add&g=Policier'] )
    liste.append( ['Romance', URL_MAIN + 'films.php?s=go&sort=add&g=Romance'] )
    liste.append( ['Science Fiction', URL_MAIN + 'films.php?s=go&sort=add&g=Science fiction'] )
    liste.append( ['Thriller', URL_MAIN + 'films.php?s=go&sort=add&g=Thriller'] )
    liste.append( ['Western', URL_MAIN + 'films.php?s=go&sort=add&g=Western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'series.php?g=Action'] )
    liste.append( ['Animation', URL_MAIN + 'series.php?g=Animation'] )
    liste.append( ['Aventure', URL_MAIN + 'series.php?g=Aventure'] )
    liste.append( ['Comédie', URL_MAIN + 'series.php?g=Comédie'] )
    liste.append( ['Drame', URL_MAIN + 'series.php?g=Drame'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'series.php?g=Epouvante-horreur'] )
    liste.append( ['Fantastique', URL_MAIN + 'series.php?g=Fantastique'] )
    liste.append( ['Historique', URL_MAIN + 'series.php?g=Historique'] )
    liste.append( ['Judiciaire', URL_MAIN + 'series.php?g=Judiciaire'] )
    liste.append( ['Policier', URL_MAIN + 'series.php?g=Policier'] )
    liste.append( ['Romance', URL_MAIN + 'series.php?g=Romance'] )
    liste.append( ['Science Fiction', URL_MAIN + 'series.php?g=Science fiction'] )
    liste.append( ['Thriller', URL_MAIN + 'series.php?g=Thriller'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('Bande-Annonce', '')
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n', ''))
    #fh.close()

    sPattern1 = '<img src="([^"]+?)" width=.+?<h2>(.+?)</h2>.*?<h3>(.+?)<\/h3>.+?<p>([^<]+)</p><a class="btn.+?href="(.+?)"'

    if  'add&g' in sUrl:
        sPattern2 = '<img src="([^"]+)" width=.+?<a href="([^"]+)">.+?data-tooltip="Synopsis *: *([^<]+)">.+?<h2>(.+?)</h2>.+?<h3>(.+?)<\/h3>'
    else:
        sPattern2 = '<img src="([^"]+)" width=.+?<a href="([^"]+)">.+?title="(.+?)".+?data-tooltip="Synopsis *: *([^<]+)">.+?<h3>(.+?)<\/h3>'

    aResult = oParser.parse(sHtmlContent, sPattern2)

    if not (aResult[0] == True):
        aResult = oParser.parse(sHtmlContent, sPattern1)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if  'add&g' in sUrl:
                sThumb = URL_MAIN + str(aEntry[0])
                siteUrl = URL_MAIN + str(aEntry[1])
                sDesc = str(aEntry[2])
                sDisplayTitle = ('%s (%s)') % (str(aEntry[3]), str(aEntry[4]).replace(' - COMP', 'COMP'))
                sTitle = aEntry[3]
            else:
                sThumb = URL_MAIN + str(aEntry[0])
                siteUrl = URL_MAIN + str(aEntry[1])
                sDesc = str(aEntry[3])
                sDisplayTitle = ('%s (%s)') % (str(aEntry[2]), str(aEntry[4]))
                sTitle = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            if 'details-serie.php' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)
            elif '/series' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
                
        if 'random.php' in sUrl:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',sUrl)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Trouvez moi d autres films >>>[/COLOR]', oOutputParameterHandler)  

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()     
    sPattern = 'class="pagination">.*?<li class="active">.+?<li><a href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False

def showSeries():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<img src="([^"]+)" width=".+?<span class.+?>(.+?)<\/span>.+?<a href="([^"]+)">.+?<h2>(.+?)</h2>.*?<h3>(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = URL_MAIN + str(aEntry[0])
            siteUrl = URL_MAIN + str(aEntry[2])
            sDesc = str(aEntry[4])
            sTitle = ('%s (%s) (%s)') % (sMovieTitle, str(aEntry[1].replace(' COMP', 'COMP')), str(aEntry[4]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def seriesHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl + '?ep=0')
    sHtmlContent = oRequestHandler.request()


    result = re.search('col s4 hide-on-med-and-down(.+?)$', sHtmlContent, re.DOTALL)
    sHtmlContent = result.group(1)

    sPattern = '<div class="truncate.+?</i>(.+?)<script>(.+?)</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if 'ep=0&' in aEntry[1]:
                continue

            links = []
            result = re.search('href="(.+?ver=vf)"', aEntry[1])
            if result:
                links += [['VF', result.group(1)]]
            result = re.search('href="(.+?ver=vo)"', aEntry[1])
            if result:
                links += [['VOST', result.group(1)]]

            for t, link in links:
                oOutputParameterHandler = cOutputParameterHandler()
                sUrl = URL_MAIN + '/series/' + link
                #name = aEntry[0] + ' (' + t + ')'
                name = ('%s (%s)') % (aEntry[0], t)

                name = name.replace('Ep. ', 'E')

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addTV(SITE_IDENTIFIER, 'showHosters', name, 'series.png', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb  = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<video><source type="video/mp4" src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0]):
        BA = aResult[1][0]
    else:
        BA = False

    sPattern = 'de\("([^\)]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            VSlog('A decoder' + str(aEntry))
            url = Decode(str(aEntry))
            VSlog('donne ' + url)

            if url.startswith('http'):
                if 'manifest.mpd' in url:
                    continue

                if '/mp4/' in url: #lien upto,1fich,direct ou inutilisable
                    sId = re.search('\/mp4\/([^-]+)', url)
                    if sId:
                        chaine = sId.group(1)
                        vUrl = base64.b64decode(chaine + "==")

                        if 't411.li' in vUrl:
                            continue
                        elif 'uptobox' in vUrl:
                            sHosterUrl = vUrl
                        elif '1fichier' in vUrl:
                            sHosterUrl = vUrl
                        else:
                            sHosterUrl = url

                else:
                    sHosterUrl = url

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

        if (BA != False):
            sHosterUrl2 = str(BA)
            oHoster2 = cHosterGui().checkHoster(sHosterUrl2)
            if (oHoster2 != False):
                oHoster2.setDisplayName(sMovieTitle + '[COLOR coral]' + (' [Bande Annonce] ') + '[/COLOR]')
                oHoster2.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster2, sHosterUrl2, '')

    oGui.setEndOfDirectory()
