"""Optional local-process Astra client. Default is dry run; never used by Pages."""
import argparse
import base64
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'book/notebooks'))
from astra_contract import build_request, validate_briefing


def extract_briefing(response):
    if response.get('status') != 'completed':
        raise ValueError('API response was not completed; no briefing accepted')
    texts = []
    for item in response.get('output', []):
        if item.get('type') != 'message':
            continue
        for content in item.get('content', []):
            if content.get('type') == 'refusal':
                raise ValueError('Model refused the request; no briefing accepted')
            if content.get('type') == 'output_text':
                texts.append(content['text'])
    if not texts:
        raise ValueError('No output_text in completed response')
    return json.loads(''.join(texts))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--image',type=Path,help='Optional authorized PNG/JPEG map; sent only with --live')
    parser.add_argument('--live',action='store_true',help='Send request to OpenAI; incurs API usage')
    args=parser.parse_args()
    if args.output.exists():
        raise ValueError('Output already exists; choose a new filename to preserve the audit trail')
    metadata_path=args.output.with_suffix(args.output.suffix+'.metadata.json')
    if args.live and metadata_path.exists():
        raise ValueError('Metadata output already exists; choose a new output filename')
    if args.input.stat().st_size > 250_000:
        raise ValueError('Evidence packet exceeds 250 KB aggregate-only limit')
    bundle=json.loads(args.input.read_text(encoding='utf-8'))
    image=None
    if args.image:
        if args.image.stat().st_size > 5_000_000:
            raise ValueError('Image exceeds 5 MB exercise limit')
        raw=args.image.read_bytes()
        mime='image/png' if raw.startswith(b'\x89PNG\r\n\x1a\n') else 'image/jpeg' if raw.startswith(b'\xff\xd8\xff') else None
        if mime is None:
            raise ValueError('Only PNG/JPEG images are accepted')
        image='data:'+mime+';base64,'+base64.b64encode(raw).decode()
    request=build_request(bundle,image)
    if args.live:
        key=os.environ.get('OPENAI_API_KEY')
        if not key:
            raise ValueError('Set OPENAI_API_KEY in this local process; never put it in a notebook')
        req=urllib.request.Request('https://api.openai.com/v1/responses',data=json.dumps(request).encode(),
                                   headers={'Content-Type':'application/json','Authorization':'Bearer '+key},method='POST')
        try:
            with urllib.request.urlopen(req,timeout=180) as result:
                response=json.load(result)
        except urllib.error.HTTPError as error:
            raise ValueError(f'OpenAI HTTP {error.code}; check model access, quota and request. No output accepted.') from None
        output=validate_briefing(extract_briefing(response),bundle)
        # Keep request identity and usage separately without storing credentials or the image.
        meta={'response_id':response.get('id'),'model':response.get('model'),'usage':response.get('usage'),
              'synthetic':True,'review_status':'NOT REVIEWED'}
        metadata_path.write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    else:
        output=request
    args.output.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(('Live response validated; human claim review still required: ' if args.live else 'Dry run; no API call: ')+str(args.output))


if __name__=='__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        raise SystemExit(str(error))
