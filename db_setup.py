import sqlite3

con = sqlite3.connect('otomoto.db')
cur = con.cursor()


for row in cur.execute("select NAME from sqlite_master where TYPE = 'table' and NAME not in ('sqlite_sequence')").fetchall():
    print (f"drop table {row[0]}")
    cur.execute(f"drop table {row[0]}")
#
# print ('-----')
#
cur.execute("create table FILES (file_uid PRIMARY KEY, file_folder, file_run, file_name, file_date, file_type, file_status, file_html) ")

# cur.execute("create table ADS_ALL (ad_id, ins_ts, ver_id, sres_file_uid, user_id, "
#             "car_make, title_short, title_complement, price, price_fv, year, fuel_type, mileage,"
#             "html_details, html_main_pic ) ")

cur.execute("create table ADS_LAST (ad_id, upd_ts, "
            "last_sres_file_uid, user_id,"
            "car_make, title_short, title_complement, "
            "price, price_fv, year, fuel_type, mileage, "
            "title_2nd_word, title_3rd_word, "
            "fst_seen_dt, last_seen_dt, last_detail_seen_dt, "
            "segment_code, car_model, score_sr, score_ad,"
            "html_ad, ad_file_uid, html_main_pic,"
            "ad_body_type, ad_country_origin ) ")

# cur.execute("create table AD_DETAILS_ALL (details_id INTEGER PRIMARY KEY, ad_id, ver_id, file_id  ) ")

cur.execute("create table USERS (user_id PRIMARY KEY, upd_ts, "
            "first_ad_id, last_ad_id, "
            "ad_file_uid, "
            "add_cnt, user_type, user_name)"  )


for row in cur.execute("select * from sqlite_master where NAME not in ('sqlite_sequence')"):
    print (row)

print ('-----')


