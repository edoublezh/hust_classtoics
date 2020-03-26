import urllib

import ics_write
from selenium import webdriver
import time
import datetime
import urllib
import urllib.request
import json

# browser = webdriver.Chrome()
cookie_send = 'JSESSIONID=r4S2geDFr-1y5jz30EJX0y0alObdfe5vUQPDMbW8QO-bb_84vaws!-454866768;username=U201714656;BIGipServerpool_122.205.11.9_80=2047478282.22811.0000';


def get_cookie(stuid, password):
    browser = webdriver.Chrome()
    browser.delete_all_cookies()
    browser.get('https://pass.hust.edu.cn/cas/login?service=http%3A%2F%2Fhub.hust.edu.cn%2Fhustpass.action')
    time.sleep(1)
    # 未进入则刷新
    if browser.title != '智慧华中大 | 统一身份认证系统':
        browser.refresh()
        time.sleep(2)
    elem = browser.find_element_by_id('un')
    elem.send_keys(stuid)
    elem = browser.find_element_by_id('pd')
    elem.send_keys(password)
    browser.find_element_by_id('index_login_btn').click()
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[-1])
    list_cookies = browser.get_cookies()

    global cookie_send
    cookie_send = "%s=%s;%s=%s;%s=%s" % (
    list_cookies[2]['name'], list_cookies[2]['value'], list_cookies[0]['name'], list_cookies[0]['value'],
    list_cookies[1]['name'], list_cookies[1]['value'])
    # browser.quit()


def getcourse(begin_time, end_time):
    print('等待抓取课程')

    headers4 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Length': '30',
        'Host': 'hubs.hust.edu.cn',
        'Connection': 'Keep-Alive',
        'Pragma': 'no-cache',
        'Cookie': None

    }

    headers4['Cookie'] = cookie_send
    params4 = {
        'start': '2019-09-26',
        'end': '2019-11-07'
    }
    params4['start']=begin_time
    params4['end']=end_time
    bdata4 = urllib.parse.urlencode(params4).encode('ascii')

    url = 'http://hubs.hust.edu.cn/aam/score/CourseInquiry_ido.action'
    req4 = urllib.request.Request(url, bdata4, headers=headers4)
    response4 = urllib.request.urlopen(req4)
    data4 = json.loads(response4.read().decode('utf-8'))
    # js=json.dumps(data4,ensure_ascii=False,indent=2)
    # print(js)
    with open('lessons.json', 'w') as f:
        f.write(json.dumps(data4, ensure_ascii=False))


def trans_ics():
    with open("lessons.json","r") as f:
        lessons=json.loads(f.read())
    lesson_num=len(lessons)
    a=eval(lessons[0]['txt'])
    calendar = ics_write.Calendar(calendar_name="test")
    copylessons=[lessons[0]]
    for i in range(1,lesson_num):
        if lessons[i] not in copylessons:
            copylessons.append(lessons[i])


    for i in range(0,len(copylessons)):
        if i%2:
            lessonstatus = eval(copylessons[i]['txt'])
            a = copylessons[i]['start']
            starttime = datetime.datetime.strptime(copylessons[i]['start'], "%Y-%m-%d %H:%M")
            endtime = datetime.datetime.strptime(copylessons[i]['end'], "%Y-%m-%d %H:%M")
            ics_write.add_event(calendar,
                                SUMMARY=copylessons[i]['title'],
                                DTSTART=starttime,
                                DTEND=endtime,
                                DESCRIPTION=lessonstatus['JGXM'],
                                LOCATION=lessonstatus['JSMC'])

    print(calendar.get_ics_text())
    calendar.save_as_ics_file()


def save(string):
    f = open("class.ics", 'wb')
    f.write(string.encode("utf-8"))
    f.close()






if __name__ == '__main__':
    get_cookie('学号', '姓名')
    getcourse('2020-02-11', '2020-07-00')
    trans_ics()