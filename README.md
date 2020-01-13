# Capstone
 Capstone project for the course Lisbon Data Science Starters Academy, Batch \#3

# Get the Data!
First thing you have to do is download the training data and save it under the root directory 'data/'

The data can be found here:
 - train dataset: http://storage.googleapis.com/capstone_train/train.csv

There is also a data dictionary to help understand the dataset

 - data dictionary: https://docs.google.com/spreadsheets/d/1m0AtSkv-Dk91Qm2tWsXHaPFguQUdDNhwy34AO8htkBw/edit#gid=0

# Connect to remote server

## jupyter notebook tunnel
```
ssh -i <path_to_priv_key> -N -f -L localhost:<local_port_tunel>:localhost:<remote_port_where_notebook_running>
```
## ratom connection
```
ssh -i <path_to_priv_key> -R 52698:localhost:52698 <user>@<ip>
```
## normal connection
```
ssh -i <path_to_priv_key> <user>@<ip>
```

# utils

## screen

http://thingsilearned.com/2009/05/26/gnu-screen-super-basic-tutorial/
