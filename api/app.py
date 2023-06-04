from flask import Flask,render_template, request
import os, matplotlib
import Logo

app = Flask(__name__)
SAVE_PATH = "/tmp"
sequences = []
sequences_file = None
image_format = ''

@app.route('/')
def webSite():
    return render_template('index.html')

@app.route('/generate_logo', methods=['GET', 'POST'])
def generate_logo():
    if request.method == 'POST':
        # delete old file (no need in vercel)
        # for filename in os.listdir(SAVE_PATH): 
        #     file_path = os.path.join(SAVE_PATH, filename)
        #     os.remove(file_path)

        # get input from form
        global sequences, sequences_file, image_format
        sequences_input = request.form['sequences-input']
        sequences = sequences_input.split('\r\n')
        sequences_file = request.files['sequences-file']
        image_format = request.form['image-format']
        print(sequences, sequences_file, image_format)

        # save sequences file
        if sequences_file:
            # save new file
            file_path = os.path.join(SAVE_PATH, 'sequences.txt')
            sequences_file.save(file_path)

            # read sequences file
            with open(file_path, 'r') as file:
                sequences_input = file.read()
                sequences = sequences_input.split('\n')

        # generate logo
        matplotlib.use('agg') # 因為在 flask 中使用，所以要加這行
        Logo.visualize_sequence_logo(sequences, SAVE_PATH, image_format)

        sequence_length = max([len(sequence) for sequence in sequences])
        print(sequences_input)
        return render_template('logo.html', logo_img = 'static/files/logo.' + image_format, sequence_number = len(sequences), sequence_length = sequence_length, sequences_input = str(sequences_input))
    else:
        return render_template('index.html')

def getInputData():
    global sequences, image_format
    return sequences, image_format

if __name__ == '__main__':
    app.run()