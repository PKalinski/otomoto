import os
import glob
import sqlite3
import uuid
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
import json



def guessModelAndSegment (make, title_short, title_2nd_word, title_3rd_word):

    if title_2nd_word == 'Qashqai': return (title_2nd_word, 'SUV C')
    if title_2nd_word == 'Tipo': return (title_2nd_word, 'A')
    if title_2nd_word == 'Sandero': return (title_2nd_word, 'C')
    if title_2nd_word == 'I30': return (title_2nd_word, 'C')
    if title_2nd_word == 'i40': return (title_2nd_word, 'D')
    if title_2nd_word == 'Clio': return (title_2nd_word, 'B')
    if title_2nd_word == 'Megane': return (title_2nd_word, 'C')
    if title_2nd_word == 'Captur': return (title_2nd_word, 'SUV B')
    if title_2nd_word == 'T-Cross': return (title_2nd_word, 'SUV B')
    if title_2nd_word == 'Yaris': return (title_2nd_word, 'B')

    if title_2nd_word == 'EcoSport': return (title_2nd_word, 'SUV C')
    if title_2nd_word == 'Octavia': return (title_2nd_word, 'C')
    if title_2nd_word == 'Corolla': return (title_2nd_word, 'C')
    if title_2nd_word == 'Golf': return (title_2nd_word, 'C')
    if title_2nd_word == 'A3': return (title_2nd_word, 'C')
    if title_2nd_word == 'Duster': return (title_2nd_word, 'SUV C')
    if title_2nd_word == 'Tucson': return (title_2nd_word, 'SUV C')
    if title_2nd_word == 'Fabia': return (title_2nd_word, 'B')
    if title_2nd_word == 'S60': return (title_2nd_word, 'D')
    if title_2nd_word == 'A4': return (title_2nd_word, 'D')
    if title_2nd_word == 'A5': return (title_2nd_word, 'D')
    if title_2nd_word == 'A6': return (title_2nd_word, 'D')
    if title_2nd_word == 'Q3': return (title_2nd_word, 'SUV C')
    if title_2nd_word == 'Q5': return (title_2nd_word, 'SUV D')
    if title_2nd_word == 'Pacifica': return (title_2nd_word, 'MPV')
    if title_2nd_word == 'Sienna': return (title_2nd_word, 'MPV')
    if title_2nd_word == 'Odyssey': return (title_2nd_word, 'MPV')
    if title_2nd_word == 'Kuga': return (title_2nd_word, 'SUV C')
    if title_2nd_word == 'i20': return (title_2nd_word, 'B')
    if title_2nd_word == 'Ceed': return (title_2nd_word, 'C')
    if title_2nd_word == 'CX-3': return (title_2nd_word, 'SUV C')
    if title_2nd_word == 'Mokka': return (title_2nd_word, 'SUV B')
    if title_2nd_word == '301': return (title_2nd_word, 'C')
    if title_2nd_word == 'Arkana': return (title_2nd_word, 'SUV C')
    if title_2nd_word == 'Aygo': return (title_2nd_word, 'A')
    if title_2nd_word == 'C4': return (title_2nd_word, 'C')
    if title_2nd_word == 'Fiesta': return (title_2nd_word, 'B')
    if title_2nd_word == 'Focus': return (title_2nd_word, 'C')
    if title_2nd_word == 'Astra': return (title_2nd_word, 'C')
    if title_2nd_word == 'Mustang': return (title_2nd_word, 'SPRT')
    if title_2nd_word == 'Civic': return (title_2nd_word, 'B')
    if title_2nd_word == 'QX50': return (title_2nd_word, 'SUV C')
    if title_2nd_word == 'E-Pace': return (title_2nd_word, 'B')
    if title_2nd_word == 'Escape': return (title_2nd_word, 'SUV C')
    if title_2nd_word == 'IS': return (title_2nd_word, 'D')
    if title_2nd_word == 'ES': return (title_2nd_word, 'D')
    if title_2nd_word == 'GX': return (title_2nd_word, 'MPV')
    if title_2nd_word == 'GL': return (title_2nd_word, 'MPV')
    if title_2nd_word == 'Passat': return (title_2nd_word, 'D')
    if title_2nd_word == 'Mondeo': return (title_2nd_word, 'D')
    if title_2nd_word == 'Avensis': return (title_2nd_word, 'D')
    if title_2nd_word == 'Superb': return (title_2nd_word, 'D')
    if title_2nd_word == 'Insignia': return (title_2nd_word, 'D')
    if title_2nd_word == 'Accord': return (title_2nd_word, 'D')
    if title_2nd_word == 'Camry': return (title_2nd_word, 'D')
    if title_2nd_word == 'Kodiaq': return (title_2nd_word, 'SUV D')
    if title_2nd_word == 'Santa Fe': return (title_2nd_word, 'SUV D')
    if title_2nd_word == 'Explorer': return (title_2nd_word, 'SUV D')
    if title_2nd_word == 'S90': return (title_2nd_word, 'D')
    if title_2nd_word == 'V60': return (title_2nd_word, 'D')
    if title_2nd_word == 'V90': return (title_2nd_word, 'D')
    if title_2nd_word == 'XC': return (title_2nd_word, 'SUV D')
    if title_2nd_word == 'S90': return (title_2nd_word, 'D')


    if make == 'mercedes-benz' and title_3rd_word == 'A': return (title_3rd_word, 'A')
    if make == 'mercedes-benz' and title_3rd_word == 'B': return (title_3rd_word, 'B')
    if make == 'mercedes-benz' and title_3rd_word == 'C': return (title_3rd_word, 'C')
    if make == 'mercedes-benz' and title_3rd_word == 'E': return (title_3rd_word, 'D')
    if make == 'bmw' and title_3rd_word == '1': return (title_3rd_word, 'A')
    if make == 'bmw' and title_3rd_word == '2': return (title_3rd_word, 'B')
    if make == 'bmw' and title_3rd_word == '3': return (title_3rd_word, 'C')
    if make == 'bmw' and title_3rd_word == '5': return (title_3rd_word, 'D')
    if make == 'bmw' and title_3rd_word == '7': return (title_3rd_word, 'E')
    if make == 'mazda' and title_2nd_word == '6': return (title_2nd_word, 'D')
    if make == 'mazda' and title_2nd_word == 'CX-5': return (title_2nd_word, 'SUV D')
    if make == 'mazda' and title_2nd_word == 'E': return (title_2nd_word, 'D')
    if make == 'alfa-romeo' and title_3rd_word == 'Stelvio': return (title_3rd_word, 'D')

    if title_short == 'Dodge Grand Caravan': return (title_short, 'MPV')

    v_model = title_2nd_word
    v_segment = '-'
    return (title_2nd_word, v_segment)



def scoreCarSr (car_make, car_model, segment, fuel_type, price, user_cnt, user_type):
    score = 0
    if segment == 'D':
        score += 50
    elif segment in ['SUV D', 'MPV']:
        score += 40
    elif segment == '-':
        score += 0
    else:
        score -= 50

    if float (price) > 55000 and float(price) < 75:
        score += 10
    elif float (price) > 90000:
        score -= 10
    elif float (price) > 110000:
        score -= 30

    if user_cnt == 1 or user_type == 'IND':
        score += 10
    elif user_type == 'SALON':
        score -= 10
    elif user_type == 'KOMIS/SALON':
        score -= 15
    elif user_type == 'KOMIS':
        score -= 20

    if fuel_type == 'Benzyna':
        score += 10
    else:
        score -= 10

    if car_make in ['alfa-romeo']:
        score -= 20


    return score


def scoreCarAd (score_sr, car_make, car_model, segment, user_type, user_cnt, price, country_origin, body_type):
    score = score_sr

    if country_origin == 'PL':
        score += 20
    else:
        score -= 10

    if body_type == 'combi':
        score += 20

    if user_cnt == 1:
        score += 20

    if price > 150000:
        score -= 50
    if price > 120000:
        score -= 40
    if price > 90000:
        score -= 30



    return score



# skanowanie wszystkich folderow i sprawdzanie spojnosci FILES
def refresh_table_files():

    con = sqlite3.connect('otomoto.db')
    cur = con.cursor()

    files = glob.glob ('data/*/car_details/*')
    files = [x.replace('\\', '/') for x in files]
    files = [ (os.path.basename(x).split('.')[0] , os.path.dirname(x), x.split('/')[1] , datetime.fromtimestamp(os.path.getmtime(x)).strftime("%Y-%m-%d %H:%M:%S") ) for x in files]

    for f in files:
        sql_text_file_select = "select count (*) from FILES where FILE_NAME = ? and FILE_RUN = ? "
        sql_out = cur.execute(sql_text_file_select, (f[0], f[2])).fetchone()
        # pliku nie ma w bazie FILES
        if sql_out[0] == 0:
            sql_text_file_ins = " insert into FILES (file_uid, file_folder, file_run, file_name, file_date, file_type, file_status) values (?,?,?,?,?,?,?)"
            v_file_uid = str (uuid.uuid4())
            cur.execute(sql_text_file_ins, (v_file_uid, f[1], f[2], f[0], f[3], 'ad', 'ACTIVE'))

    con.commit()
    con.close()


# uzupelnie AD_FILE_UID w tabeli ADS_LAST (na podstawie tabeli FILES)
def refresh_table_ads_last():

    con = sqlite3.connect('otomoto.db')
    cur = con.cursor()

    sql_text_file_select = """
                            select f.FILE_UID, a.AD_ID
                            from (
                                select f1.FILE_UID, f1.FILE_NAME
                                from
                                    (
                                    select FILE_UID, FILE_NAME, FILE_RUN
                                    from FILES
                                    ) f1
                                    inner join
                                    ( 
                                    select FILE_NAME, max (FILE_RUN) as MAX_FILE_RUN
                                    from FILES
                                    group by FILE_NAME
                                    ) f2
                                    on f1.FILE_RUN = f2.MAX_FILE_RUN                                
                                ) f 
                                inner join
                                ADS_LAST a
                                    on f.FILE_NAME = a.AD_ID
                            where a.AD_FILE_UID is null
                            """
    #where FILE_STATUS = 'ACTIVE'



    for r in cur.execute(sql_text_file_select).fetchall():
        sql_text_file_upd = "update ADS_LAST set AD_FILE_UID = ? where AD_ID = ?"
        cur.execute(sql_text_file_upd, (r[0],r[1]))

    con.commit()
    con.close()


# uzupelnie AD_FILE_ID dla tabeli USER (na podstawie tabeli ADS_LAST)
def refresh_table_user ():
    con = sqlite3.connect('otomoto.db')
    cur = con.cursor()

    sql_text_file_select = """
                            select u.USER_ID, a.AD_FILE_UID
                            from
                                USERS u
                                inner join
                                (
                                select USER_ID, max (AD_FILE_UID) as AD_FILE_UID
                                from ADS_LAST
                                where AD_FILE_UID is not null
                                ) a
                                    on u.USER_ID = a.USER_ID 
                            where u.AD_FILE_UID is null and a.AD_FILE_UID is not null
                            """
    for r in cur.execute(sql_text_file_select).fetchall():
        sql_text_file_upd = "update USERS set AD_FILE_UID = ? where USER_ID = ?"
        cur.execute(sql_text_file_upd, (r[1],r[0]))

    cur.close()
    con.commit()
    con.close()


def refresh_scoreSr():

    con = sqlite3.connect('otomoto.db')
    cur = con.cursor()



    sql_text_scoreSr = """
                        select a.AD_ID, a.CAR_MAKE, a.CAR_MODEL, a.SEGMENT_CODE, a.FUEL_TYPE, a.PRICE, u.ADD_CNT, u.USER_TYPE
                        from ADS_LAST a
                            inner join
                            USERS u
                            on a.USER_ID = u.USER_ID
                        """

    sql_out = list (con.execute(sql_text_scoreSr).fetchall())
    for r in sql_out:
        print (r)
        v_score = scoreCarSr ( r[1], r[2], r[3], r[4], r[5], r[6], r[7])
        sql_update = "update ADS_LAST set SCORE_SR = ? where AD_ID = ? "
        con.execute(sql_update, (v_score, r[0]))

    con.commit()
    con.close()



# pobierz plik z html'em dla konkretnego samochodu (znajdz go w repo albo pobierz z sieci)
# rejrestruje go w FILES i ADS_LAST
# in_file_run jest potrzebny tylko gdy musze utworzyc nowy plik
def getAdFile (in_ad_id, in_file_run, con):

    # con = sqlite3.connect('otomoto.db')
    cur = con.cursor()

    sql_text_ad = "select FILE_UID, FILE_FOLDER, FILE_NAME, FILE_RUN from FILES where FILE_NAME = ? order by FILE_RUN desc"
    sql_out = cur.execute(sql_text_ad, (in_ad_id,)).fetchone()



    # sprawdzic czy plik jest na dysku

    if sql_out is not None and sql_out[0] is not None:
        # plik istnieje w bazie
        v_file_uid = sql_out[0]
        (v_file_directory, v_file_name) = (sql_out[1], sql_out[2])
        v_full_file_path = v_file_directory + '/' + v_file_name + '.html'
        with open (v_full_file_path, 'r', encoding="utf-8") as file:
            html_string = file.read ()
        # con.commit()
        # con.close()
        return (v_file_uid, html_string)

    # plik nie istnieje i trzeba go pobrac
    print ('pobieram plik z sieci')
    sql_text_ad = "select HTML_AD from ADS_LAST where AD_ID = ?"
    sql_out = cur.execute(sql_text_ad, (in_ad_id,)).fetchone()
    v_ad_html = sql_out[0]

    req = requests.get (v_ad_html)
    html_string = req.text
    req.close()


    v_file_name = in_ad_id
    v_file_folder = f"data/{in_file_run}/car_details"
    v_full_file_path = f"{v_file_folder}/{v_file_name}.html"
    with open (v_full_file_path, 'w', encoding="utf-8") as file:
        file.write (html_string)

    v_file_uid = str (uuid.uuid4())
    sql_text_file = """
                    insert into FILES (file_uid, file_folder, file_run, file_name, file_date, file_type)
                    values (?, ?, ?, ?, ?, ?)
                    """
    cur.execute(sql_text_file, (v_file_uid, v_file_folder, in_file_run, v_file_name, 'null', 'ad') )


    sql_text_ad = "update ADS_LAST set AD_FILE_UID = ? where AD_ID = ?"
    cur.execute(sql_text_ad, (v_file_uid, in_ad_id) )


    # con.commit()
    # con.close()

    return (v_file_uid, html_string)



# pobierz podstawowe atrybuty samochodu (price, fuel_type ...) na podstawie naglowka
def getCarThumbnailAttr(art):

    v_make = ''
    v_year = ''
    v_mileage = ''
    v_fuel_type= ''
    v_price = 0
    v_title_short = ''
    v_ad_id = ''
    v_title_2nd_word = ''
    v_title_3rd_word = ''
    v_title_complement = ''
    v_user_id = ''
    v_html_link= ''

    tag_a = art.find("a", title=True)
    tag_a_title = art.find("a", "offer-title__link")
    tag_h3_title_complement = art.find("h3", "offer-item__subtitle ds-title-complement hidden-xs")
    tag_ul = art.find("ul", "ds-params-block")
    tag_span_price = art.find("span", "offer-price__number ds-price-number")
    # tag_img = art.find ("img", "")  data-src
    # print ('--------------------------------')
    v_title_long = tag_a['title']
    v_title_short = tag_a_title['title']
    v_title_2nd_word = v_title_short.split()[1]
    if len(v_title_short.split()) >= 3:
        v_title_3rd_word = v_title_short.split()[2]
    else:
        v_title_3rd_word = 'null'
    v_ad_id = art['data-ad-id']
    v_user_id = art.get('data-user-id')
    if tag_h3_title_complement:
        v_title_complement = tag_h3_title_complement.text
    else:
        v_title_complement = ""
    if art.attrs.get('data-href'):
        v_html_link = art['data-href']
        v_make = art['data-param-make']

        tag_year = tag_ul.find("li", attrs={"data-code": "year"})
        if tag_year:
            v_year = tag_year.text.strip()

        tag_mileage = tag_ul.find("li", attrs={"data-code": "mileage"})
        if tag_mileage:
            v_mileage = tag_ul.find("li", attrs={"data-code": "mileage"}).text.strip()

        tag_fuel_type = tag_ul.find("li", attrs={"data-code": "fuel_type"})
        if tag_fuel_type:
            v_fuel_type = tag_fuel_type.text.strip()

        tag_price = tag_span_price.span
        if tag_price:
            v_price = tag_price.text.strip()
            v_price = v_price.replace(" ", "")
            v_price = v_price.replace(",", ".")
            v_price = float (v_price)
    else:
        v_html_link = art['href']
        v_make = ""
        v_year = ""
        v_mileage = ""
        v_fuel_type = ""
        v_price = 0

    dicAttr = { 'ad_id': v_ad_id,'user_id':v_user_id,
                'html_link': v_html_link, 'make' : v_make,
               'title_short': v_title_short, 'title_long': v_title_long, 'title_complement':v_title_complement,
               'title_2nd_word':v_title_2nd_word, 'title_3rd_word':v_title_3rd_word,
               'year' : v_year, 'mileage' : v_mileage, 'fuel_type': v_fuel_type, 'price' :v_price}

    return dicAttr


# pobierz nazwe uzytkownika, ktory wstawil ogloszenie
def getOwnerAttr(html_string):
    ad_soup = BeautifulSoup(html_string, 'html.parser')
    tag_user = ad_soup.find("h2","seller-box__seller-name")
    if tag_user is not None:
        tag_user_title = tag_user.find("a")
        if tag_user_title:
            v_user_name = tag_user_title.text
            v_user_type = 'KOMIS / SALON'
        else:
            v_user_name = 'Osoba prywatna (' + tag_user.text + ')'
            v_user_type = 'IND'
    else:
        v_user_name = 'na'
        v_user_type = 'na'

    return (v_user_name, v_user_type)



def getCarDetailsAttr (html_string):

    soup = BeautifulSoup (html_string, 'html.parser')
    tag_script = soup.findAll ("script",text=re.compile('GPT.targeting'))
    if len(tag_script) == 1:
        script_text = tag_script[0].text
    else:
        return ('-','-')

    pattern = re.compile(r"GPT.targeting\s+=\s+(\{.*?\});\n")
    data = pattern.search(script_text).group(1)
    data = json.loads(data)

    if 'body_type' in data:
        v_body_type = data['body_type'][0]
    else:
        v_body_type = '-'

    if 'country_origin' in data:
        v_country_origin = data['country_origin'][0]
    else:
        v_country_origin = '-'

    # v_country_origin = ''
    # v_country_registered_now = ''
    # c_chasis_type = ''
    # v_no_crash  = ''

    return (v_body_type, v_country_origin)