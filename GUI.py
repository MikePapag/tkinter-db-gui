import tkinter as tk
from tkinter import ttk, messagebox
import requests
#initialize window
root = tk.Tk()
root.title('Testing GUI handling a DB')
root.minsize(900,600)
#options of table and methods that can be used
options_table = ['boats', 'boats_2', 'boats_3']
options_method = ['PUT', 'POST', 'GET', 'DELETE']
#creating labels,entries and dropdown menus
api_label = tk.Label(root, text="Enter your API key: ")
api_label.pack(pady=10)

api_entry = tk.Entry(root, show='*')
api_entry.pack()

table_label = tk.Label(root, text='Select a table: ')
#dropdown menu
table_selected = tk.StringVar()
table_dropdown = ttk.Combobox(root, textvariable=table_selected, state='readonly')
table_dropdown['values'] = options_table
table_dropdown.current(0)
table_dropdown.config(state='disabled') #have the menu disabled until the api key is inputted

method_label = tk.Label(root, text='What method do you want to use: ')
#dropdown menu
method_selected = tk.StringVar()
method_dropdown = ttk.Combobox(root, textvariable=method_selected, state='readonly')
method_dropdown['values'] = options_method
method_dropdown.current(0)
method_dropdown.config(state='disabled')#have the menu disabled until the api key is inputted

id_label = tk.Label(root, text='id: ')
id_entry = tk.Entry(root)

name_label = tk.Label(root, text='Name: ')
name_entry = tk.Entry(root)

latitude_label = tk.Label(root, text='latitude: ')
latitude_entry = tk.Entry(root)

longitude_label = tk.Label(root, text='longitude: ')
longitude_entry = tk.Entry(root)

moving_label = tk.Label(root, text='moving: ')
moving_entry = tk.Entry(root)

role_label = tk.Label(root, text="")
role_label.pack()
#creating a function to hide or show the API KEY
def toggle_key_visibility():
    if api_entry.cget('show') == '*':
        api_entry.config(show = '')
        toggle_button.config(text="Hide key")#changing the text on the button depending on "show"
    else:
        api_entry.config(show='*')
        toggle_button.config(text='Show key')#changing the text on the button depending on "show"
#creating a function for API KEY validation
def verify_api_key():
    key = api_entry.get()
    try:
        #request access with the key we inserted
        response = requests.get('http://127.0.0.1:5000/verify-key', headers={"x-api-key": key})
        #if the key is accepted
        if response.status_code == 200:
            role = response.json().get('role',"")
            table_dropdown.config(state='readonly')
            method_dropdown.config(state='readonly')
            #if the API KEY is a user limit access
            if role == "user":
                #remove api key labels,entries and buttons
                api_label.pack_forget()
                api_entry.pack_forget()
                toggle_button.pack_forget()
                check_key_button.pack_forget()
                #show table and method labels, entries and menus
                table_label.pack()
                table_dropdown.pack()
                method_label.pack()
                method_dropdown.pack()
                method_dropdown["values"] = ['POST','GET']
                method_dropdown.current(1)
                messagebox.showinfo("Access","User access: POST GET only.")
            #if the API KEY is an admin give full access
            elif role == "admin":
                #remove api key labels,entries and buttons
                api_label.pack_forget()
                api_entry.pack_forget()
                toggle_button.pack_forget()
                check_key_button.pack_forget()
                #show table and method labels, entries and menus
                table_label.pack()
                table_dropdown.pack()
                method_label.pack()
                method_dropdown.pack()
                method_dropdown["values"] = ['POST', 'GET', 'DELETE', 'PUT']
                method_dropdown.current(0)
                messagebox.showinfo('Access',"Admin access: Full access granted")
            role_label.config(text=f'Logged in as: {role.upper()}')
        else:
            messagebox.showerror('Access Denied',response.json().get('error','Invalid Key'))
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Request Failed", f'Error: {e}')

def on_method_change(event):
    selected_method = method_selected.get()
    #deletes previous entries after changing method
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    latitude_entry.delete(0, tk.END)
    longitude_entry.delete(0, tk.END)
    moving_entry.delete(0, tk.END)
    #hides label and entry until method is selected
    if selected_method == '':
        id_label.pack_forget()
        id_entry.pack_forget()
    #shows labels and entries after the method is selected and depending on method
    elif selected_method == 'PUT' or selected_method == 'POST':
        id_label.pack(pady=(20, 0))
        id_entry.pack()
        name_label.pack(pady=(20, 0))
        name_entry.pack()
        latitude_label.pack(pady=(20, 0))
        latitude_entry.pack()
        longitude_label.pack(pady=(20, 0))
        longitude_entry.pack()
        moving_label.pack(pady=(20, 0))
        moving_entry.pack()
    #shows labels and entries after the method is selected and depending on method
    else:
        id_label.pack(pady=(20, 0))
        id_entry.pack()
        name_label.pack_forget()
        name_entry.pack_forget()
        latitude_label.pack_forget()
        latitude_entry.pack_forget()
        longitude_label.pack_forget()
        longitude_entry.pack_forget()
        moving_label.pack_forget()
        moving_entry.pack_forget()
method_dropdown.bind("<<ComboboxSelected>>", on_method_change)

def submit_to_backend():
    table = table_selected.get()
    method = method_selected.get()
    id_value = id_entry.get()
    name = name_entry.get()
    latitude = latitude_entry.get()
    longitude = longitude_entry.get()
    moving = moving_entry.get()
    id = id_entry.get()
    api_key = api_entry.get()
    headers = {"x-api-key":api_key}

    try:
        if method == "DELETE":
            if not id_value:
                messagebox.showerror("Input Error", "Please enter an ID to delete.")
                return

            url = f"http://127.0.0.1:5000/{table}/{id_value}"
            response = requests.delete(url, headers=headers)

            if response.status_code == 200:
                messagebox.showinfo("Success", response.json().get("message", "Deleted successfully."))
            else:
                messagebox.showerror("Error: ", response.json().get("error ","Unknown error"))
            return
        
        if method == "POST":
            if not latitude or not longitude:
                messagebox.showerror('Input Error','Latitude and Longitude cannot be empty.')
                return
            try:
                lat = float(latitude)
                lon = float(longitude)
            except ValueError:
                messagebox.showerror('Input Error',"Latitude and Longitude must be valid numbers.")
                return
            data = {
                "id" : id,
                "name": name,
                "latitude": lat,
                "longitude": lon,
                "moving": moving.lower() in ['true', '1', 'yes']
            }
            url = f"http://127.0.0.1:5000/{table}"
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 201:
                messagebox.showinfo("Success: ", response.json().get("message","Added successfully."))
            else:
                messagebox.showerror("Error: ", response.json().get("error ","Unknown error"))
            return
      
        if method == "PUT":
            url = f"http://127.0.0.1:5000/{table}/{id_value}"
            data2 = {}
            if name:
                data2["name"] = name
            if latitude:
                data2["latitude"] = latitude
            if longitude:
                data2["longitude"] = longitude
            if moving:
                data2["moving"] = moving
            if not data2:
                messagebox.showerror("Input Error","Please fill at least one field")
                return
            response = requests.put(url, json=data2, headers=headers)
            if response.status_code == 200:
                messagebox.showinfo("Success", response.json().get("message","Updated successfully."))
            else:
                messagebox.showerror("Error",response.json().get("Error","Unknown error"))
            return
        
        if method == "GET":
            url = f"http://127.0.0.1:5000/{table}"
            if id_value:
                url += f"/{id_value}"
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        data = response.json()
                    except ValueError:
                        messagebox.showerror("Error", "Invalid JSON response.")
                        return

                    if not data:
                        messagebox.showinfo("No Data", "No data found.")
                        return
                    if isinstance(data, list):
                        formatted = "\n\n".join(
                    [f"ID: {row.get('id')}\nName: {row.get('name')}\nLatitude: {row.get('latitude')}\nLongitude: {row.get('longitude')}\nMoving: {row.get('moving')}"
                        for row in data
                    ]
                    )
                    elif isinstance(data, dict):
                        formatted = (
                            f"ID: {data.get('id')}\nName: {data.get('name')}\n"
                            f"Latitude: {data.get('latitude')}\nLongitude: {data.get('longitude')}\nMoving: {data.get('moving')}"
                        )
                    else:
                        formatted = str(data)
                    messagebox.showinfo("Data retrieved", formatted)
                else:
                    try:
                        error_msg = response.json().get("error","Unknown error")
                    except ValueError:
                        error_msg = "Non-JSON error response"
                    messagebox.showerror("Error",error_msg)
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Request Failed",f"An error occured: {e}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Request Failed", f"An error occurred: {e}")
    except ValueError as e:
        messagebox.showerror("Input error", f"Invalid input {e}")

toggle_button = tk.Button(root, text='Show key', command=toggle_key_visibility)
toggle_button.pack()

check_key_button = tk.Button(root, text="Verify API Key", command=verify_api_key)
check_key_button.pack(pady=(5, 10))

submit_button = tk.Button(root, text='Submit', width=20, height=2, command=submit_to_backend)
submit_button.pack(side='bottom', padx=10, pady=10)

root.mainloop()
