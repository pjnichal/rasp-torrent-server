import pdb
import time


from transmission_rpc import Client
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://torrentserver-8847c-default-rtdb.asia-southeast1.firebasedatabase.app/'})

torrentToAdd = db.reference('/TorrentToBeAdded')
torrentAdded = db.reference('/TorrentAdded')
time.sleep(30)
client=Client(host='192.168.31.218',port=9091,username='root', password='root')
# ##############TORRENT METHODS################################


def addTorrent(link):
    client.add_torrent(link)

#


def getAllTorrent():
    torrentarry = client.get_torrents()
    return torrentarry


def removeTorrentWithData(id):
    client.remove_torrent(id, delete_data=True)
#


def removeTorrentFromList(id):
    client.remove_torrent(id)
#


def pauseTorrent(id):
    client.stop_torrent(id)
#


def startTorrent(id):
    client.start_torrent(id)

##############FIREBASE METHODS################################


def dbaddTorrent():
    toaddtorrent = torrentToAdd.get()
    print(toaddtorrent)
    if(toaddtorrent != None):
        for key, value in toaddtorrent.items():
            if(value['isAdded'] == False):
                print(value['magnetlinks'])
                try:
                    addTorrent(value['magnetlinks'])
                    torrentToAdd.child(key).update({'isAdded': True})
                except Exception:
                    torrentToAdd.child(key).update({'isAdded': True})


def dbremovelinks():
    toaddtorrent=torrentToAdd.get()
    if(toaddtorrent!=None):
        for key,value in toaddtorrent.items():
            if(value['isAdded']==True):
                torrentToAdd.child(key).delete()

def dbgetAllTorrent():
    alltorrent = getAllTorrent()
    for t in alltorrent:
        if (t.progress > 0):
            addedtorrent = torrentAdded.get()
            if(addedtorrent != None):
                has=False
                for key, value in addedtorrent.items():

                    if(value['name'] == t.name):
                        has=True
                        torrentAdded.child(key).update({'status': t.status, 'rate_download': t.rateDownload,
                                                        'progess': t.progress, 'total_size': t.total_size, 'left_until_done': t.left_until_done})

                if(has==False):
                 print('this 1')
                 torrentAdded.push({'id': t.id, 'name': t.name, 'status': t.status, 'rate_download': t.rateDownload,
                 'progess': t.progress, 'total_size': t.total_size, 'left_until_done': t.left_until_done, 'isPause': 1, 'isDelete': False, 'isDeleteWithData': False})
            else:
                print('this')
                torrentAdded.push({'id': t.id, 'name': t.name, 'status': t.status, 'rate_download': t.rateDownload,
                                   'progess': t.progress, 'total_size': t.total_size, 'left_until_done': t.left_until_done,
                                   'isPause': 1, 'isDelete': False, 'isDeleteWithData': False})


def dbPauseTorrent():
    alltorrent = torrentAdded.get()
    if(alltorrent != None):
        for key, value in alltorrent.items():
            print(value['isPause'])
            if(value['isPause'] == 2):
                pauseTorrent(value['id'])


def dbstartTorrent():
    alltorrent = torrentAdded.get()
    if (alltorrent != None):
        for key, value in alltorrent.items():
            if (value['isPause'] == 3):
                startTorrent(value['id'])
                torrentAdded.child(key).update({'isPause': 1})


def dbRemoveTorrent():
    alltorrent = torrentAdded.get()
    if(alltorrent != None):
        for key, value in alltorrent.items():
            if(value['isDelete'] == True):
                removeTorrentFromList(value['id'])
                torrentAdded.child(key).delete()


def dbRemoveWithDataTorrent():
    alltorrent = torrentAdded.get()
    if(alltorrent != None):
        for key, value in alltorrent.items():
            if(value['isDeleteWithData'] == True):
                removeTorrentWithData(value['id'])
                torrentAdded.child(key).delete()


if __name__ == '__main__':
    
   
    while(True):
        dbgetAllTorrent()
        dbstartTorrent()
        dbaddTorrent()
        dbPauseTorrent()
        dbRemoveTorrent()
        dbRemoveWithDataTorrent()
        dbremovelinks()
        time.sleep(3)
