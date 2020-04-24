# Thank you, Tom Chapin and stackoverflow
# https://stackoverflow.com/questions/34468319/reading-the-data-written-to-s3-by-amazon-kinesis-firehose-stream
import json
from json.decoder import JSONDecodeError

decoder = json.JSONDecoder()

with open('giant_kinesis_s3_text_file_with_concatenated_json_blobs.txt', 'r') as content_file:

    content = content_file.read()

    content_length = len(content)
    decode_index = 0

    while decode_index < content_length:
        try:
            obj, decode_index = decoder.raw_decode(content, decode_index)
            print("File index:", decode_index)
            print(obj)
        except JSONDecodeError as e:
            print("JSONDecodeError:", e)
            # Scan forward and keep trying to decode
            decode_index += 1