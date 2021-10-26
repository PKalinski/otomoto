from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import requests
import datetime
import csv
import sqlite3
import os
import glob
import uuid
import helperFunctions

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

main_html = "https://www.otomoto.pl/osobowe/od-2017/warszawa/?search%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol&search%5Border%5D=created_at_first%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=50&search%5Bcountry%5D="

READ_HTTP = 0


# opts = Options()
# opts.headless = True
# assert opts.headless  # Operating in headless mode
# browser = Firefox(options=opts)
# browser.implicitly_wait(10)
# browser.get('https://www.otomoto.pl/')



#
# browser.get("https://www.otomoto.pl/osobowe/od-2017/warszawa/?search%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol&search%5Border%5D=created_at_first%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=50&search%5Bcountry%5D=")
# browser.save_full_page_screenshot("screenshot.png")
#
#
# with open ('website.html', 'w', encoding="utf-8") as file:
#     file.write (browser.page_source)
#
# try:
#     browser.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
#     browser.save_full_page_screenshot("screenshot_2.png")
#
#     html_string = browser.page_source
#     with open ('website.html', 'w', encoding="utf-8") as file:
#         file.write (browser.page_source)
#
# finally:
#     browser.close()
#     browser.quit()


con = sqlite3.connect('otomoto.db')
cur = con.cursor()
#cur.execute("PRAGMA journal_mode=WAL;")


v_file_run = "2021_10_21_001"
v_dt_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print (v_dt_string)

# skanowanie wszystkich folderow i sprawdzanie spojnosci FILES
helperFunctions.refresh_table_files()

# uzupelnie AD_FILE_UID w tabeli ADS_LAST
helperFunctions.refresh_table_ads_last()

# uzupelnie AD_FILE_ID dla tabeli USER
helperFunctions.refresh_table_user()




# wybieram pierwszych N stron z wynikow wyszukiwania
for i in range (20):

    v_file_name = f"search_result_{i+1:02d}"
    v_file_directory = f"data/{v_file_run}/search_results"
    v_full_file_path = f"{v_file_directory}/{v_file_name}.html"


    sql_output = cur.execute("select FILE_UID from FILES where FILE_RUN = ? and FILE_NAME = ?", (v_file_run,v_file_name)).fetchall()

    # create a new row in the FILES tables
    if len (sql_output) == 0 or sql_output[0][0] is None:
        v_file_uid = str (uuid.uuid4())
        cur.execute("insert into FILES (file_uid, file_folder, file_run, file_name, file_date, file_type) "
                    "values (?,?,?,?,?,?)", (v_file_uid, v_file_directory, v_file_run, v_file_name, 'null', 'sr'))

        con.commit()
    else:
        v_file_uid = sql_output[0][0]


    if READ_HTTP == 0:
        with open (v_full_file_path, 'r', encoding="utf-8") as file:
            html_string = file.read ()

    elif READ_HTTP == 1:
        next_url = main_html + "&page=" + str (i+1)
        r = requests.get (next_url)
        html_string = r.text
        r.close()
        with open (v_full_file_path, 'w', encoding="utf-8") as file:
            file.write (html_string)



    soup = BeautifulSoup(html_string, 'html.parser')

    article_list = soup.findAll('article')

    for art in article_list:
        attrDic = helperFunctions.getCarThumbnailAttr(art)
        v_make = attrDic['make']
        v_year = attrDic['year']
        v_mileage = attrDic['mileage']
        v_fuel_type=attrDic['fuel_type']
        v_price = attrDic['price']
        v_title_short = attrDic['title_short']
        v_ad_id = attrDic['ad_id']
        v_title_2nd_word = attrDic['title_2nd_word']
        v_title_3rd_word = attrDic['title_3rd_word']
        v_title_complement = attrDic['title_complement']
        v_user_id = attrDic['user_id']
        v_html_link=attrDic['html_link']


        (v_model, v_segment) = helperFunctions.guessModelAndSegment(v_make, v_title_short, v_title_2nd_word, v_title_3rd_word)

        # sql_output = list (cur.execute("select SRES_FILE_UID from ADS_ALL where SRES_FILE_UID = ? and AD_ID = ?", (v_file_uid,v_ad_id)).fetchall())
        #
        #
        # if len (sql_output) == 0:
        #     cur.execute("insert into ADS_ALL (ad_id, ins_ts, ver_id, sres_file_uid, user_id, car_make, title_short, title_complement, "
        #                 "price, price_fv, year, fuel_type, mileage, "
        #                 "html_details, html_main_pic)"
        #                 "values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        #                 (v_ad_id, v_dt_string, 1, v_file_uid,v_user_id, v_make, v_title_short, v_title_complement,
        #                  v_price, 'null', v_year, v_fuel_type, v_mileage, v_html_link, 'null' ))

        sql_out_ad_last = cur.execute("select AD_ID from ADS_LAST where AD_ID = ?", (v_ad_id,)).fetchone()
        # this is a new ad and should be added to our DB
        if sql_out_ad_last is None:
            con.commit()
            cur.execute("insert into ADS_LAST (ad_id, upd_ts, "
                        "last_sres_file_uid, user_id,"
                        "car_make, title_short, title_complement,"
                        "title_2nd_word, title_3rd_word, "
                        "price, price_fv, year, fuel_type, mileage, "
                        "fst_seen_dt, last_seen_dt, last_detail_seen_dt,"
                        "segment_code, car_model, score_sr,"
                        "html_ad, html_main_pic) "
                        "values (?,?,"
                        "?,?,"
                        "?,?,?,"
                        "?,?,"
                        "?,?,?,?,?,"
                        "?,?,?,"
                        "?,?,?,"
                        "?,?)",
                        (v_ad_id, v_dt_string,
                         v_file_uid, v_user_id,
                         v_make, v_title_short, v_title_complement,
                         v_title_2nd_word, v_title_3rd_word,
                         v_price, 0, v_year, v_fuel_type, v_mileage,
                         'null', 'null', 'null',
                         v_segment, v_model, -1,
                         v_html_link, '--')
                        )


        else:
            # we have alread seen this ad before and we just need to update its attributes
            con.commit()
            cur.execute("update ADS_LAST "
                        "set upd_ts = ?, last_sres_file_uid = ?, user_id = ?, car_make = ?, title_short = ?, title_complement = ?,"
                            "title_2nd_word = ?, title_3rd_word = ?, "
                            "price = ?, price_fv = ?, year = ?, fuel_type = ?, mileage = ?, "
                            "fst_seen_dt = ?, last_seen_dt = ?, last_detail_seen_dt = ?,"
                            "segment_code = ?, car_model = ?, score_sr = ?,"
                            "html_ad = ?"
                        "where AD_ID = ?",
                        ( v_dt_string, v_file_uid, v_user_id, v_make, v_title_short, v_title_complement,
                          v_title_2nd_word, v_title_3rd_word,
                          v_price, 0, v_year, v_fuel_type, v_mileage,
                          'null', 'null', 'null',
                          v_segment, v_model, -1, v_html_link,
                          v_ad_id)
                        )

        con.commit()

    # end-of for art loop
#end-of for i loop



# update USER counts
sql_text_adslast = """
                    select
                        u.USER_ID, a.USER_ID, a.MIN_AD_ID, a.MAX_AD_ID, a.CNT
                    from
                        (
                        select 
                            USER_ID, min (AD_ID) as MIN_AD_ID, max (AD_ID) as MAX_AD_ID, count (*) as CNT 
                        from ADS_LAST 
                        where USER_ID is not null 
                        group by USER_ID
                        )  a
                        left outer join
                        USERS u
                        on a.USER_ID = u.USER_ID                                            
                    """
sql_out_user = cur.execute(sql_text_adslast).fetchall()
print (sql_out_user)

for r in sql_out_user:
    print (r)
    if r[0] is None:
        sql_text_ins = "insert into USERS (USER_ID, UPD_TS, FIRST_AD_ID, LAST_AD_ID, ADD_CNT) values (?,?,?,?,?)"
        cur.execute(sql_text_ins, (r[1], v_dt_string, r[2], r[3], r[4]) )
    else:
        sql_text_upd = """
                        update USERS
                        set UPD_TS = ?, LAST_AD_ID = ?, ADD_CNT = ?
                        where USER_ID = ?
                        """
        cur.execute(sql_text_upd, (v_dt_string, r[3], r[4], r[1]) )



print ('----')



print ('---ddf-')


con.commit()

# ponownie uzupelnie AD_FILE_UID, w tabeli ADS_LAST
helperFunctions.refresh_table_ads_last()

# ponownie uzupelnie AD_FILE_ID dla tabeli USER
helperFunctions.refresh_table_user()

#przeliczam SCORE_SR
helperFunctions.refresh_scoreSr()

# szukam user'ow z CNT > 1, ktorzy nie maja zadnego pliku albo zadnej nazwy i wstawiam dla nich USER_NAME
sql_text_user = """
    select 
        u.USER_ID, u.FIRST_AD_ID, 
        a.HTML_AD
    from USERS u     
         left outer join
         ( select USER_ID, max (AD_ID) as AD_ID, HTML_AD  from ADS_LAST group by USER_ID) a
         on u.USER_ID = a.USER_ID
    where ADD_CNT > 1 and (u.AD_FILE_UID is null or USER_NAME is null)"""

con.commit()

my_cursor = list (cur.execute(sql_text_user).fetchall())
for r in my_cursor:

    print (r)
    v_user_id = r[0]
    v_ad_id = r[1]

    con.commit()
    (v_file_uid, v_html_string) = helperFunctions.getAdFile(v_ad_id, v_file_run, con)
    sql_text_upd = "update USERS set AD_FILE_UID = ? where USER_ID = ?"
    cur.execute(sql_text_upd, (v_file_uid,v_user_id) )
    con.commit()

    (v_user_name, v_user_type) = helperFunctions.getOwnerAttr(v_html_string)
    sql_text_user = "update USERS set USER_TYPE = ?, USER_NAME = ? where USER_ID = ?"
    cur.execute(sql_text_user, (v_user_type, v_user_name, v_user_id) )


helperFunctions.refresh_table_ads_last()

# pobieram szczegolowe dane dla tych samochodow, ktore juz maja swoj plik
sql_text_adslast = """select AD_ID from ADS_LAST 
                        where USER_ID is not null 
                            and AD_FILE_UID is not null 
                            and SCORE_SR >= 0 and SCORE_AD is null"""
sql_out = list (cur.execute(sql_text_adslast).fetchall())
for r in sql_out:
    (v_file_uid, html_string) = helperFunctions.getAdFile (r[0],v_file_run, con)
    print ('getAdFile 1, ad_id = ', r[0])
    (v_body_type, v_country_origin) = helperFunctions.getCarDetailsAttr (html_string)
    sql_text_adslast = "update ADS_LAST set AD_BODY_TYPE = ? , AD_COUNTRY_ORIGIN = ? where AD_ID = ?"
    cur.execute(sql_text_adslast, (v_body_type, v_country_origin, r[0]))


# pobieram szczegolowe dane dla najwyzej notowanych samochodow, ktore nie maja jeszcze swojego pliku
sql_text_adslast = """select AD_ID from ADS_LAST 
                        where USER_ID is not null 
                            and SCORE_SR >= 40 
                            and SCORE_AD is null 
                            and order by SCORE_SR desc"""
sql_out = list (cur.execute(sql_text_adslast).fetchmany(50))
for r in sql_out:
    (v_file_uid, html_string) = helperFunctions.getAdFile (r[0],v_file_run, con)
    print ('getAdFile 2, ad_id = ', r[0])
    (v_body_type, v_country_origin) = helperFunctions.getCarDetailsAttr (html_string)
    sql_text_adslast = "update ADS_LAST set AD_BODY_TYPE = ? , AD_COUNTRY_ORIGIN = ? where AD_ID = ?"
    cur.execute(sql_text_adslast, (v_body_type, v_country_origin, r[0]))


sql_text = """select from ADS_LAST a, USERS u where """
#v_score = helperFunctions.scoreCarAd (score_sr, car_make, car_model, segment, user_type, user_cnt, price, country_origin, body_type):



#ad_body_type, ad_country_origin

con.commit()




con.close()