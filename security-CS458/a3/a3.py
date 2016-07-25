#!/usr/bin/env python

import requests
import base64

URL = 'http://localhost:4555'


def test(cookie):
	encode = base64.b64encode(cookie)

	print encode
	r = requests.get(URL, cookies={'user': encode})

	return r.status_code != 500

def getPlain(padLen, i):	
	if i == 0:
		return padLen

	return i

def printBytes(title, data):	
	print title, ''.join('{:02x}'.format(x) for x in data)

def decryptByte(cookie):
	original = cookie[:16]
	iv = bytearray(16) #this will be backwards

	# printBytes("Initial cookie", cookie)

	for place in range(16):
		print "START:", place
		prefix = bytearray(16) #this will be backwards

		# printBytes("iv", iv)
		for i in range(place):
			# print place, i, getPlain(place, i)
			prefix[15-i] = iv[15-i] ^ getPlain(place, i)


		# printBytes("prefix", prefix)

		for i in range(256):
			prefix[15-place] = i

			if(test(prefix + cookie)):
				print "chosen val", i
				break

		iv[15-place] = prefix[15-place] ^ getPlain(place, place)


	plaintext = [0] * 16
	for i in range(16):
		plaintext[i] = iv[i] ^ cookie[i]

	return plaintext





def main():
	dummy = "k0UtzN9gwc1qfe2CMYn3rESGL6mJwyG8Z+ztkAJJBVM="
	cookie =  base64.b64decode(dummy)

	plaintext = decryptByte(cookie)
	print (bytearray(plaintext))

if __name__ == '__main__':
    main()