import os
import tkFileDialog
import tkMessageBox
from Tkinter import *
from model import *


def classify(root):
    try:
        # classify the test set with the model built
        model.classify()
        tkMessageBox.showinfo("Naive Bayes Classifier", "Classification done!")
        root.destroy()  # close the main window
        sys.exit(0)  # exit program
    except NameError:
        tkMessageBox.showerror("Naive Bayes Classifier", "Build the model first!")
    except SystemExit:
        pass
    except:
        tkMessageBox.showerror("Naive Bayes Classifier", "Something went wrong")


def build(tk_path, tk_bins):
    # check if path is valid
    dir_path = tk_path.get()
    if not os.path.isdir(dir_path):
        tkMessageBox.showerror("Naive Bayes Classifier", "Path is not a folder")
        return

    # check if number of bins is valid
    try:
        bins = int(tk_bins.get())
        if bins <= 0:
            tkMessageBox.showerror("Naive Bayes Classifier", "Number must be positive")
            return
    except:
        tkMessageBox.showerror("Naive Bayes Classifier", "Number of bins is not an integer")
        return

    # go throw the folder given to check if all the files exist
    file_list = []
    for file_name in os.listdir(dir_path):
        file_list.append(file_name)
    if not 'train.csv' in file_list or 'test.csv' not in file_list or 'Structure.txt' not in file_list:
        tkMessageBox.showerror("Error", "One or more files are missing from the given folder")
        return
    global model
    try:
        # build the model
        model = NaiveBayesModel(dir_path, bins)
        tkMessageBox.showinfo("Information", "Building classifier using train-set is done!")
    except:
        tkMessageBox.showerror("Error", "Something went wrong, please try again")


def browse(tk_path_entry):
    # open folder dialog to choose folder
    dir_path = tkFileDialog.askdirectory(title='Naive Bayes Classifier')
    tk_path_entry.set(dir_path)


def build_window(root):
    root.title("Naive Bayes Classifier")
    root.geometry('500x250')

    main_frame = Frame(root)
    main_frame.pack()

    # Tkinter variables
    dir_path = StringVar()
    dis_bins = StringVar()

    # Labels
    lbl_dir_path = Label(main_frame, text="Directory Path: ")
    lbl_dir_path.grid(sticky='E', row=0, column=0, pady=30)

    lbl_dis_bins = Label(main_frame, text="Discretization Bins: ")
    lbl_dis_bins.grid(row=1, column=0)

    # Entries
    entry_dir_path = Entry(main_frame, width=50, textvariable=dir_path)
    entry_dir_path.grid(row=0, column=1)

    entry_dis_bins = Entry(main_frame, width=15, textvariable=dis_bins)
    entry_dis_bins.grid(sticky='W', row=1, column=1)

    # Buttons
    btn_browse = Button(main_frame, text='Browse', command=lambda: browse(dir_path))
    btn_browse.grid(row=0, column=2, padx=3)

    btn_build = Button(main_frame, text='Build', command=lambda: build(dir_path, dis_bins), width=20)
    btn_build.grid(row=2, column=1, pady=30)

    btn_classify = Button(main_frame, text='Classify', command=lambda: classify(root), width=20)
    btn_classify.grid(row=3, column=1)


def main():
    root = Tk()
    build_window(root)
    root.mainloop()


if __name__ == "__main__":
    main()
