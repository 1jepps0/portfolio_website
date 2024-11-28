To get the secret matrix (matB) we need to send the server an identity matrix. An identity matrix is a matrix that when used to multiply by another matrix, results in the second matrix. Since the server is performing matrix multiplication, this will give us matB.

![](media/writeup_images/Screenshot_1.png)

In order to get a matrix in the ".pt" format we can use the pytorch library

```python
import torch

identity_matrix 4x4 = torch.eye(4)
torch.save(identity_matrix_4x4, "identity_matrix_4x4.pt")
```
Creates a 4x4 identity matrix and saves it to a file.

```python
import torch
import requests

identity_matrix_4x4 = torch.eye(4)
torch.save(identity_matrix_4x4, "identity_matrix_4x4.pt")

url = "https://ictf24-under-distributed-training.chals.io/upload"

with open("identity_matrix_4x4.pt", "rb") as file:
    files = {"file": file}
    response = requests.post(url, files=files)
    print(response.text)
```
Sends it to the /upload endpoint. We get matB back:
```
Response Text: {"result":"[[25449.0, 26228.0, 25211.0, 25652.0], [25695.0, 13619.0, 29235.0, 13361.0], [24428.0, 12656.0 27491.0, 13164.0], [12383.0, 18253.0, 30815.0, 32120.0]]"}
```

We are given the script that was used to encode the flag into a matrix so we can use that to reverse it.

```python
def flag_to_matrix(flag: str) -> torch.Tensor:
    # Convert the flag to a matrix of integers
    assert len(flag) == 32
    # two characters per integer
    mat = torch.tensor(
        [ord(flag[i]) + (ord(flag[i + 1]) << 8) for i in range(0, len(flag), 2)],
        dtype=torch.float,
    )
    mat = mat.view(MATRIX_SIZE)

    return mat
```
This is the function that they used to transform their flag into a matrix. It packs each character into a single integer by having the first character occupy the lower byte, while the second character occupies the upper byte. Since this is only using bit shifting, this is easily reversible.

```python
def matrix_to_flag(matrix):
    flat_matrix = matrix.view(-1).int().tolist()  
    
    flag_chars = ""
    for num in flat_matrix:
        char1 = chr(num & 0xFF)  
        char2 = chr(num >> 8)   
        flag_chars += char1 + char2

    return flag_chars
```
To reverse this we can use the and operation against 0xFF (255) which will isolate the rightmost bits, giving us the first letter. For the second letter we can reverse the left bit shift with a right one. We can do this process for each number, giving us the flag.

```
ictf{b4d_d353r14l_p1ckl3_0MG_xx}
```