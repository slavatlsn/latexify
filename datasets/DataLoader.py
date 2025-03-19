class Dataset(torch.utils.data.Dataset):

    def __init__(self, directory):
        syms = os.listdir(directory)
        data = {'data': [], 'labels': []}
        l = 0
        i = 0
        classes = dict()
        self.datamap = dict()
        self.dir = directory
        self.tens = t.ToTensor()
        for el in syms:
            if os.path.isdir(directory + '/' + el):
                l += len(os.listdir(directory + '/' + el)) 
                self.datamap[el] = l
                classes[el] = i
                i += 1
        self.classes = classes
        self.len = l

    def __len__(self):
        return self.len

    def __getitem__(self, index):
        res = now = ''
        items = list(self.datamap.keys())
        prev = items[0]
        for el in items[1:]:
            if self.datamap[el] > index:
                res = prev
                now = el
                break
            prev = el
        im = None
        lst = os.listdir(self.dir + '/' + now)
        with Image.open(self.dir + '/' + now + '/' + lst[index - self.datamap[res]]) as image:
            im = self.tens(image)
        return im, self.classes[prev]

def DataLoader(directory, batch_size, if_shuffle):
    return torch.utils.data.DataLoader(
            dataset = Dataset(directory),
            batch_size = batch_size,
            shuffle = if_shuffle,
            drop_last = True)
