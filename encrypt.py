import rsa
import time


start_time = time.time()

publicKey, privateKey = rsa.newkeys(4096)

print("Public key string: ", publicKey)
print("Secret key string: ", privateKey)


# the password will retrieved from the data base.
password = "openpgpwd"

encMessage = rsa.encrypt(password.encode(),	publicKey)

print("original password: ", password)
print("encrypted password: ", encMessage)

with open("cifrados.txt","rb") as outfile:
    outfile.write(str(encMessage))


'''
decMessage = rsa.decrypt(encMessage, privateKey).decode()

end_time = time.time()

running_time = end_time - start_time

print("decrypted password: ", decMessage)
print('Execution time:', running_time, 'seconds')

'''