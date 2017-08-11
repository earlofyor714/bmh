

class ExploreVisualizer:
    def __init__(self, cols):
        self.cols = cols
        self.bats = []
        self.water = []
        self.rusty = []
        self.etc = []

    def split_cols(self):
        self.bats = self.split("bat")
        self.water = self.split("water")
        self.rusty = self.split("rusty")

    def split(self, regex):
        cols = self.choose_cols()
        temp_etc = []
        splitted = []

        for col in cols:
            if regex in col:
                splitted.append(col)
            else:
                temp_etc.append(col)

        self.etc = temp_etc
        return splitted

    def choose_cols(self):
        if len(self.etc) < 1:
            return self.cols

        return self.etc

# look into splitting by level (difficulties / game speeds change
#
