from bs4 import BeautifulSoup


def xml_parser(text):
    dic = {}
    soup = BeautifulSoup(text, 'html.parser')
    print(soup)
    div = soup.find(name='error')
    for item in div.find_all(recursive=False):
        dic[item.name] = item.text
    print(dic)


text1 = "<error><ret>0</ret><message></message><skey>@crypt_1567ce_3da1aaac6372f509db8290aa75c690e4</skey><wxsid>SsVFCxwRoNNZNi84" \
       "</wxsid><wxuin>293015240</wxuin><pass_ticket>B98m3D5LCmt9Onq5ezTWc8vdAqUce8IhdgAWI2gU3fdI2q26FoaxEjNl1hg3%2BTrq</pass_ticket><isgrayscale>1</isgrayscale></error>"

xml_parser(text1)
