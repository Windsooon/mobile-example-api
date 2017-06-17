import json
import time
import requests


class Mobike:

    def __init__(
        self, mobike_no,
        token, bikecode,
        citycode, latitude, longitude
    ):
        self.base_url = 'http://api.test1.mobike.io/mobike-api/'
        self.mobike_no = mobike_no
        self.token = token
        self.bikecode = bikecode
        self.citycode = citycode
        self.latitude = latitude
        self.longitude = longitude
        r = self.user_info()
        self.accesstoken = r['object']['authtoken']
        self.headers = {
            'accesstoken': self.accesstoken
        }
        self.userid = r['object']['userid']

    def user_info(self):
        url = (
            self.base_url + 'usermgr/' +
            'partnerlogin.do?mobileNo=' + self.mobike_no +
            '&access_token=' + self.token
        )
        r = requests.post(url=url)
        return r.json()

    def open_lock(self):
        headers = {
            'accesstoken': self.accesstoken,
            'platform': '99'
        }
        url = (
            self.base_url + 'rentmgr/' + 'unlockBike.do?bikecode=' +
            self.bikecode + '&latitude=' + self.latitude +
            '&longitude=' + self.longitude + '&timestamp=' +
            str(int(time.time())) + '&citycode=' + self.citycode +
            '&userid=' + self.userid + '&channel=0')
        r = requests.post(url=url, headers=headers)
        self.orderid = r.json()['object']
        return r.json()

    def ride_status(self):
        url = (
            self.base_url + 'rentmgr/getridestate.do' +
            '?userid=' + self.userid)
        r = requests.post(url=url, headers=self.headers)
        return r.json()

    def order_status(self):
        orderid = 'MBK75501011831497684558822'
        url = (
            self.base_url + 'rentmgr/orderinfo.do' +
            '?userid=' + self.userid + '&orderid=' + orderid)
        r = requests.get(url=url, headers=self.headers)
        return r.json()

    def account_status(self):
        url = self.base_url + 'pay/downpayment.do' + '?userid=' + self.userid
        r = requests.get(url=url, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    with open('info.json') as json_data:
        base_info = json.load(json_data)

    mobike = Mobike(
        base_info['phone'], base_info['token'],
        base_info['bikecode'], base_info['citycode'],
        base_info['latitude'], base_info['longitude'],
    )
    # mobike.open_lock()
    # mobike.ride_status()
    # mobike.order_status()
    # mobike.account_status()
