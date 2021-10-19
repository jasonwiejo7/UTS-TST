from fastapi import FastAPI, HTTPException, Depends
from Auth.Auth_handler import signJWT, get_password_hash, verify_password
from Auth.Auth_bearer import JWTBearer
import json

with open("menu.json", "r") as readFile:
    daftarMenu = json.load(readFile)

with open("account.json", "r") as readUser:
    daftarUser = json.load(readUser)

app = FastAPI()

@app.post("/user/sign-up")
async def register(username: str, password: str):
    hashpassword = get_password_hash(password)
    newuser = {'username': username, 'password': hashpassword}
    daftarUser['user'].append(newuser)
    with open("account.json", "w") as writeUser:
        json.dump(daftarUser, writeUser, indent = 4)
    writeUser.close()
    return ({'Message' : "User berhasil di-tambahkan."})

@app.post("/user/login")
async def login(username: str, password: str):
    for list_user in daftarUser['user']:
        if list_user['username'] == username:
            if verify_password(password, list_user['password']):
                return signJWT(username)
            else:
                return ({'Message' : "Password yang dimasukkan salah."})
    return ({'Message' : "User tidak ditemukan."})

@app.get('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def read_menu(item_id: int):
    for menu_list in daftarMenu['menu']:
        if menu_list['id'] == item_id:
            return menu_list
    raise HTTPException(
        status_code = 404, detail =f'Item not Found'
    )

@app.post('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def add_menu(name: str):
    item_id = len(daftarMenu['menu'])+1
    new_menu = {'id': item_id, 'name': name}
    if (item_id > 0):
        daftarMenu['menu'].append(new_menu)
        with open("menu.json", "w") as writeFile:
            json.dump(daftarMenu, writeFile, indent = 4)
        writeFile.close()
        return ({'Message' : "Menu berhasil di-tambahkan."})
    raise HTTPException(
        status_code = 505, detail =f'Failed to add menu'
    )

@app.put('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def update_menu(item_id: int, new_name: str):
    for menu_list in daftarMenu['menu']:
        if menu_list['id'] == item_id:
            menu_list['name'] = new_name
            readFile.close()
            with open("menu.json", "w") as writeFile:
                json.dump(daftarMenu, writeFile, indent = 4)
            writeFile.close()
            return ({'Message' : "Menu berhasil di-update."})
    raise HTTPException(
        status_code = 404, detail =f'Item not Found'
    )

@app.delete('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def delete_menu(item_id: int):
    for menu_list in daftarMenu['menu']:
        if menu_list['id'] == item_id:
            daftarMenu['menu'].remove(menu_list)
            readFile.close()
            with open("menu.json", "w") as writeFile:
                json.dump(daftarMenu, writeFile, indent = 4)
            writeFile.close()
            return ({'Message' : "Menu berhasil di-hapus."})
    raise HTTPException(
        status_code = 404, detail =f'Item not Found'
    )