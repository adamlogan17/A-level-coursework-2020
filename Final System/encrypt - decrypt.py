def encrypt(data):
    '''This will encrypt the data. 'data' needs to be a string'''
    key=2478
    encrypted_data=""
    for i in data:
        i=ord(i)
        unicode_value=i+key
        encrypted_data=chr(unicode_value)+encrypted_data
    return encrypted_data

def decrypt(data):
    '''This decrypts the data'''
    key=2478
    encrypted_data=""
    for i in data:
        i=ord(i)
        unicode_value=i-key
        encrypted_data= chr(unicode_value)+encrypted_data
    return encrypted_data


if __name__=='__main__':
    print(decrypt("৏য়ਢਡਗਜਝਗਢਞਓ਑ਓ਀"))



