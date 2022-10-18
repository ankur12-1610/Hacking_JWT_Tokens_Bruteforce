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
The scenario consits of a REST API running on a target machine and uses JWT-based authorization.
> **Note**: The signing key used for token generation is weak.
