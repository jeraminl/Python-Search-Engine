from tkinter import *
from search_engine import *

class SearchGUI:
    def __init__(self):
        self.se = SearchEngine('index.json', 'bookkeeping.json')
        
        self.root = Tk()

        self.root.title("Search Engine")
        self.root.geometry('1000x1000')

        self.search_bar = Frame(self.root)
        self.search_bar.pack()

        self.search_label = Label(self.search_bar, text="What would you like to search?")
        self.search_label.pack(side = LEFT)

        self.search_entry = Entry(self.search_bar, bd = 5, width = 20)
        self.search_entry.pack(side = LEFT)

        self.query = StringVar()
        self.search_button = Button(self.search_bar, text="Search", command=self.showResults)
        self.search_button.pack(side = LEFT)

        self.search_results = Frame(self.root)
        self.search_results.pack()
        self.list_results = Listbox(self.search_results)
        self.list_results.pack(side = LEFT, fill = BOTH, expand = 1)

        for i in range(20):
            self.list_results.insert(END, str(i))

        self.root.update()
        #self.root.mainloop()

    def showResults(self):
        #se = SearchEngine('index.json', 'bookkeeping.json')
        queries = self.se.format_query(self.search_entry.get())
        ranking = self.se.docRanking(queries)
        i = 0
        for key in ranking.keys():
            if i < 20:
                self.list_results.insert(END, str(i+1)+"\t" + key + "\t" + self.se.book[key])
                print(str(i+1)+"\t" + key + "\t" + self.se.book[key])
                i+=1
        self.root.update()

if __name__ == '__main__':
    search = SearchGUI()
    search.root.mainloop()

