#!/usr/bin/env python

import pickle
import dblp
from os import getenv

HOME = getenv("HOME")

def main():
    with open(HOME+'/Desktop/crawl/data/origi_list.pickle','rb') as fid:
        origi_list = pickle.load(fid)

    author_pub = []
    id_last = 0

    for i in range(len(origi_list)):
        rec = origi_list[i]
        id_now = rec[u'Reviewer People ID']
        if id_now != id_last:
            id_last = id_now
            fname = rec[u'Reviewer First Name']
            lname = rec[u'Reviewer Last Name']
            temp_dic = {'fname': fname, 'lname': lname, 'id': id_now}
            url = lname[0].lower() + '/' + lname + ':' + fname
            author = dblp.Author(url)
            author.load_data()
            update_dic(temp_dic, author.data)
            author_pub.append(temp_dic)

    print 'len of authors is',len(author_pub)

    with open(HOME+'/Desktop/crawl/data/author_pub.pickle','wb') as fid:
        pickle.dump(author_pub,fid)


def update_dic(dic,data):
    print 'process id ',dic['id']
    dic['fail'] = False
    dic['homo'] = False
    dic['pub_url'] = []
    dic['pub_list'] = []
    if data is not None:
        if data['homonyms'] == []:
            pub_list = []
            for one_pub in data['publications']:
                one_pub.load_data()
                pub_list.append(one_pub.data)
            dic['pub_list'] = pub_list
        else:
            dic['homo'] = True
    else:
        dic['fail'] = True


if __name__ == '__main__':
    main()
