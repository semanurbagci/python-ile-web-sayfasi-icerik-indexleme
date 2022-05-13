from flask import Flask,render_template,request
import requests
import operator
from bs4 import BeautifulSoup

def metniAl(url):
    tumkelimeler = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    for kelimegruplari in soup.find_all("p"):
        icerik = kelimegruplari.text
        kelimeler = icerik.lower().split()
    
        for kelime in kelimeler:
            tumkelimeler.append(kelime)
    
    return tumkelimeler

def sembolleritemizle(tumkelimeler):
    sembolsuzkelimeler = []
    semboller = "•!'^+%&/()=?_-*|\}][{½$#£\"><@.,;:’"+chr(775)

    for kelime in tumkelimeler:
        for sembol in semboller:
            if sembol in kelime:
                kelime = kelime.replace(sembol,"")

        if(len(kelime)>0):
            sembolsuzkelimeler.append(kelime)

    return sembolsuzkelimeler

def frekanssozluguolustur(url):
        tumkelimeler = metniAl(url)
        sembolsuzkelimeler = sembolleritemizle(tumkelimeler)

        kelimefrekanslari = {}

        for kelime in sembolsuzkelimeler:
            if kelime in kelimefrekanslari:
                kelimefrekanslari[kelime] +=1
            else:
                kelimefrekanslari[kelime] = 1

        return kelimefrekanslari

def anahtarlariBul(url):
    tumkelimeler = metniAl(url)
    sembolsuzkelimeler = sembolleritemizle(tumkelimeler)
    kelimefrekanslari = frekanssozluguolustur(url)

    atilacaklar=["and", "but", "or", "yet", "so", "for", "nor", "after", "that", "as", "long", "soon", "before", 
    "by the time", "during", "henceforth", "immediately", "meanwhile", "then", "now", "once", "since", "till", "the", "moment", 
    "when", "whenever", "while", "until", "as", "as a result of", "because", "because of", "concequently", "due to the fact that", 
    "eventually", "finally", "for", "for that reason", "in that case", "in the event", "now that", "now", "on account of", "owing to", 
    "owing", "seeing that", "since", "so", "that's", "why" "therefor", "thus", "as if", "as long as", "much", "many", "though", "but", 
    "even if", "if", "if only", "indeed", "in case", "in fact that", "in the case of", "in the event of", "just as", "just in case",
    "on condition that", "only if", "providing", "rather", "than", "so as to", "so long as", "supposing", "unless", "whereas", "without", 
    "as far as", "where", "wherever", "although", "conversely", "despite", "even so", "even though", "however", "in contrast to", 
    "in spite of", "nevertheless", "nonetheless", "no matter", "otherwise", "though", "unless", "unlike", "whether or not",
    "additionally", "along", "also", "well", "besides", "further", "in addition", "moreover", "example", "instance", "per", "perhaps"
    "apart", "aside", "except", "either", "neither", "whether","be", "being", "been", "am", "is","are", "was", "mr", "mrs", "out",
    "were", "do", "does", "did", "have", "haven't", "has", "had", "could", "would", "should", "may", "might", "must", "will", "really",
    "can", "can't", "shall", "hasn't", "hadn't", "couldn't", "wouldn't", "shouldn't", "won't", "one", "i'm", "other", "possible",
    "thing", "up", "down", "seem", "seen", "cannot", "between", "entirely", "every", "few", "first", "last", "half", "how", "liked", 
    "mean", "at", "in", "on", "to", "the", "until", "under", "by", "with", "of", "about", "across", "after", "against", "along", "among",
    "before", "behind", "below", "beside", "beyond", "down", "during", "into", "like", "near", "outside", "there", "over", "round", "through",
    "till", "towards", "without", "he", "she", "is", "it", "its", "us", "am", "is", "are", "a", "an", "i", "you", "we", "they", "like", "maybe",
    "no", "none", "nobody", "never", "ever", "probably", "yourself", "within", "always", "anywhere", "anyone", "someone", "also", "more", "only",
    "isn't", "aren't", "didn't", "don't", "cause", "from", "this", "which", "his", "her", "most", "their", "such", "all", "what", "not", "some",
    "often", "even", "use", "used", "ago", "these", "around", "became", "who", "whose", "became",]

    for kelime in list(kelimefrekanslari):
        if kelime in atilacaklar:
            del kelimefrekanslari[kelime]
        
    marklist = sorted(kelimefrekanslari.items(), key=lambda x:x[1])
    sortdict = dict(marklist)

    anahtarlar={}

    for y in sembolsuzkelimeler:
        if y in anahtarlar and list(reversed(list(sortdict)))[0:10]:
            anahtarlar[y] +=1
        elif y in list(reversed(list(sortdict)))[0:10]:
            anahtarlar[y] = 1
    
    return anahtarlar 

def benzerlikskoruhesapla(url1,url2):
    anahtarlar = anahtarlariBul(url1)
    tumkelimeler2 = metniAl(url2)
    sembolsuzkelimeler2 = sembolleritemizle(tumkelimeler2)
    kelimeSayac = 0

    for kelime in sembolsuzkelimeler2:
        if kelime in sembolsuzkelimeler2:
            kelimeSayac+=1

    anahtarlarfrekanslarıToplamı = 0

    for anahtar, deger in anahtarlar.items():
        anahtarlarfrekanslarıToplamı+=deger

    ortFrekans = anahtarlarfrekanslarıToplamı/10
    ikidegecenAnahtarlar = {}

    for anahtar in anahtarlar:
        for kelime in sembolsuzkelimeler2:
            if anahtar == kelime:
                if anahtar in ikidegecenAnahtarlar:
                    ikidegecenAnahtarlar[anahtar] +=1
                else:
                    ikidegecenAnahtarlar[anahtar] = 1

    formulPay = 0

    for anahtar in anahtarlar:
        for gecen in ikidegecenAnahtarlar:
            if anahtar == gecen:
                formulPay = formulPay+(anahtarlar[anahtar]*ikidegecenAnahtarlar[gecen])

    if (kelimeSayac == 0):
        formul = 0.0
    else:
        formulPayda = ortFrekans*kelimeSayac
        formul = (formulPay/formulPayda)*100

    return formul, ikidegecenAnahtarlar

def altURLcek(url,sinir):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    urls1 = []

    for a in soup.find_all('a', href=True):
        urls1.append(a['href'])

    istenilenurls1 = []
    kontrol = "http"
    sayac1 = 0
    skorlanacakurls = []
    toplamsayac = 0
    urls2 = []
    seviye2 = "2. SEVIYE"
    seviye3 = "3. SEVIYE"
    urlSeviye = []

    for kelime in urls1:
        if kontrol in kelime: 
            sayac1+=1
            skorlanacakurls.append(kelime)
            urlSeviye.append(seviye2)
            print("******************",kelime)

            r = requests.get(kelime)
            soup = BeautifulSoup(r.content, "html.parser")

            for a in soup.find_all('a', href=True):
                urls2.append(a['href'])

            sayac2 = 0

            for kelime in urls2:
                if kontrol in kelime:
                    sayac2 +=1 
                    toplamsayac +=1
                    skorlanacakurls.append(kelime)
                    urlSeviye.append(seviye3)
                    
                if (sayac2 == sinir):
                    break
        
            if(toplamsayac == (sinir*sinir)):
                break

        if (sayac1 == sinir):
            break

    return skorlanacakurls, urlSeviye

def madde1_frekanshesaplama(url):
    kelimefrekanslari = frekanssozluguolustur(url)

    for anahtar, deger in kelimefrekanslari.items(): 
        return render_template("frekans.html",anahtar = anahtar, deger = deger, kelimefrekanslari = kelimefrekanslari.items()) 

def madde2_anahtarkelimebul(url):
    anahtarlar = anahtarlariBul(url)

    for anahtar, deger in anahtarlar.items():
        return render_template("anahtarkelime.html",anahtar = anahtar, deger = deger, anahtarlar = anahtarlar.items()) 

def madde3_benzerlikskoru(url1,url2):  
    anahtarlar = anahtarlariBul(url1)
    sonuc, ikidegecenAnahtarlar = benzerlikskoruhesapla(url1,url2)
    
    for anahtar, deger in anahtarlar.items():
        return render_template("benzerlik.html",anahtar = anahtar, deger = deger, anahtarlar = anahtarlar.items(), sonuc = sonuc, ikidegecenAnahtarlar = ikidegecenAnahtarlar) 

def madde4_indexleSirala(url):
    sinir = 5
    altURLler, urlSeviye = altURLcek(url,sinir)
    URLskorsozlugu = {}
    atama = 100.0
    gecenler = {}

    urlAdı = []
    urlSkoru = []
    urlGecenAnahtarlar = []

    for u in altURLler:
        atama, gecenler = benzerlikskoruhesapla(url,u)
        urlAdı.append(u)
        urlSkoru.append(atama)
        urlGecenAnahtarlar.append(gecenler)

    veri = list(zip(urlSeviye,urlAdı,urlSkoru,urlGecenAnahtarlar))

    for i in veri:
        return render_template("indexle_sirala.html", i= i, veri = veri)

def madde5_semantikanaliz(url):
    sinir = 5
    altURLler, urlSeviye = altURLcek(url,sinir)
    URLskorsozlugu = {}
    atama = 100.0
    gecenler = {}

    urlAdı = []
    urlSkoru = []
    urlGecenAnahtarlar = []

    for u in altURLler:
        atama, gecenler = benzerlikskoruhesapla(url,u)
        urlAdı.append(u)
        urlSkoru.append(atama)
        urlGecenAnahtarlar.append(gecenler)

    veri = list(zip(urlSeviye,urlAdı,urlSkoru,urlGecenAnahtarlar))

    for i in veri:
        return render_template("indexle_sirala.html", i= i, veri = veri)


app = Flask(__name__)

@app.route("/")
def giris():
    return render_template("giris.html")

@app.route("/1")
def frekans():
    return render_template("frekans.html")

@app.route("/2")
def anahtarkelime():
    return render_template("anahtarkelime.html")

@app.route("/3")
def benzerlik():
    return render_template("benzerlik.html")

@app.route("/4")
def indexSıra():
    return render_template("indexle_sirala.html")

@app.route("/5")
def semantik():
    return render_template("semantik.html")

@app.route("/<string:id>", methods = ["GET", "POST"])
def anafonksiyon(id):
    if request.method == "POST":
        if id == "1":
            url = request.form.get("text")
            return madde1_frekanshesaplama(url)     
        else:
            pass

        if id == "2":
            url = request.form.get("text")
            return madde2_anahtarkelimebul(url) 
        else:
            pass

        if id == "3":
            url1 = request.form.get("text1")
            url2 = request.form.get("text2")
            return madde3_benzerlikskoru(url1,url2)
        else:
            pass
   
        if id == "4":
            url = request.form.get("text")
            return madde4_indexleSirala(url)
        else:
            pass
        
        if id =="5":
            url = request.form.get("text")
            return madde5_semantikanaliz(url)
    else:
        pass



if __name__ == "__main__":
    app.run(debug = True)




    