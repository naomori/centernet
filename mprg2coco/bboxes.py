import sys
import pandas as pd

class BoundingBoxes:
    def __init__(self, filename,
                 delimiter=' ', width=1280, height=960, normalize=True):
        self.field_names =\
            ['item_id', 'center_x', 'center_y', 'width', 'height']
        self.field_dtype =\
            { self.field_names[0]: 'int',
              self.field_names[1]: 'float',
              self.field_names[2]: 'float',
              self.field_names[3]: 'float',
              self.field_names[4]: 'float' }
        self.delimiter = delimiter
        self.width = width
        self.height = height
        self.normalize = normalize
        if filename:
            self.read(filename)

    def read(self, filename):
        self.filename = filename
        self.df = pd.read_csv(filename, header=None, sep=' ',
                              names=self.field_names, index_col=0,
                              dtype=self.field_dtype)
        self.df['center_x_pixel'] = self.df['center_x'] * self.width
        self.df['center_y_pixel'] = self.df['center_y'] * self.height
        self.df['width_pixel'] = self.df['width'] * self.width
        self.df['height_pixel'] = self.df['height'] * self.height

    def fetch_df(self):
        return self.df

    def show(self):
        print(self.df)

if __name__ == "__main__":
    args = sys.argv
    filename = args[1]

    bboxes = BoudingBoxes(filename)
    bboxes.show()

    df_bboxes = bboxes.fetch_df()
    print(len(df_bboxes))
    for df_bbox in df_bboxes.itertuples():
        print(df_bbox.Index,
              df_bbox.center_x_pixel, df_bbox.center_y_pixel,
              df_bbox.width_pixel, df_bbox.height_pixel)
