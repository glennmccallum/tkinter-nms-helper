from tkinter import *
from tkinter import ttk
import pandas as pd
import os

# Keep filtering listbox when user enters characters in textbox
def on_keyrelease(event):

    # Get value from Entrybox
    value = event.widget.get()
    # Strip whitespaces and convert to lower case
    value = value.strip().lower()

    # If nothing entered display all hostnames
    if value == '':
        data = hostnames
    # else serach hostnames and display any that match string
    else:
        data = []
        for item in hostnames:
            if value in item.lower():
                data.append(item)                

    # Update hostanmes in listbox
    listbox_update(data)

# Used to populate the listbox from data entered
def listbox_update(data):
    # delete previous data
    listbox.delete(0, 'end')

    # sorting data 
    data = sorted(data, key=str.lower)

    # put new data
    for item in data:
        listbox.insert('end', item)

# For debugging purposes to show active seclection in terminal
def on_select(event):
    # display element selected on list
    print('(event) previous:', event.widget.get('active'))
    print('(event)  current:', event.widget.get(event.widget.curselection()))
    print('---')
    infoDevice()

# Get IP of selection from CSV file
def getSelection():
    # Get Current Selection
    selected = listbox.curselection()
    # Get the value of selection
    for item in selected:
        host = listbox.get(item)
    # From selected hostname get the IP from CSV file
    ip = devices.loc[devices['Hostname'] == host, 'IP'].item()

    #return the IP of selected device
    return ip

# Used for clear search button to clear all fields
def clearEntry():
    # clear search
    entry.delete(0, 'end')
    # clear data in textbox and update listbox
    value = ''
    data = hostnames
    listbox_update(data)
    # leave curser in focus in textbox
    entry.focus()

    # clear out all device infomration fields
    hostname_entry.delete(0,END)
    natIp_entry.delete(0,END)
    custIp_entry.delete(0,END)
    customer_entry.delete(0,END)
    model_entry.delete(0,END)
    serial_entry.delete(0,END)
    circuit_entry.delete(0,END)
    site_entry.delete(0,END)
    critical_entry.delete(0,END)
    sla_entry.delete(0,END)
    version_entry.delete(0,END)

    #Clear out dropdown cobo box
    comboBox.set('')

# used for Ping Button
def pingDevice():
    # Get IP from selection
    ip = getSelection()
    # Start cmd and ping IP
    os.system("start cmd /k ping " + ip + " -t")

# used for SSH Button
def sshDevice():
    # Get IP from selection
    ip = getSelection()
    # Start cmd and SSH to IP using Putty
    os.system("start cmd /k putty.exe -ssh " + ip + " 22")

# used for TELNET Button
def telnetDevice():
    # Get IP from selection
    ip = getSelection()
    # Start cmd and telnet to IP using Putty
    os.system("start cmd /k putty.exe -telnet " + ip + " 23")

# used for HTTP Button
def httpDevice():
    # Get IP from selection
    ip = getSelection()
    # Start browser and http to IP
    url = "http://" + ip
    os.startfile(url)

# used for HTTPS Button
def httpsDevice():
    # Get IP from selection
    ip = getSelection()
    # Start browser and https to IP
    url = "https://" + ip
    os.startfile(url)

# used for VNC Button
def vncDevice():
    # Get IP from selection
    ip = getSelection()
    # Start cmd and telnet to IP using Putty
    os.system("start cmd /k vncviewer.exe " + ip)

# used to get info from CSV for selected device
def infoDevice():
    # Get Current Selection
    selected = listbox.curselection()

    # Get the value of selection
    for item in selected:
        host = listbox.get(item)

    # Get all fields required from CSV
    ip = devices.loc[devices['Hostname'] == host, 'IP'].item()
    cust_ip = devices.loc[devices['Hostname'] == host, 'Customer IP'].item()
    customer = devices.loc[devices['Hostname'] == host, 'Company'].item()
    models = devices.loc[devices['Hostname'] == host, 'Model'].item()
    sn = devices.loc[devices['Hostname'] == host, 'Serial number'].item()
    circuit = devices.loc[devices['Hostname'] == host, 'Circuits'].item()
    site = devices.loc[devices['Hostname'] == host, 'Site'].item()
    critical = devices.loc[devices['Hostname'] == host, 'Critical'].item()
    sla = devices.loc[devices['Hostname'] == host, 'SLA'].item()
    version = devices.loc[devices['Hostname'] == host, 'OS Version'].item()

    # Display results in text fields
    hostname_entry.delete(0,END)
    hostname_entry.insert(0,host)
    natIp_entry.delete(0,END)
    natIp_entry.insert(0,ip)
    custIp_entry.delete(0,END)
    custIp_entry.insert(0,cust_ip)
    customer_entry.delete(0,END)
    customer_entry.insert(0,customer)
    model_entry.delete(0,END)
    model_entry.insert(0,models)
    serial_entry.delete(0,END)
    serial_entry.insert(0,sn)
    circuit_entry.delete(0,END)
    circuit_entry.insert(0,circuit)
    site_entry.delete(0,END)
    site_entry.insert(0,site)
    critical_entry.delete(0,END)
    critical_entry.insert(0,critical)
    sla_entry.delete(0,END)
    sla_entry.insert(0,sla)
    version_entry.delete(0,END)
    version_entry.insert(0,version)

# used for Dropdow when selecting a specific company
# display only hostnames in that company
def callbackFunc(event):
    company_Selected = comboBox.get()
    print (company_Selected)
    # locate all hostnames under that copany selected
    data = devices.loc[devices.Company == company_Selected, 'Hostname']
    # update data in listbox
    listbox_update(data)


#----main----#
host = ""
# Read in csv using pandas
devices = pd.read_csv("all_devices.csv")

# Get All hostnames in a sorted List
hostnames = devices['Hostname']
hostnames = list(hostnames)
hostnames = sorted(hostnames)
# Get All Comapnies in a sorted List
companies = devices['Company'].unique()
companies = list(companies)
companies = sorted(companies)

# nitalise Tkinter
root = Tk()
# Title on window
root.title('NMS HELPER 2.0')
# favicon for window
#root.iconbitmap("favicon.ico")
# Size of window
root.geometry('{}x{}'.format(460, 375))

# create all of the main containers
top_frame = Frame(root, bg='#333333', width=450, height=50, pady=3)
center = Frame(root, bg='gray2', width=50, height=40, padx=3, pady=3)
btm_frame = Frame(root, bg='#333333', width=450, height=45, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Set the way window can expand
top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")

# Create the widgets for the top frame
# Search Label and place in topframe
searchLabel = Label(top_frame, text="Filter Hostname:", bg='#333333', fg="grey")
# Entry textbox for user to filter results in topframe
entry = Entry(top_frame, bg='grey', font=(12))
# give curser focus 
entry.focus()
# when user adds charactrs to filter pass to on_keyrelease function
entry.bind('<KeyRelease>', on_keyrelease)
# Clear search Button assigned to top frame, if pressed pass to clearEntry function
clearSearch = Button(top_frame, text = "Clear Search", command = clearEntry)
# Company seach dropdown comboxbox in top frame
comboBoxLabel = Label(top_frame, text="Filter Company:", bg='#333333', fg="grey")
# Fill the combobox with companies
comboBox = ttk.Combobox(top_frame, values=companies)
# If user selects a company pass to callbackFunc to filter hostnames
comboBox.bind("<<ComboboxSelected>>", callbackFunc)

# layout the widgets in the top frame
searchLabel.grid(row=0, column=0)
entry.grid(row=0, column=1)
clearSearch.grid(row=0, column=2, padx=3, pady=3)
comboBoxLabel.grid(row=1, column=0)
comboBox.grid(row=1, column=1)

# create the center widgets row and columns 
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)
center.grid_columnconfigure(2, weight=4)

# layout the widgets in center frame
ctr_left = Frame(center, bg='#333333')
ctr_mid = Frame(center, bg='#333333')
ctr_right = Frame(center, bg='#333333', padx=3, pady=3)
ctr_left.grid(row=0, column=0, sticky="nsew")
ctr_mid.grid(row=0, column=1, sticky="nsew")
ctr_right.grid(row=0, column=2, sticky="nsew")

# create the widgets in the ctr_left Frame
scrollbar = Scrollbar(ctr_left)
# Make listbox with a black background and grey text
listbox = Listbox(ctr_left, bd=0, background="black", fg="grey",selectbackground="grey", font = (12))

# layout the scrollbar and listbox and attach in the ctr_left Frame
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(fill = BOTH, expand=True)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
# For debugging to show selection was selected in terminal
listbox.bind('<<ListboxSelect>>', on_select)

# Show all hostnames when first opening program
listbox_update(hostnames)

# create the widgets in the centre Right Frame to display hostname details
hostnameLabel = Label(ctr_mid, text="CUSTOMER:", bg='#333333', fg="grey", font = (12))
hostname_entry = Entry(ctr_right, text="",bg='grey',font = (12))
hostnameLabel = Label(ctr_mid, text="HOSTNAME:", bg='#333333', fg="grey",font = (12))
hostname_entry = Entry(ctr_right, text="",bg='grey',font = (12))
natIpLabel = Label(ctr_mid, text="NAT IP:", bg='#333333', fg="grey",font = (12))
natIp_entry = Entry(ctr_right, text="",bg='grey',font = (12))
custIpLabel = Label(ctr_mid, text="CUST IP:", bg='#333333', fg="grey",font = (12))
custIp_entry = Entry(ctr_right, text="",bg='grey',font = (12))
customerLabel = Label(ctr_mid, text="CUSTOMER:", bg='#333333', fg="grey",font = (12))
customer_entry = Entry(ctr_right, text="",bg='grey',font = (12))
modelLabel = Label(ctr_mid, text="MODEL:", bg='#333333', fg="grey",font = (12))
model_entry = Entry(ctr_right, text="",bg='grey',font = (12))
serialLabel = Label(ctr_mid, text="SERIAL(s):", bg='#333333', fg="grey",font = (12))
serial_entry = Entry(ctr_right, text="",bg='grey',font = (12))
circuitLabel = Label(ctr_mid, text="CIRCUIT(s):", bg='#333333', fg="grey",font = (12))
circuit_entry = Entry(ctr_right, text="",bg='grey',font = (12))
siteLabel = Label(ctr_mid, text="SITE:", bg='#333333', fg="grey",font = (12))
site_entry = Entry(ctr_right, text="",bg='grey',font = (12))

# For critical field to process TRUE or FALSE data
booleandf = devices.select_dtypes(include=[bool])
booleanDictionary = {True: 'TRUE', False: 'FALSE'}
for column in booleandf:
    devices[column] = devices[column].map(booleanDictionary)
# create out more widgets in the centre Right Frame to display hostname details
criticalLabel = Label(ctr_mid, text="CRITICAL:", bg='#333333', fg="grey",font = (12))
critical_entry = Entry(ctr_right, text="",bg='grey',font = (12))
slaLabel = Label(ctr_mid, text="SLA:", bg='#333333', fg="grey",font = (12))
sla_entry = Entry(ctr_right, text="",bg='grey',font = (12))
versionLabel = Label(ctr_mid, text="VERSION:", bg='#333333', fg="grey",font = (12))
version_entry = Entry(ctr_right, text="",bg='grey',font = (12))

# layout the widgets in the ctr_right Frame
hostnameLabel.pack(fill = X, expand=True)
hostname_entry.pack(fill = X, expand=True)
hostnameLabel.pack(fill = X, expand=True)
hostname_entry.pack(fill = X, expand=True)
natIpLabel.pack(fill = X, expand=True)
natIp_entry.pack(fill = X, expand=True)
custIpLabel.pack(fill = X, expand=True)
custIp_entry.pack(fill = X, expand=True)
customerLabel.pack(fill = X, expand=True)
customer_entry.pack(fill = X, expand=True)
modelLabel.pack(fill = X, expand=True)
model_entry.pack(fill = X, expand=True)
serialLabel.pack(fill = X, expand=True)
serial_entry.pack(fill = X, expand=True)
circuitLabel.pack(fill = X, expand=True)
circuit_entry.pack(fill = X, expand=True)
siteLabel.pack(fill = X, expand=True)
site_entry.pack(fill = X, expand=True)
criticalLabel.pack(fill = X, expand=True)
critical_entry.pack(fill = X, expand=True)
slaLabel.pack(fill = X, expand=True)
sla_entry.pack(fill = X, expand=True)
versionLabel.pack(fill = X, expand=True)
version_entry.pack(fill = X, expand=True)

# create the buttons in the Bottom Frame to send to each function to action
ping = Button(btm_frame, text = "PING", command = pingDevice, font = (12))
ssh = Button(btm_frame, text = "SSH", command = sshDevice, font = (12))
telnet = Button(btm_frame, text = "TELNET", command = telnetDevice, font = (12))
http = Button(btm_frame, text = "HTTP", command = httpDevice, font = (12))
https = Button(btm_frame, text = "HTTPS", command = httpsDevice, font = (12))
vnc = Button(btm_frame, text = "VNC", command = vncDevice, font = (12))

# layout the widgets in the Bottom Frame
ping.grid(row=0, column=1, padx=3, pady=3)
ssh.grid(row=0, column=2, padx=3, pady=3)
telnet.grid(row=0, column=3, padx=3, pady=3)
http.grid(row=0, column=4, padx=3, pady=3)
https.grid(row=0, column=5, padx=3, pady=3)
vnc.grid(row=0, column=6, padx=3, pady=3)

# run the program
root.mainloop()
