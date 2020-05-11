class Wrap:
    def __init__(self, data=None):
        self.bc = []
        if data is not None:
            self.bc.append(data)

    @staticmethod
    def dictToBen(d):
        dout = {}
        for i in d.keys():
            if isinstance(i,int):
                k = Wrap.intToBen(i)
            elif isinstance(i,str):
                k = Wrap.strToBen(i)
            else:
                raise Exception
            if isinstance(d[i], int):
                dout[Wrap.reduceToBytes(k)] = Wrap.reduceToBytes(Wrap.intToBen(d[i]))
            elif isinstance(d[i], str):
                dout[Wrap.reduceToBytes(k)] = Wrap.reduceToBytes(Wrap.strToBen(d[i]))
            elif isinstance(d[i], list):
                dout[Wrap.reduceToBytes(k)] = Wrap.reduceToBytes(Wrap.listToBen(d[i]))
            elif isinstance(d[i], dict):
                dout[Wrap.reduceToBytes(k)] = Wrap.reduceToBytes(Wrap.dictToBen(d[i]))
            elif isinstance(d[i], Wrap):
                dout[Wrap.reduceToBytes(k)] = Wrap.reduceToBytes(d[i])
            else:
                raise Exception
        return Wrap(Wrap.reduceToBytes(Wrap(dout)))
        pass

    @staticmethod
    def listToBen(lst):
        l = []
        for i in lst:
            if isinstance(i, int):
                l.append(Wrap.reduceToBytes(Wrap.intToBen(i)))
            elif isinstance(i, str):
                l.append(Wrap.reduceToBytes(Wrap.strToBen(i)))
            elif isinstance(i, list):
                l.append(Wrap.reduceToBytes(Wrap.listToBen(i)))
            elif isinstance(i, dict):
                l.append(Wrap.reduceToBytes(Wrap.dictToBen(i)))
            elif isinstance(i, Wrap):
                l.append(Wrap.reduceToBytes(i))
            else:
                raise Exception
        return Wrap(Wrap.reduceToBytes(Wrap(l)))

    @staticmethod
    def intToBen(i):
        return Wrap(bytes("i" + str(i) + "e", encoding="utf-8"))

    @staticmethod
    def strToBen(string):
        return Wrap(bytes(str(len(string)) + ":" + string, encoding="utf-8"))

    @staticmethod
    def reduceToBytes(wrp):
        out = b""
        for i in wrp.bc:
            if isinstance(i, bytes):
                out += i
            elif isinstance(i, list):
                out += b"l"
                for j in i:
                    out += j
                out += b"e"
            elif isinstance(i, dict):
                out += b"d"
                for j in i.keys():
                    out += j + i[j]
                out += b"e"
            else:
                raise Exception
        return out

    @staticmethod
    def bytesToReduce_r(st):
        wrp = Wrap()
        i = 0
        while i < len(st) - 1:
            if st[i].isdigit():
                ln = int(st[i:st.find(":", i)])
                fnd = st.find(":", i)
                wrp.bc.append(st[fnd + 1:fnd + ln + 1])
                i = fnd + ln + 1
            else:
                if st[i] == 'i':
                    fn = i
                    fne = st.find("e", fn + 1)
                    num = int(st[fn + 1:fne])
                    i = fn + fne - fn + 1
                    wrp.bc.append(num)
                elif st[i] == 'l':
                    fn = i
                    st2 = st[fn + 1:]
                    temp_wrp, endl = Wrap.bytesToReduce_r(st2)
                    wrp.bc.append(temp_wrp.bc)
                    i = fn + endl + 2
                elif st[i] == 'd':
                    fn = i
                    st2 = st[fn + 1:]
                    temp_wrp, endl = Wrap.bytesToReduce_r(st2)
                    itr = iter(temp_wrp.bc)
                    wrp.bc.append(dict(zip(itr, itr)))
                    i = fn + endl + 2
                elif st[i] == 'e':
                    break
        return wrp, i

    @staticmethod
    def bytesToReduce(st):
        wrp,i = Wrap.bytesToReduce_r(st)
        return wrp.bc
    @staticmethod
    def toBen(d):
        return Wrap.reduceToBytes(Wrap.dictToBen(d))


if __name__ == "__main__":
    l = [1, 2, 3, 4, 5]
    print(Wrap.reduceToBytes(Wrap.dictToBen({'key2': ['Geeks', 'For', 'Geeks'], 'key1': [1, 2]})))
    print(Wrap.bytesToReduce('d4:key2l5:Geeks3:For5:Geekse4:key1li1ei2eeed4:key2l5:Geeks3:For5:Geekse4:key1li1ei2eee'))
    print(Wrap.bytesToReduce('d13:response-datad4:datad2:dbl9:sadasdads12:asdasdasdasd15:asdasdasdasdasdeee13:response-type4:DATAe'))