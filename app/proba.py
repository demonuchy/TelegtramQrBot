import segno 
import io
#
def sort_key(massiv: list | str, key: int = 0):
    try:
        for i in range(len(massiv)):
            value=massiv[i][0]
            massiv[i][0]=massiv[i][key]
            massiv[i][key]=value
        return massiv

    except:
        return print('Ключем являеться максимальный индекс подмасива',[type(item) for item in massiv])


#
def sort_bubble(massiv: list | str):
    massiv_intgr=[]
    massiv_strng=[]
    try:

        massiv=list(map(ord, massiv))
        for item in range(len(massiv)-1):
            if massiv[item] > massiv[item+1]:

                value = massiv[item]
                massiv[item] = massiv[item+1]
                massiv[item+1] = value
                sort_bubble(massiv)
                return list(map(chr, massiv))
        return list(map(chr, massiv))

    except TypeError:
        try:
            for item in range(len(massiv) - 1):
                if massiv[item] > massiv[item + 1]:

                    value = massiv[item]
                    massiv[item] = massiv[item + 1]
                    massiv[item + 1] = value
                    sort_bubble(massiv)
                    return massiv
            return massiv
        except:
            try:
                for item in massiv:
                    if isinstance(item,int):
                        massiv_intgr.append(item)
                    else:
                        massiv_strng.append(item)
            finally:
                return sort_bubble(massiv_intgr)+sort_bubble(massiv_strng)

#
def sort_bobble_with_key(massiv: list | str, key: int = 0):
    try:
        for item in massiv:
            if isinstance(item,list):
                sort_key(massiv=massiv, key=key)
                return sort_bubble(massiv=sort_key(massiv))
            return sort_bubble(massiv)

    except:
        return sort_bubble(massiv)


d=[
   1231,',ejfer',53534,'23354'
]


qr=segno.make("https://dzen.ru/a/XuuyWxUXzh1fpiRj")
#qr.save("users/qr689579806/qr.png")
print(qr.save(io.BytesIO()))