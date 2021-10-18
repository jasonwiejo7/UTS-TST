from fastapi import FastAPI, HTTPException
import json

with open("menu.json", "r") as readFile:
    daftarMenu = json.load(readFile)

app = FastAPI()

@app.get('/menu/{item_id}')
async def read_menu(item_id: int):
    for menu_list in daftarMenu['menu']:
        if menu_list['id'] == item_id:
            return menu_list
    raise HTTPException(
        status_code = 404, detail =f'Item not Found'
    )

@app.post('/menu/{item_id}')
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

@app.put('/menu/{item_id}')
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

@app.delete('/menu/{item_id}')
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
