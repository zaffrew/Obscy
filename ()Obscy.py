import Tkinter as tk
import  tkFileDialog, os
from PIL import Image, ImageTk
import zipfile

grey = '#212121'
red = '#FF5252'
cream = '#FFE57F'
white = '#FFFFFF'
light_green = '#B9F6CA'

logo_font = ('consolas bold', 54)
title_font = ('segoe ui', 24)
sub_font = ('segoe ui semibold', 12)
button_font = ('consolas bold', 12)

class app:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title('Obscy')
        self.root.config(background = grey)

    def create_widgets(self):

        self.frame1 = tk.Frame(self.root)

        hline1 = tk.Label(self.root, text = '____________________________________________________________________________', fg = white, bg = grey, font = button_font, pady = 5, padx = 5)
        hline2 = tk.Label(self.root, text = '____________________________________________________________________________', fg = white, bg = grey, font = button_font, pady = 5, padx = 5)
        
        

        title = tk.Label(self.root, text = 'Obscy.', fg = white, bg = grey, font = logo_font, padx = 64, pady = 200)
    
     
        
        
        self.upload_button = tk.Button(self.frame1, text = 'UPLOAD', bg = grey, fg = white, relief = 'ridge', font = button_font, padx = 84, pady = 2, command = self.upload_on_click)

        self.decode_button = tk.Button(self.frame1, text = 'DECODE', bg = grey, fg = white, relief = 'ridge', font = button_font, padx = 84, pady = 2, command = self.decode_on_click)

        self.frame1.config(background = grey, padx = 10, pady = 10)

        hline1.grid(row = 0, column = 0)
        title.grid(row = 1, column = 0, columnspan = 2)
        hline2.grid(row = 2, column = 0)

        
        self.frame1.grid(row = 3, column = 0, columnspan = 2)
        self.upload_button.grid(row = 4, column = 0)
        self.decode_button.grid(row = 5, column = 0)
        

        self.root.mainloop()

    def upload_on_click(self):

        explorer = tk.Tk()
        self.src_path = str(tkFileDialog.askopenfilename())
        explorer.destroy()

        self.change_frame()

    def change_frame(self):

        load_image = Image.open(self.src_path)
        width, height = load_image.size
        ratio = float(width)/height
        
        if width > height:
            width = 450
            height = int(width/ratio)
            
        elif height > width:
            height = 450
            width = int(height * ratio)
            
        else:
            height = 400
            width = 400
            
        load_image = load_image.resize((width, height), Image.ANTIALIAS)
        render_image = ImageTk.PhotoImage(load_image)

        image_label = tk.Label(self.root, image = render_image)
        image_label.img = render_image

        self.frame2 = tk.Frame(self.frame1)
        self.frame2.config(background = grey, pady = 5, padx = 40)

        self.var1 = tk.StringVar(self.frame2)

        self.msg_label = tk.Label(self.frame2, text = 'Enter type of message ', bg = grey, fg = white, font = sub_font, padx = 10)
        self.options = tk.OptionMenu(self.frame2, self.var1, 'Text', 'Image/Document', command = self.chosen)
        self.options.config(relief='flat', bg=grey, fg=white, font=sub_font, activeforeground=white, activebackground='black', width=1, padx=5, pady=5, highlightthickness=0)
        self.options['menu'].config(bg=grey, fg=white, font=sub_font, activeforeground=white, activebackground='black')

        self.upload_button.destroy()
        self.decode_button.destroy()
        image_label.grid(row = 1, column = 0, columnspan = 2)

        self.frame2.grid(row = 3, column = 0, rowspan = 2)

        self.msg_label.grid(row = 4, column = 0)
        self.options.grid(row = 4, column = 1)

    def chosen(self, choice):

        if choice == 'Text':
            self.text_frame()

        elif choice == 'Image/Document':
            self.doc_frame()

    def text_frame(self):
        
        self.var2 = tk.StringVar(self.frame2)
        self.message_entry = tk.Entry(self.frame2, textvariable = self.var2, bg = grey, fg = white, font = sub_font, highlightthickness = 2)
        self.enter_button1 = tk.Button(self.frame2, text = 'ENTER', relief = 'ridge', bg = grey, fg = white, padx = 25, font = button_font, command = self.hide_text)

        self.msg_label.destroy()
        self.options.destroy()
        self.decode_button.destroy()
        self.message_entry.grid(row = 4, column = 0)
        self.enter_button1.grid(row = 4, column = 1)
        

    def doc_frame(self):

        # add this
##        self.add_this_button = tk.Button(self.frame2, text = 'ADD THIS', relief = 'ridge', bg = grey, fg = white, padx = 25, font = button_font, command = self.get_source)
        
        # to this
        self.add_this_button = tk.Button(self.frame2, text = 'ADD THIS', relief = 'ridge', bg = grey, fg = white, padx = 25, font = button_font, command = self.get_source)

        self.msg_label.destroy()
        self.options.destroy()
        self.decode_button.destroy()
##        self.add_this_button.grid(row = 4, column = 0)
        self.add_this_button.grid(row = 4, column = 0)
        
    def get_source(self):

        explorer = tk.Tk()
        add = str(tkFileDialog.askopenfilename())
        explorer.destroy()
        self.hide_doc(add, self.src_path)
        
        
        

    def hide_text(self):
        '''
        modifying the red part of each pixel to hide message
        '''

        source_img = Image.open(self.src_path)
        print source_img, source_img.mode
        new_img = 'new.png'
        copy = source_img.copy() # duplicate of image
        msg = self.var2.get()
        width, height = source_img.size
        count = 0
        for row in range(height):
            for column in range(width):
                try:
                    
                    red, green, blue = source_img.getpixel((column, row))
            
                except:

                    red, green, blue, alpha = source_img.getpixel((column, row)) # for png

                
                if row == 0 and column == 0 and count < len(msg):
                    dat = len(msg) # useful when decoding      
                    # if we are at first pixel
                    # add length of message as red

                elif count <= len(msg):
                    char = msg[count - 1]
                    # get the character
                    dat = ord(char)
                    
                    # get corresponding ascii value
                else:
                    # if complete message has been added
                    # add default red

                    dat = red
                
                # add the new pixel data to the duplicate of image
                copy.putpixel((column, row), (dat, green, blue))
                count += 1

        

        copy.save(new_img)
        done = tk.Label(self.frame2, text = 'Done', fg = light_green, bg = grey, font = sub_font)
        done.grid(row = 5, column = 0)
        
        print 'DONE'


    def show_text(self, path):

        image = Image.open(path)
        width, height = image.size
        count = 0
        message = ''

        for row in range(height):
            for column in range(width):
                try:
                    red, green, blue = image.getpixel((column, row))
                except:
                    red, green, blue, alpha = image.getpixel((column, row))

                if row == 0 and column == 0:
                    length = red # get length of image from first pixel

                elif count <= length:
                    message += chr(red)

                count += 1

        print message

        f = open('decoded.txt', 'w')
        f.write(message)
        f.close()
                
    def hide_doc(self, src, newimg):
        '''
        Appending information into a an image as binary file. The appended information cannot be accessed by looking into the image.
        '''
        
        
        dst = 'temp.zip' # zip file that will contain all the information that has to be hidden
        z = zipfile.ZipFile(dst, "w")
        z.write(src) # write the information into the zip file
        z.close()
        os.remove(src) # cut and paste instead of copy and paste. original file is deleted.
        with open(newimg, "ab") as image: # open the destination image
            with open(dst, "rb") as archive: # open the zip file
                image.write("\n" + archive.read()) # save contents of zip file into the image.
        os.remove(dst)

    def show_doc(self, unhide_file):
        Zip = zipfile.ZipFile(unhide_file)
        Zip.extractall('message')


    def decode_on_click(self):
        
        explorer = tk.Tk()
        path = str(tkFileDialog.askopenfilename())
        explorer.destroy()

        try:
            self.show_doc(path)

        except:
            self.show_text(path)
        
        

a = app()
a.create_widgets()
