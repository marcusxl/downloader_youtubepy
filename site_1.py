from flask import Flask, jsonify, render_template, request, make_response, send_from_directory, send_file
from pytube import YouTube
import os

app = Flask(__name__, template_folder='templates')

def allowed_url(url):
    return url and isinstance(url, str) and url.startswith('https://')

def dowloader_video(video_url):
    try: 
        youtube_url = YouTube(video_url)
        video_title = youtube_url.title
        stream = youtube_url.streams.filter(file_extension='mp4', progressive=True).first()

        downloader_folder = 'downloads'
        if not os.path.exists(downloader_folder):
            os.makedirs(downloader_folder)
        
        file_path = os.path.join(downloader_folder, f'{video_title}.mp4')
        stream.download(output_path=downloader_folder, filename=f'{video_title}.mp4'
                        )
        return True, file_path, video_title
    
    except Exception as e:
        print(f'Erro ao baixar video: {e}')
        return False, None, None
    
@app.route('/')
def hello():
    return render_template('pagina_web.html')

@app.route('/download', methods=['POST'])
def download():
    if request.method ==  'POST':
        video_url = request.form['video_url']

    if allowed_url(video_url):
        success, file_path, video_title = dowloader_video(video_url)
        
        if success:
            return send_file(file_path, as_attachment=True, download_name=f'{video_title}.mp4')
        
        else:
            return render_template('erro_download.html', error_message='Erro ao baixar video verifique a URL')
        
    else:
        return render_template('erro_download.html', 
                error_message="URL não permitida")

if __name__ == '__main__':
    app.run(debug=True)