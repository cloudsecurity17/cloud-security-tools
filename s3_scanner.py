import boto3

def check_s3_buckets():
    # AWS S3 mijozini ishga tushirish
    s3 = boto3.client('s3')
    
    # Barcha bucketlarni ro'yxatini olish
    response = s3.list_buckets()
    
    print("S3 Bucket xavfsizlik tekshiruvi:")
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        try:
            # Bucketning ACL (Access Control List) sozlamalarini olish
            acl = s3.get_bucket_acl(Bucket=bucket_name)
            
            # Har bir grantni tekshirish
            for grant in acl['Grants']:
                grantee = grant.get('Grantee', {})
                uri = grantee.get('URI', '')
                
                # Agar "AllUsers" yoki "AuthenticatedUsers" bo'lsa, bu xavfli bo'lishi mumkin
                if 'AllUsers' in uri or 'AuthenticatedUsers' in uri:
                    print(f"[XAVF!] Bucket '{bucket_name}' ochiq (Public): {uri}")
                else:
                    print(f"[OK] Bucket '{bucket_name}' xavfsiz.")
                    
        except Exception as e:
            print(f"Xatolik yuz berdi {bucket_name}: {e}")

if __name__ == "__main__":
    check_s3_buckets()
  
