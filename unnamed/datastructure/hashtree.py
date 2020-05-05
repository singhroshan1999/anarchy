class hashtree:
    def __init__(self):
        self.tree = {}
    def add(self,phash,dhash):
        temp = self.tree
        prev = {}
        for i in phash:
            if(i in temp):
                prev = temp
                temp = temp[i]
            else:
                prev = temp
                temp[i] = {}
                temp = temp[i]
        if type(prev[phash[-1]]) == list:
            prev[phash[-1]].append(dhash)
        else:
            prev[phash[-1]] = [dhash]
    def get(self,phash):
        temp = self.tree
        for i in phash:
            if i in temp:
                temp = temp[i]
            else:
                return -1
        return len(temp)
if __name__ == "__main__":
    tree = hashtree()
    tree.add("5345234534534","tretertertert")
    tree.add("6787897645345","545reyter673456tert")
    tree.add("6787897645345", "bcvnbjfhrgsdfsdfddgh")
    print(tree.get("ertertetrert"))