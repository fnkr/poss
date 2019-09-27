import requests
requests.packages.urllib3.disable_warnings()

try:
    from config import POSS_API_URL as API_URL
except Exception:
    API_URL = None

try:
    from config import POSS_API_KEY as API_KEY
except Exception:
    API_KEY = None

OUTPUT = ''


def __out(output, OUTPUT=OUTPUT):
    OUTPUT += output
    if args.clipboard:
        import pyperclip
        pyperclip.copy(OUTPUT)

    print(output)


def upload(files, API_URL=API_URL, API_KEY=API_KEY, randomize_filename=False):
    if not API_URL or not API_KEY:
        raise Exception('API_URL and/or API_KEY is not configured')

    url = '%s/upload?apikey=%s' % (API_URL, API_KEY)
    files = [('files[]', file) for file in files]

    options = {}

    if randomize_filename:
        options['randomize_filename'] = True

    try:
        request = requests.post(url,
                                files=files,
                                data=options,
                                allow_redirects=False,
                                verify=False)
    except Exception:
        raise Exception('could not connect to server')

    if request.status_code == 404:
        raise Exception('invalid api url')

    elif request.status_code == 302:
        raise Exception('invalid api key')

    try:
        request = request.json()
    except:
        raise Exception('invalid response from server')

    files = []

    for file in request:
        if file['error']:
            files.append(Exception('upload failed'))
        else:
            files.append(file)

    return request


if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser(description='POSS Client')

    task_parser = parser.add_mutually_exclusive_group(required=True)
    task_parser.add_argument('--upload',
                             metavar='file',
                             type=str,
                             nargs='+',
                             help='upload files')

    parser.add_argument('--randomize-filename',
                        action='store_true',
                        help='randomize filenames')

    parser.add_argument('--clipboard',
                        action='store_true',
                        help='copy result to clipboard')

    args = parser.parse_args()

    if not args.upload and args.randomize_filename:
        parser.error("--randomize_filename requires --upload.")

    if args.upload:
        files = []
        for file in args.upload:
            if os.path.isfile(file):
                files.append([
                    os.path.basename(file),
                    open(file, 'rb'),
                    'application/octet-stream'
                ])
            else:
                if os.path.isdir(file):
                    parser.error('uploading directorys is currently not supported')
                else:
                    parser.error('file not found: %s' % file)

        try:
            upload = upload(files, randomize_filename=args.randomize_filename)
        except Exception as e:
            __out(str(e))
        else:
            output = ''
            for file in upload:
                try:
                    __out(file['link'])
                except Exception:
                    __out(str(file))
