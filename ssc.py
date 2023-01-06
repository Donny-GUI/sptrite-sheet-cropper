import os 
from sys import argv
from string import punctuation
import pathlib
import shutil
import sys
import PySimpleGUI as sg
from PIL import Image


class ConsoleApplication:
    name = 'Sprite Sheet Cutter'
    username = __file__.split("/")[2]
    version = '1.1'
    author = 'Donald Guiles'
    description_box = "  [Description]"
    usage_box = "  [Usage]"
    flags_box = "  [Options]"
    newline = '\n'
    examples_box = f'  [Examples]'
    example = f'    ssc cowboy.png 6 8'
    example2 = f'    ssc /home/woody/Desktop/astronaut.png 8 9'
    description = f'    Crop sprite sheets into individual pictures by action'
    helpflags = ['-h', '--help']
    red = '\033[31m'
    italic = '\033[3m'
    reset = '\033[0m'
    green = '\033[32m'
    blue = '\033[34m'
    bold = '\033[1m'
    aldir = f'/home/{username}/ssc' if sys.platform == 'linux' else f'/Users/{username}/ssc'
    alfile = f'/home/{username}/ssc/ssc.py' if sys.platform == 'linux' else f'/Users/{username}/ssc/ssc.py'
    usage = f'    ssc <filename> <number of images per row> <number of rows>'
    show_help_sequence = [f'{bold}{name} {version}{reset}\n', usage_box, f'{usage}\n', description_box, f'{description}\n', examples_box, example, f'{example2}\n' ]
    bashrc = f'/home/{username}/.bashrc' if sys.platform == 'linux' else f'/Users/{username}/.zprofile'

    def __init__(self):
        self.checkInstalled()
        self.columns = argv[2] if len(argv) > 2 else None 
        self.rows = argv[3] if len(argv) > 3 else None
        self.filename = argv[1] if len(argv) > 1 else None
        self.args = [self.filename, self.columns, self.rows]
        self.determine_help()
        self.file_arg = self.fixFilename()
        self.extension = self.determineExtension()
        self.column_int = self.determineColumns()
        self.row_int = self.determineRows()
        self.user_input = self.file_arg, self.column_int, self.row_int

    def checkInstalled(self):
        if self.alfile != __file__:
            print(f'[{self.green}Question{self.reset}]   {self.italic}would you like to make an alias for this script?{self.reset}')
            x = input(f"[{self.blue}Answer{self.reset}] [y/n]: ")
            if x[0].lower() == 'n':
                pass
            elif x[0].lower() == 'y':
                self.makeAlias()
            elif x[0].lower() == "":
                pass
            else:
                self.checkInstalled()
    
    def makeAlias(self):
        al = input('Please Provide an Alias For this Script: ')
        for x in al:
            if x in punctuation or x in [' ', '\t', '\n']:
                print(f"You cant use character [ {self.red}{x}{self.reset} ] in an alias")
                exit()
        string = f'\nalias {al}="python3 {self.alfile}"\n'
        with open(self.bashrc, 'r') as rfile:
            lines = [x for x in rfile.readlines()]
        lines.append(string)
        with open(self.bashrc, 'w') as wfile:
            for line in lines:
                wfile.write(line)
        os.mkdir(self.aldir)
        os.sync()
        shutil.copy(src=__file__, dst=self.alfile)
        os.sync()
        print('done.')

    def showHelp(self, extra=None):
        for x in self.show_help_sequence:
            print(x)
        if extra != None: print(f'{self.red}{extra}{self.reset}')

    def determineExtension(self):
        self.file = self.filename.split("/")[-1]
        ext = self.file.split('.')[-1]
        if ext not in ['jpg', 'png', 'jpeg', 'gif']:
            self.showHelp(extra=f'ERROR Extension: Extension {ext} not supported')
            exit()
        return ext

    def determineFilename(self):
        path = pathlib.Path(self.filename)
        retv = True if path.exists() else False
        return retv
    
    def fixFilename(self):
        if "/" not in self.filename:
            if self.filename in os.listdir(os.getcwd()):
                return f'{os.getcwd()}/{self.filename}'
            else:
                self.showHelp(extra=f'ERROR LocalFile: Directory file {self.filename} could not be located')
        else:
            if not self.determineFilename():
                self.showHelp(extra= f'ERROR GlobalFile: Could not find file {self.filename}')
            else:
                return self.filename

    def determineRows(self):
        try:
            rows = int(self.rows)
            return rows
        except:
            self.showHelp()
            exit()

    def determineColumns(self):        
        try:
            col = int(self.columns)
            return col
        except:
            self.showHelp()
            exit()

    def determine_help(self):
        for x in argv:
            if x in self.helpflags:
                self.showHelp()
                break
        if None in self.args:
            self.showHelp(extra='ERROR: Please Provide All Arguments')
            exit()


class SubImage:
    """
    x_start      = x coordinate where the upper left corner of the sub image begins
    y_start      = y coordinate where the lower left corner of the sub image begins 
    column_width = the width of the column to cut, this is equal to the subimage width
    row_height   = the height of the row to cut, this is equal to the subimage height
    image_height = the height of the full image
    image_width  = the width of the full image   
    """
    def __init__(self, x_start: int, y_start: int, column_width: int, row_height: int, image_height: int, image_width: int, parent_image: str):
        self.x1 = x_start
        self.width = column_width
        self.height = row_height
        self.x2 = x_start + column_width if x_start != image_width else None
        self.xvalid = True if self.x2 != None else False
        self.y1 = y_start
        self.y2 = y_start + row_height if y_start != image_height else None
        self.yvalid = True if self.y2 != None else False
        self.valid = True if self.yvalid == True and self.xvalid == True else False
        self.rect = (self.x1, self.y1, self.x2, self.y2)
        self.parent = Image.open(parent_image)
        if self.valid:
            self.image = self.parent.crop(self.rect)

    def xcoordinates(self):
        return self.x1, self.x2
    
    def ycoordinates(self):
        return self.y1, self.y2
    
    def rectangle(self):
        return self.x1, self.x2, self.y1, self.y2
    
    def show(self, parent_image: str):
        #left, upper, right, lower
        self.image.show()
    
    def save(self, filepath: str):
        self.image.save(filepath)
        print(f'image saved as {filepath}')


class PixelImage:
    def __init__(self, filepath: str, rows: int, columns, verbose=True):
        self.filepath = filepath
        self.filename = self.filepath.split('/')[-1]
        self.file_extension = self.filename.split('.')[-1]
        self.number_of_rows = rows
        self.number_of_columns = columns
        self.image = Image.open(self.filepath)
        self.width = self.image.width
        self.height = self.image.height
        self.row_height = round(self.height/self.number_of_rows)
        self.column_width = round(self.width/self.number_of_columns)
        self.row_starts = []
        self.row_ends = []
        self.column_starts = []
        self.column_ends = []
        for i in range(0, self.number_of_rows):
            self.row_starts.append(i*self.row_height)
        for x in self.row_starts:
            self.row_ends.append(x+self.row_height)
        for i in range(0, self.number_of_columns):
            self.column_starts.append(i*self.column_width)
        for x in self.column_starts:
            self.column_ends.append(x+self.column_width)
        if verbose:
            self.__verbose()
        self.subimages = []
        self.sub_images_map = {}
        self.total_subimages = self.number_of_rows * self.number_of_columns
        image_count = 0
        for i in range(0, len(self.row_ends)):
            for index, x in enumerate(self.column_starts):
                x_start = x
                y_start = self.row_ends[i]
                subimage = SubImage(x_start=x_start, y_start=y_start, column_width=self.column_width, row_height=self.row_height, image_height=self.height, image_width=self.width, parent_image=self.filepath)
                if subimage.valid == True:
                    subimagename = f'{i}{index}'
                    self.sub_images_map[subimagename] = subimage
                    self.subimages.append(subimage)
                    print(f'\tSub-Image Cropped: {subimagename} {image_count}/{self.total_subimages}')
                    image_count+=1
        self.row_names =  {}
        self.folder_name = None

    def __verbose(self):
        print(f"""
        Image Name:       {self.filepath}
        Image Height:     {self.height}
        Image Width:      {self.width}

        Sub Image Columns:{self.number_of_columns}
        Sub Image Rows:   {self.number_of_rows}
        Sub Image Width:  {self.column_width}
        Sub image Height: {self.row_height} """)
    
    def subImages(self):
        for x in self.subimages:
            x.show(self.filepath)
    
    def getFolderName(self):
        fname = input("Enter a Folder Name for the images: ")
        self.folder_name = fname
        os.mkdir(f'{os.getcwd()}/{self.folder_name}')
    
    def getRowDimensions(self, index: int):
        xstart = 0
        ystart = index*self.row_height + self.row_height

        sub = SubImage(
            x_start=xstart, 
            y_start=ystart, 
            column_width=self.width-1, 
            row_height=self.row_height, 
            image_height=self.height, 
            image_width=self.width, 
            parent_image=self.filepath
            )
        return sub.rect

    def getRowImage(self, index: int):
        rect = self.getRowDimensions(index)
        srow = self.image.crop(rect)
        return srow

    def NameRow(self, row_number: int):
        if self.folder_name == None:
            self.getFolderName()
        start = self.number_of_columns * row_number
        end = start + self.number_of_columns
        try:
            choices = self.subimages[start:end]
        except:
            print('not a valid choice')
            return
        rect = self.getRowDimensions(row_number)
        srow = self.image.crop(rect)
        srow.show()
        row_name = input("Give a name for this Row of Character: ")
        srow.close()
        self.row_names[f'{row_name}'] = choices
        path = f'{os.getcwd()}/{self.folder_name}/{row_name}'
        os.mkdir(path)
        os.sync()
        for index, x in enumerate(choices):
            x.save(f'{path}/{index}.{self.file_extension}')
            print(f'[SAVED]  {path}/{index}.{self.file_extension}')

def main():
    app = ConsoleApplication()
    image = PixelImage(app.user_input[0], app.user_input[2], app.user_input[1])
    image.getFolderName()
    for ri in range(0, image.number_of_rows-1):
        image.NameRow(ri)

if __name__ == '__main__':
    main()
