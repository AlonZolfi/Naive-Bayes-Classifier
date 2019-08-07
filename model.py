import pandas as pd
import numpy as np


class NaiveBayesModel:

    def __init__(self, dir_path, num_of_bins):
        self.dir_path = dir_path  # save the path of the directory given
        self.num_of_bins = num_of_bins  # save the number of bins wanted
        self.data_structure = self.get_struct_data()  # parse the Structure.txt file
        self.train_df = pd.read_csv(dir_path+"/train.csv")  # save the train file in data frame
        if self.train_df.shape[0] == 0:
            raise Exception
        self.fill_missing_data(self.train_df)  # fill the missing data
        self.discretization_to_bins(self.train_df) # discretsize all numeric columns

    def get_struct_data(self):
        struct_data = {}  # {column name: type,.. }
        with open(self.dir_path+"/Structure.txt", "r") as struct_file:
            # get all lines from file
            struct_lines = struct_file.readlines()
            for line in struct_lines:
                if line.__contains__('{'):  # in case of non numeric data
                    column_val = line[line.find('{')+1:line.rfind('}')]
                else:  # numeric data
                    column_val = 'NUMERIC'
                split_arr = line.rsplit(" ")
                struct_data[split_arr[1]] = column_val
            return struct_data

    def fill_missing_data(self, data_frame):
        for column in self.data_structure:  # for each column fill data
            column_val = self.data_structure[column]
            if column_val == 'NUMERIC':  # if data is numeric fill with mean
                data_frame[column] = data_frame.groupby('class')[column].apply(lambda x: x.fillna(x.mean()))
            else:  # if data is not numeric fill with mode
                data_frame[column].fillna((data_frame[column].mode()[0]), inplace=True)

    def discretization_to_bins(self, data_frame):
        for column in self.data_structure:  # for each column
            column_val = self.data_structure[column]
            if column_val == 'NUMERIC':  # if column is numeric
                # calculate equal width
                max_val = data_frame[column].max()
                min_val = data_frame[column].min()
                width = (max_val - min_val) / self.num_of_bins
                # assign labels
                labels = range(1,self.num_of_bins+1)
                # create ranges array
                bins = [-np.inf]
                for i in range(1,self.num_of_bins):
                    bins.append(min_val+i*width)
                bins.append(np.inf)
                #discretisize the column
                data_frame[column] = pd.cut(data_frame[column], bins=bins, labels=labels)

    def classify(self):
        test_df = pd.read_csv(self.dir_path+"/test.csv") #  read test set from the folder
        self.fill_missing_data(test_df)  # fill missing data in test set
        self.discretization_to_bins(test_df)  # discretisize test set

        # calculate the probability of each value in class feature
        class_prob = self.train_df['class'].value_counts(normalize=True)

        # get the name of the values of the class
        class_values = self.data_structure['class'].split(",")

        with open(self.dir_path + "/output.txt", "w") as output_file:
            for index, row in test_df.iterrows():  # for each row in the test set
                cond_prob = [1, 1]  # each cell will represent the probability of each value in class
                for col in self.data_structure:  # for each column in the
                    if not col == 'class':
                        # calculate conditional probability of P(col_name = row [col_name] | class = y/n)
                        cond_prob[0] *= self.calc_prob_feature(col,row[col],class_values[0])
                        cond_prob[1] *= self.calc_prob_feature(col,row[col],class_values[1])
                # multiply with probability of each value in class
                prob = [class_prob[0] * cond_prob[0], class_prob[1] * cond_prob[1]]
                # get the max posterior
                str_res = class_values[np.argmax(prob)]
                # write it to the output file
                output_file.write(str(index + 1) + " " + str_res + "\n")

    def calc_prob_feature(self, col_name, row_val, class_val):
        # number of rows where col_name = row_val and class = class_val
        nc = self.train_df[((self.train_df[col_name] == row_val) & (self.train_df['class'] == class_val))].count()[0]
        # number of appearances of the class_val
        n = self.train_df['class'].value_counts()[class_val]
        if self.data_structure[col_name] == 'NUMERIC':
            mechane = self.num_of_bins
        else:
            mechane = len(self.data_structure[col_name].split(","))
        p = 1.0 / mechane  # uniform distribution of class
        m = 2  # m-estimator
        m_estimate = (nc + m*p) / (n + m)
        return m_estimate
