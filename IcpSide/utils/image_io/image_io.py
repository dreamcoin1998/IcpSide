"""
处理图片文件的io流 基于腾讯云对象存储

Creator: Gao Junbin
Update: 2021-07-02
"""
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from IcpSide import config as cg
from datetime import datetime
import random


def upload_image(fp, mime='jpg'):
    secret_id = cg.TENCENT_SECRET_ID
    secret_key = cg.TENCENT_SECRET_KEY
    region = cg.TENCENT_REGION
    scheme = cg.TENCENT_SCHEME
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Scheme=scheme)
    client = CosS3Client(config)
    format_filename = str(int(datetime.timestamp(datetime.now()))) + str(random.randint(0000, 9999)) + f'.{mime}'
    response = client.put_object(
        Bucket='icpside-1258554384',
        Body=fp,
        Key=format_filename,
        StorageClass="STANDARD",
        EnableMD5=False
    )
    if response['ETag']:
        return cg.TENCENT_BASE_URL + format_filename
    return False
